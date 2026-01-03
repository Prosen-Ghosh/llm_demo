#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import torch
import os
from datasets import load_dataset, DatasetDict, Audio
from transformers import (
    WhisperFeatureExtractor,
    WhisperTokenizer,
    WhisperProcessor,
    WhisperForConditionalGeneration,
    Seq2SeqTrainingArguments,
    Seq2SeqTrainer
)
from dataclasses import dataclass
from typing import Any, Dict, List, Union
import evaluate

def main():
    print(f"PyTorch version: {torch.__version__}")
    print(f"MPS available: {torch.backends.mps.is_available()}")
    print(f"MPS built: {torch.backends.mps.is_built()}")
    
    # Set device
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    print(f"Using device: {device}")
    
    # Load dataset
    print("Loading dataset...")
    common_voice = DatasetDict()
    common_voice["train"] = load_dataset("arifulFarhad/mozilla-bangla-dataset", split="train+validation")
    common_voice["test"] = load_dataset("arifulFarhad/mozilla-bangla-dataset", split="test")
    
    # Remove unnecessary columns
    common_voice = common_voice.remove_columns(["age", "client_id", "gender"])
    
    # Initialize processor
    print("Initializing processor...")
    feature_extractor = WhisperFeatureExtractor.from_pretrained("openai/whisper-medium")
    tokenizer = WhisperTokenizer.from_pretrained("openai/whisper-medium", language="Bengali", task="transcribe")
    processor = WhisperProcessor.from_pretrained("openai/whisper-medium", language="Bengali", task="transcribe")
    
    # Cast audio column to 16kHz
    common_voice = common_voice.cast_column("audio", Audio(sampling_rate=16000))
    
    def prepare_dataset(batch):
        # Load and resample audio
        audio = batch["audio"]
        
        # Compute log-Mel input features
        batch["input_features"] = feature_extractor(
            audio["array"], 
            sampling_rate=audio["sampling_rate"]
        ).input_features[0]
        
        # Encode target text
        batch["labels"] = tokenizer(batch["sentence"]).input_ids
        return batch
    
    # Prepare dataset
    print("Preparing dataset...")
    common_voice = common_voice.map(
        prepare_dataset, 
        remove_columns=common_voice.column_names["train"], 
        num_proc=min(6, os.cpu_count() or 1)
    )
    
    # Load model
    print("Loading model...")
    model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-medium")
    
    # Configure generation
    model.generation_config.language = "bengali"
    model.generation_config.task = "transcribe"
    model.generation_config.forced_decoder_ids = None
    
    # Move model to device
    model.to(device)
    
    # Data collator
    @dataclass
    class DataCollatorSpeechSeq2SeqWithPadding:
        processor: Any
        decoder_start_token_id: int

        def __call__(self, features: List[Dict[str, Union[List[int], torch.Tensor]]]) -> Dict[str, torch.Tensor]:
            input_features = [{"input_features": feature["input_features"]} for feature in features]
            batch = self.processor.feature_extractor.pad(input_features, return_tensors="pt")
            
            label_features = [{"input_ids": feature["labels"]} for feature in features]
            labels_batch = self.processor.tokenizer.pad(label_features, return_tensors="pt")
            
            labels = labels_batch["input_ids"].masked_fill(labels_batch.attention_mask.ne(1), -100)
            
            if (labels[:, 0] == self.decoder_start_token_id).all().cpu().item():
                labels = labels[:, 1:]
            
            batch["labels"] = labels
            return batch
    
    data_collator = DataCollatorSpeechSeq2SeqWithPadding(
        processor=processor,
        decoder_start_token_id=model.config.decoder_start_token_id,
    )
    
    # Metrics
    metric = evaluate.load("wer")
    
    def compute_metrics(pred):
        pred_ids = pred.predictions
        label_ids = pred.label_ids
        
        label_ids[label_ids == -100] = tokenizer.pad_token_id
        
        pred_str = tokenizer.batch_decode(pred_ids, skip_special_tokens=True)
        label_str = tokenizer.batch_decode(label_ids, skip_special_tokens=True)
        
        wer = 100 * metric.compute(predictions=pred_str, references=label_str)
        return {"wer": wer}
    
    # Training arguments
    training_args = Seq2SeqTrainingArguments(
        output_dir="./whisper-medium-bn",
        per_device_train_batch_size=16,
        gradient_accumulation_steps=1,  # Increased for MPS stability
        learning_rate=1e-5,
        warmup_steps=50,
        max_steps=500,
        gradient_checkpointing=False,
        fp16=False,  # MPS doesn't support fp16 well yet
        bf16=False,   # MPS doesn't support bf16
        eval_strategy="steps",
        per_device_eval_batch_size=8,
        predict_with_generate=True,
        generation_max_length=225,
        save_steps=100,
        eval_steps=100,
        logging_steps=25,
        report_to=["tensorboard"],
        load_best_model_at_end=True,
        metric_for_best_model="wer",
        greater_is_better=False,
        push_to_hub=False,
        remove_unused_columns=False,
        dataloader_num_workers=min(6, os.cpu_count() or 1),  # Reduced for MPS
    )
    
    # Trainer
    trainer = Seq2SeqTrainer(
        args=training_args,
        model=model,
        train_dataset=common_voice["train"],
        eval_dataset=common_voice["test"],
        data_collator=data_collator,
        compute_metrics=compute_metrics,
        tokenizer=processor.feature_extractor,
    )
    
    # Train
    print("Starting training...")
    trainer.train()
    
    # Save final model
    print("Saving model...")
    trainer.save_model("./whisper-medium-bn-final")
    
    print("Training completed!")

if __name__ == "__main__":
    main()