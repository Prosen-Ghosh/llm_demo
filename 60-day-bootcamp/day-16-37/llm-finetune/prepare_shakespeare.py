from datasets import load_dataset, Dataset, DatasetDict, load_from_disk
from transformers import AutoTokenizer
import os

print("📥 Loading tiny_shakespeare dataset...")
dataset = load_dataset('text', data_files={'train': 'https://raw.githubusercontent.com/karpathy/char-rnn/master/data/tinyshakespeare/input.txt'})

print(f"\n📊 Original dataset size: {len(dataset['train'])} lines")
print(f"First few characters of text: {dataset['train'][0]['text'][:200]}...")

print("\n🔤 Loading gpt2-medium tokenizer...")
tokenizer = AutoTokenizer.from_pretrained("gpt2-medium")
tokenizer.pad_token = tokenizer.eos_token

print("\n⚡ Tokenizing dataset...")
def tokenize_function(examples):
    return tokenizer(examples["text"], truncation=False, padding=False)

# Tokenize the entire dataset
tokenized = tokenize_function({"text": [dataset['train'][i]['text'] for i in range(len(dataset['train']))]})

print(f"\n📊 Tokenized: {len(tokenized['input_ids'])} sequences")

print("\n✂️ Concatenating and chunking into blocks of size 128...")
block_size = 128

# Concatenate all token sequences
all_input_ids = []
all_attention_mask = []

for i in range(len(tokenized['input_ids'])):
    all_input_ids.extend(tokenized['input_ids'][i])
    all_attention_mask.extend(tokenized['attention_mask'][i] if 'attention_mask' in tokenized else [1] * len(tokenized['input_ids'][i]))

print(f"Total tokens: {len(all_input_ids)}")

# Create chunks
input_ids_chunks = []
attention_mask_chunks = []

for i in range(0, len(all_input_ids) - block_size + 1, block_size):
    input_ids_chunks.append(all_input_ids[i:i+block_size])
    attention_mask_chunks.append(all_attention_mask[i:i+block_size])

print(f"Created {len(input_ids_chunks)} chunks of size {block_size}")

# Create a new dataset
chunked_dataset = Dataset.from_dict({
    'input_ids': input_ids_chunks,
    'attention_mask': attention_mask_chunks,
    'labels': input_ids_chunks  # For language modeling, labels are same as input_ids
})

# Wrap in DatasetDict
dataset_dict = DatasetDict({'train': chunked_dataset})

print(f"\n📊 Final dataset: {len(dataset_dict['train'])} chunks")
if len(dataset_dict['train']) > 0:
    print(f"  First chunk length: {len(dataset_dict['train'][0]['input_ids'])}")
    print(f"  Decoded sample: {tokenizer.decode(dataset_dict['train'][0]['input_ids'][:50])}...")

print("\n💾 Saving to disk...")
output_path = "./shakespeare_prepared"

# Remove old directory if it exists
import shutil
if os.path.exists(output_path):
    shutil.rmtree(output_path)

dataset_dict.save_to_disk(output_path)

print(f"✅ Prepared dataset saved to {output_path}")
print(f"\nVerification:")
print(f"  Saved path exists: {os.path.exists(output_path)}")
print(f"  Size of dataset: {len(dataset_dict['train'])} chunks")

# Quick test load
print("\n🧪 Testing load...")
test_load = load_from_disk(output_path)
print(f"  Loaded splits: {list(test_load.keys())}")
print(f"  Train split columns: {test_load['train'].column_names}")
print(f"  Number of examples: {len(test_load['train'])}")
if len(test_load['train']) > 0:
    print(f"  First example keys: {list(test_load['train'][0].keys())}")