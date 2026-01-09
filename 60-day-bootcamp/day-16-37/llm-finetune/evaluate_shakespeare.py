import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from tqdm import tqdm
from datasets import load_dataset

model_path = "./gpt2-shakespeare-finetuned"
base_model_path = "gpt2-medium"

print(f"🤖 Loading fine-tuned model and tokenizer from: {model_path}...")

device = "mps" if torch.backends.mps.is_available() else "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

model = AutoModelForCausalLM.from_pretrained(model_path).to(device)
tokenizer = AutoTokenizer.from_pretrained(model_path)

text = """
I tell you, friends, most charitable care
Have the patricians of you. For your wants,
Your suffering in this dearth, you may as well
Strike at the heaven with your staves as lift them
Against the Roman state, whose course will on
The way it takes, cracking ten thousand curbs
Of more strong link asunder than can ever
Appear in your impediment. For the dearth,
The gods, not the patricians, make it, and
Your knees to them, not arms, must help. Alack,
You are transported by calamity
Thither where more attends you, and you slander
The helms o' the state, who care for you like fathers,
When you curse them as enemies.
"""

encoding = tokenizer(text, return_tensors="pt").to(device)

with torch.no_grad():
    outputs = model(**encoding, labels=encoding["input_ids"])
    loss = outputs.loss
    perplexity = torch.exp(loss)

# print(f"Phrase: '{text}'")
print(f"=" * 40)
print("Calculating Perplexity Manually")
print(f"=" * 40)
print(f"Loss: {loss.item():.4f}")
print(f"Perplexity: {perplexity.item():.4f}")

print('\n')
print(f"=" * 40)
print("Batch Evaluation on WikiText-2")
print(f"=" * 40)

def evaluate_perplexity(model, tokenizer, wiki_data, max_samples=100):
    model.eval()
    total_loss = 0.0
    total_steps = 0

    print("Evaluating on WikiText-2 test set...")

    for i in tqdm(range(min(max_samples, len(wiki_data)))):
        sample = wiki_data[i]

        input = tokenizer(
            sample["text"],
            return_tensors="pt",
            truncation=True,
            max_length=512,
        ).to(device)

        if input["input_ids"].shape[1] < 2:
            continue

        with torch.no_grad():
            outputs = model(**input, labels=input["input_ids"])
            total_loss += outputs.loss
            total_steps += 1

    avg_loss = total_loss / total_steps
    perplexity = torch.exp(avg_loss)
    return perplexity

wiki_data = load_dataset("wikitext", "wikitext-2-raw-v1", split="test")

ppl_score = evaluate_perplexity(model, tokenizer, wiki_data)
print(f"Perplexity on WikiText-2 test set: {ppl_score:.4f}")

print('\n')
print(f"=" * 40)
print(f"The Turing Test")
print(f"=" * 40)

base_model = AutoModelForCausalLM.from_pretrained(base_model_path).to(device)
finetuned_model = model

prompt = "The king said"

def generate(mdl, p):
    inputs = tokenizer(p, return_tensors="pt").to(device)
    outputs = mdl.generate(
        **inputs,
        max_new_tokens=50,
        do_sample=True,
        temperature=0.7,
        pad_token_id=tokenizer.eos_token_id,
    )
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

print("\n--- Base Model Output ---")
base_output = generate(base_model, prompt)
print(base_output)

print("\n--- Fine-tuned Model Output ---")
finetuned_output = generate(finetuned_model, prompt)
print(finetuned_output)