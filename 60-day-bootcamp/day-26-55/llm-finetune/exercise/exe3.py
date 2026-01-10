import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from verify_hardware import device

tokenizer = AutoTokenizer.from_pretrained("gpt2-medium")
model = AutoModelForCausalLM.from_pretrained("gpt2-medium")
model.to(device) 

def generate_text(prompt, max_new_tokens=15):
    inputs = tokenizer(prompt, return_tensors="pt").to(device)
    input_ids = inputs["input_ids"]
    
    print(f"Generating from: '{prompt}'")
    
    for _ in range(max_new_tokens):
        with torch.no_grad():
            outputs = model(input_ids)
            next_token_logits = outputs.logits[0, -1, :]
            next_token_id = torch.argmax(next_token_logits).unsqueeze(0).unsqueeze(0)

            input_ids = torch.cat([input_ids, next_token_id], dim=1)

            word = tokenizer.decode(next_token_id[0])
            if not word:
                break
            print(word, end="", flush=True)
            
    return tokenizer.decode(input_ids[0])

full_text = generate_text("Artificial Intelligence is")
print("\n\nFinal Result:", full_text)