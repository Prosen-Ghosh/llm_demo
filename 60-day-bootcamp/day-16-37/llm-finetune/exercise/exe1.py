from transformers import AutoTokenizer

model_id = "distilgpt2" 
tokenizer = AutoTokenizer.from_pretrained(model_id)

text = "Fine-tuning is fascinating."
encoded = tokenizer(text, return_tensors="pt")

print(f"Input Text: {text}")
print(f"Input IDs: {encoded['input_ids']}")

decoded = tokenizer.decode(encoded['input_ids'][0])
print(f"Decoded: {decoded}")

if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token
    print("Set pad_token to eos_token")