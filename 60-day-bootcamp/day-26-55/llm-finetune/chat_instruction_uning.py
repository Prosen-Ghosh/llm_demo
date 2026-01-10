from datasets import load_dataset
import pandas as pd
from transformers import AutoTokenizer

dataset = load_dataset("yahma/alpaca-cleaned", split="train[:500]")

df = pd.DataFrame(dataset)
print(df.head(3))

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

formatted_dataset = dataset.map(format_alpaca)

print("--- RAW SAMPLE ---")
print(formatted_dataset[0]['text'])

model_id = "gpt2-medium" 
tokenizer = AutoTokenizer.from_pretrained(model_id)
tokenizer.pad_token = tokenizer.eos_token

def tokenize_function(sample):
    text = sample["text"] + tokenizer.eos_token
    
    tokenized = tokenizer(
        text,
        truncation=True,
        max_length=256,
        padding="max_length"
    )
    
    tokenized["labels"] = tokenized["input_ids"].copy()
    return tokenized

tokenized_dataset = formatted_dataset.map(tokenize_function, batched=False)

print(f"Input IDs Length: {len(tokenized_dataset[0]['input_ids'])}")
print(f"Last Token ID: {tokenized_dataset[0]['input_ids'][-1]}")