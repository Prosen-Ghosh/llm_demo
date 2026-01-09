import os
import shutil
import json
from datasets import load_dataset, Dataset
from transformers import AutoTokenizer
import pandas as pd
import traceback

MODEL_ID = "gpt2-medium" 
MAX_LENGTH = 256 
SPLIT = "train[:500]"
OUT_DIR = "./alpaca_prepared"

def format_alpaca(sample):
    instruction = sample['instruction']
    input_text = sample['input']
    output = sample['output']

    if input_text:
        text = f"""### Instruction:
            {instruction}

            ### Input:
            {input_text}

            ### Response:
            {output}"""
    else:
        text = f"""### Instruction:
            {instruction}

            ### Response:
            {output}"""
    
    return {"text": text}

def simple_byte_tokenize(batch, max_length):
    input_ids_list = []
    attention_mask_list = []
    labels_list = []

    for t in batch["text"]:
        b = t.encode("utf-8", error="replace")[:max_length]
        ids = list(b)
        pad_len = max_length - len(ids)
        ids_padded = ids + [0] * pad_len
        attn = [1] * len(ids) + [0] * pad_len
        input_ids_list.append(ids_padded)
        attention_mask_list.append(attn)
        labels_list.append(ids_padded.copy())

    return {
        "input_ids": input_ids_list,
        "attention_mask": attention_mask_list,
        "labels": labels_list
    }

def main():
    print(f"Loading dataset 'yahma/alpaca-cleaned' slice {SPLIT} ...")
    ds = load_dataset("yahma/alpaca-cleaned", split=SPLIT)
    print("Loaded dataset. Examples:", len(ds))

    formatted = ds.map(lambda ex: format_alpaca(ex), remove_columns=ds.column_names)
    print("\n--- RAW FORMATTED SAMPLE (first example) ---\n")
    print(formatted[0]["text"][:1000])

    print("\nLoading tokenizer:", MODEL_ID)
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    print("Tokenizer loaded. Vocab size:", getattr(tokenizer, "vocab_size", "unknown"))

    def tok_fn(batch):
        texts = [t + tokenizer.eos_token for t in batch["text"]]
        enc = tokenizer(texts, truncation=True, padding="max_length", max_length=MAX_LENGTH)
        enc["labels"] = [list(ids) for ids in enc["input_ids"]]
        return enc
    
    tokenized = formatted.map(tok_fn, batched=True, batch_size=16, remove_columns=formatted.column_names)

    sample = tokenized[0]
    print("\n--- TOKENIZATION DIAGNOSTICS ---")
    print("Input length:", len(sample["input_ids"]))
    print("First 20 input ids:", sample["input_ids"][:20])
    print("Last token id:", sample["input_ids"][-1])

    if os.path.exists(OUT_DIR):
        shutil.rmtree(OUT_DIR)
    tokenized.save_to_disk(OUT_DIR)
    
    print("Summary:")
    print(json.dumps({
        "num_examples_saved": len(tokenized),
        "max_length": MAX_LENGTH,
        "output_dir": OUT_DIR
    }, indent=2))

if __name__ == "__main__":
    main()

