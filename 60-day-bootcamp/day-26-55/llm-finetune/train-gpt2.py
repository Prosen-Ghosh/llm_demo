from transformers import AutoModelForCausalLM, AutoTokenizer, DataCollatorForLanguageModeling, TrainingArguments, Trainer
from peft import get_peft_model, LoraConfig, TaskType, PeftModel, PeftConfig
from datasets import load_from_disk

model_name = "gpt2-medium"
print(f"🤖 Loading pre-trained model and tokenizer: {model_name}...")

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

peft_config = LoraConfig(
    task_type=TaskType.CAUSAL_LM,
    inference_mode=False,
    r=64,
    lora_alpha=32,
    lora_dropout=0.1,
    target_modules=["c_attn"],
)

lora_model = get_peft_model(model, peft_config)

print("📊 LoRA Model Summary:")
lora_model.print_trainable_parameters()

print("\n")
print(f"=" * 40)
print("Starting Fine-Tuning with LoRA")
print(f"=" * 40)

print("📥 Loading tiny_shakespeare dataset...")
dataset = load_from_disk('./shakespeare_prepared')

tokenizer.pad_token = tokenizer.eos_token
model.config.pad_token_id = model.config.eos_token_id

data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer,
    mlm=False,
)

output_dir = "./gpt2-lora-shakespeare"

training_args = TrainingArguments(
    output_dir=output_dir,
    overwrite_output_dir=True,

    per_device_train_batch_size=4,
    gradient_accumulation_steps=8,

    num_train_epochs=3,
    learning_rate=1e-4,
    weight_decay=0.01,

    logging_steps=10,
    save_strategy="no",
)

trainer = Trainer(
    model=lora_model,
    args=training_args,
    train_dataset=dataset['train'],
    data_collator=data_collator,
    tokenizer=tokenizer, 
)

print("\n🚀 Starting fine-tuning...")
trainer.train()

lora_model.save_pretrained("./shakespeare-adapter")

print(f"\n✅ Fine-tuned model and tokenizer saved to {output_dir}")

print("\n")
print(f"=" * 40)
print("Loading the adapter for inference")
print(f"=" * 40)

base_model = AutoModelForCausalLM.from_pretrained(model_name).to("mps")
model = PeftModel.from_pretrained(base_model, "./shakespeare-adapter")

inputs = tokenizer("Shall i compare thee", return_tensors="pt").to("mps")
outputs = model.generate(
    **inputs,
    max_new_tokens=50,
    do_sample=True,
    temperature=0.7,
    pad_token_id=tokenizer.eos_token_id,
)

print("\n--- Generated Text with LoRA Adapter ---")
print(tokenizer.decode(outputs[0], skip_special_tokens=True))

