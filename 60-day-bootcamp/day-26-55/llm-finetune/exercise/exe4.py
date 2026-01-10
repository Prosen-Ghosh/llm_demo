from datasets import load_dataset
from transformers import AutoTokenizer

# dataset = load_dataset('wikitext', "wikitext-2-raw-v1")
dataset = load_dataset('text', data_files={'train': './data/my_data.txt'})
# print("Data Structure:", dataset)
# print("Sample Data:", dataset['train'][10]["text"])

debug_dataset = dataset['train'].select(range(10))
print("Debug Dataset Size:", len(debug_dataset))

model_checkpoint = 'gpt2-medium'
tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)

def tokenize_function(examples):
    return tokenizer(examples['text'])

tokenized_datasets = dataset.map(
    tokenize_function, 
    batched=False, 
    num_proc=6, 
    remove_columns=["text"]
)

# print("Sample Tokenized Data:", tokenized_datasets['train'][10])

block_size = 512

def group_texts(examples):
    concatenated_examples = {
        k: sum(examples[k], []) for k in examples.keys()
    }

    total_length = len(concatenated_examples[list(examples.keys())[0]])

    if total_length >= block_size:
        total_length = (total_length // block_size) * block_size

    result = {
        k: [t[i : i + block_size] for i in range(0, total_length, block_size)]
        for k, t in concatenated_examples.items()
    }

    result["labels"] = result["input_ids"].copy()
    return result

lm_datasets = tokenized_datasets.map(
    group_texts,
    batched=True,
    num_proc=6,
)

print(f"Original row count: {len(tokenized_datasets['train'])}")
print(f"Chunked row count: {len(lm_datasets['train'])}")