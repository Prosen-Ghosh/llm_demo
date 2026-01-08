# LLM Finetuning Project

This project demonstrates how to finetune a large language model (LLM) on a custom dataset, specifically the works of William Shakespeare. The goal is to adapt a pre-trained model to generate text in a specific style.

## Why

Finetuning is a crucial technique for adapting powerful pre-trained language models to specific tasks or domains. This project serves as a practical example of how to:

*   Prepare a custom dataset for finetuning.
*   Use a pre-trained model and tokenizer from the Hugging Face Hub.
*   Finetune the model on the custom dataset.
*   Do so efficiently, even on consumer hardware, by using techniques like parameter-efficient finetuning (PEFT) and 8-bit quantization.

## How

### 1. Setup

First, install the required dependencies:

```bash
pip install -r requirements.txt
```

### 2. Verify Hardware

This project can run on CPU, Apple's Metal Performance Shaders (MPS), or CUDA-enabled GPUs. To check which hardware will be used, run:

```bash
python verify_hardware.py
```

### 3. Prepare Data

The `prepare_shakespeare.py` script downloads the "tiny_shakespeare" dataset, tokenizes it using the "gpt2-medium" tokenizer, and saves the processed dataset to the `shakespeare_prepared/` directory.

To run the script:

```bash
python prepare_shakespeare.py
```

### 4. Finetune the Model

(Instructions for finetuning will be added here once the finetuning script is available.)
