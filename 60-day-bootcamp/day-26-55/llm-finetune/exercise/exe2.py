import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from verify_hardware import device

tokenizer = AutoTokenizer.from_pretrained("distilgpt2")

device = "mps" if torch.backends.mps.is_available() else "cpu"
print(f"Loading model to {device}...")

model = AutoModelForCausalLM.from_pretrained("distilgpt2")
model.to(device)

text = "The quick brown fox jumps over the"
inputs = tokenizer(text, return_tensors="pt").to(device)

with torch.no_grad():
    outputs = model(**inputs)
    logits = outputs.logits
    next_token_logits = logits[0, -1, :]
    next_token_id = torch.argmax(next_token_logits).item()
    next_word = tokenizer.decode(next_token_id)

print(f"Prompt: {text}")
print(f"Model prediction: '{next_word}'") # Should be ' dog' or ' lazy'