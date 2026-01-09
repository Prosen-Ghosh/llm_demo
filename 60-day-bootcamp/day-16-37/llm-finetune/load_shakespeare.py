from transformers import AutoTokenizer, AutoModelForCausalLM, DataCollatorForLanguageModeling, TrainingArguments, Trainer
from datasets import load_from_disk
import torch

print("📥 Loading tiny_shakespeare dataset...")
dataset = load_from_disk('./shakespeare_prepared')

print(f"Dataset columns: {dataset['train'].column_names}")
print(f"Dataset size: {len(dataset['train'])} samples")
print(f"First sample keys: {list(dataset['train'][0].keys())}")

model_name = "gpt2-medium"
print(f"\n🤖 Loading pre-trained model and tokenizer: {model_name}...")
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

tokenizer.pad_token = tokenizer.eos_token
model.config.pad_token_id = model.config.eos_token_id

data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer,
    mlm=False,
)

print(f"\n📊 Dataset info:")
print(f"  Number of training samples: {len(dataset['train'])}")
print(f"  First sample input_ids length: {len(dataset['train'][0]['input_ids'])}")
print(f"  Model parameters: {model.num_parameters() / 1_000_000:.1f}M")

output_dir = "./gpt2-shakespeare-finetuned"

training_args = TrainingArguments(
    output_dir=output_dir,
    overwrite_output_dir=True,

    per_device_train_batch_size=4,
    gradient_accumulation_steps=8,

    num_train_epochs=3,
    learning_rate=5e-5,
    weight_decay=0.01,

    logging_steps=10,
    save_strategy="epoch",
    seed=42
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset['train'],
    data_collator=data_collator,
    tokenizer=tokenizer, 
)

print("\n🚀 Starting fine-tuning...")
trainer.train()

trainer.save_model(output_dir)
tokenizer.save_pretrained(output_dir)

print(f"\n✅ Fine-tuned model and tokenizer saved to {output_dir}")