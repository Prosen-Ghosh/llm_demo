from datasets import load_dataset
from transformers import AutoTokenizer
import os

print("📥 Loading tiny_shakespeare dataset...")
dataset = load_dataset('text', data_files={'train': 'https://raw.githubusercontent.com/karpathy/char-rnn/master/data/tinyshakespeare/input.txt'})

print("\n🔤 Loading gpt2-medium tokenizer...")
tokenizer = AutoTokenizer.from_pretrained("gpt2-medium")
tokenizer.pad_token = tokenizer.eos_token

def tokenize_function(examples):
    tokenized = tokenizer(
        examples["text"],
        padding=False,
    )
    
    return tokenized

print("\n⚡ Tokenizing dataset...")
tokenized_dataset = dataset.map(
    tokenize_function,
    batched=True,
    remove_columns=["text"],
    desc="Tokenizing texts",
    num_proc=6, 
)

print("\n✂️ Chunking into blocks of size 128...")

def chunk_examples(examples, chunk_size=128):
    # Concatenate all input_ids from the batch
    concatenated_input_ids = []
    concatenated_attention_mask = []
    
    for i in range(len(examples['input_ids'])):
        concatenated_input_ids.extend(examples['input_ids'][i])
        # For attention mask, use all 1s if not provided
        if 'attention_mask' in examples:
            concatenated_attention_mask.extend(examples['attention_mask'][i])
        else:
            concatenated_attention_mask.extend([1] * len(examples['input_ids'][i]))
    
    # Split into chunks
    total_length = len(concatenated_input_ids)
    total_length = (total_length // chunk_size) * chunk_size
    
    input_ids_chunks = []
    attention_mask_chunks = []
    
    for i in range(0, total_length, chunk_size):
        input_ids_chunks.append(concatenated_input_ids[i:i+chunk_size])
        attention_mask_chunks.append(concatenated_attention_mask[i:i+chunk_size])
    
    return {
        'input_ids': input_ids_chunks,
        'attention_mask': attention_mask_chunks
    }

# Process the dataset in smaller batches for chunking
chunked_dataset = tokenized_dataset.map(
    chunk_examples,
    batched=True,
    batch_size=1000,  # Process in smaller batches
    desc="Chunking into blocks",
    num_proc=6, 
)

print(f"\n📊 After chunking:")
for split in chunked_dataset:
    print(f"  {split}: {len(chunked_dataset[split])} blocks")
    if len(chunked_dataset[split]) > 0:
        print(f"    First block shape: {len(chunked_dataset[split]['input_ids'][0])} tokens")

print("\n💾 Saving to disk...")
output_path = "./shakespeare_prepared"
chunked_dataset.save_to_disk(output_path)
print(f"Prepared dataset saved to {output_path}")
print("\n✅ Verification:")
print(f"Saved to: {os.path.abspath(output_path)}")