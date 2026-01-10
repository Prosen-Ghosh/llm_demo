from transformers import AutoModelForCausalLM, AutoTokenizer, DataCollatorForLanguageModeling, TrainingArguments, Trainer
from peft import get_peft_model, LoraConfig, TaskType, PeftModel, PeftConfig
from datasets import load_from_disk
import torch

model_name = "gpt2-medium"
print(f"🤖 Loading base model: {model_name}...")

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

print("\n")
print(f"=" * 40)
print("Loading the adapter for inference")
print(f"=" * 40)

base_model = AutoModelForCausalLM.from_pretrained(model_name).to("mps")
model = PeftModel.from_pretrained(base_model, "./shakespeare-adapter")

device = "mps" if torch.backends.mps.is_available() else "cpu"
model.to(device)


prompt = "The iPhone is a device that"
input_ids = tokenizer(prompt, return_tensors="pt").to(device)

print("--- GREEDY DECODING ---")

outputs = model.generate(**input_ids, max_new_tokens=50, do_sample=False, pad_token_id=tokenizer.eos_token_id)
print(tokenizer.decode(outputs[0], skip_special_tokens=True))

print("\n")
print(f"=" * 40)
print("Tuning Temperature & Top-K")
print(f"=" * 40)

print("\n--- HIGH TEMP (Creative/Crazy) ---")
outputs = model.generate(
    **input_ids, 
    max_new_tokens=50, 
    do_sample=True, 
    temperature=1.5,
    top_k=0,
    pad_token_id=tokenizer.eos_token_id
)
print(tokenizer.decode(outputs[0], skip_special_tokens=True))

print("\n--- LOW TEMP (Conservative) ---")
outputs = model.generate(
    **input_ids, 
    max_new_tokens=50, 
    do_sample=True, 
    temperature=0.6, 
    top_k=50,
    pad_token_id=tokenizer.eos_token_id
)
print(tokenizer.decode(outputs[0], skip_special_tokens=True))

print("\n")
print(f"=" * 40)
print("The Gold Standard (Top-P + Repetition Penalty)")
print(f"=" * 40)

print("\n--- OPTIMIZED INFERENCE ---")
outputs = model.generate(
    **input_ids, 
    max_new_tokens=100, 
    do_sample=True, 
    
    temperature=0.8,
    top_p=0.92,
    top_k=50,
    
    repetition_penalty=1.2,
    no_repeat_ngram_size=2,
    pad_token_id=tokenizer.eos_token_id
)
print(tokenizer.decode(outputs[0], skip_special_tokens=True))