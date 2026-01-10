import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import LoraConfig
from datasets import load_dataset
from trl import SFTTrainer, SFTConfig

dataset = load_dataset("yahma/alpaca-cleaned", split="train[:500]")

# print(dataset[:1])
# print("\n\n\n")

model_name = "gpt2-medium"
print(f"🤖 Loading base model: {model_name}...")
tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.pad_token = tokenizer.eos_token
tokenizer.padding_side = "right"
tokenizer.model_max_length = 512

peft_config = LoraConfig(
    r=16,
    lora_alpha=32,
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)

def formatting_prompts_func(example):
    instruction = example["instruction"]
    output = example["output"]
    input_text = example.get("input", "")

    if input_text and input_text.strip():
        text = (
            f"### Instruction:\n{instruction}\n\n"
            f"### Input:\n{input_text}\n\n"
            f"### Response:\n{output}"
        )
    else:
        text = (
            f"### Instruction:\n{instruction}\n\n"
            f"### Response:\n{output}"
        )

    return text


response_template = "### Response:\n"

sft_config = SFTConfig(
    output_dir="./alpaca-sft-gpt2-medium",
    packing=False,
    num_train_epochs=1,
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,
    learning_rate=2e-4,
    logging_steps=10,
    save_strategy="epoch",
    dataset_text_field="text"
)

trainer = SFTTrainer(
    model=model_name,
    train_dataset=dataset,
    peft_config=peft_config,
    formatting_func=formatting_prompts_func,
    args=sft_config,
)

print("Starting SFT Training...")
trainer.train()

trainer.save_model("./alpaca-sft-final")

