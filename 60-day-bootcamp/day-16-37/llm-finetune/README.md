# LLM Finetuning Project

This project provides a comprehensive guide to fine-tuning Large Language Models (LLMs) using various techniques and datasets. It covers data preparation, model training (including parameter-efficient methods), and evaluation.

## Features

*   **Hardware Verification**: Check your hardware (CPU, CUDA, MPS) to ensure compatibility.
*   **Data Preparation**: Scripts to prepare datasets for fine-tuning:
    *   **Shakespeare**: For learning stylistic text generation.
    *   **Alpaca**: For instruction-based fine-tuning.
*   **Model Fine-Tuning**:
    *   **PEFT with LoRA**: Fine-tune `gpt2-medium` on the Shakespeare dataset using Parameter-Efficient Fine-Tuning (PEFT) with Low-Rank Adaptation (LoRA).
    *   **Supervised Fine-Tuning (SFT)**: Fine-tune `gpt2-medium` on the Alpaca dataset using the TRL library.
*   **Evaluation and Inference**:
    *   Evaluate the fine-tuned models.
    *   Examples of prompt engineering to compare base and fine-tuned models.

## How to Use

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

### 3. Data Preparation

#### Shakespeare Dataset

The `prepare_shakespeare.py` script downloads the "tiny_shakespeare" dataset, tokenizes it using the "gpt2-medium" tokenizer, and saves the processed dataset to the `shakespeare_prepared/` directory.

```bash
python prepare_shakespeare.py
```

#### Alpaca Dataset

The `prepare_alpaca.py` script downloads and processes the Alpaca dataset, saving it to the `alpaca_prepared/` directory.

```bash
python prepare_alpaca.py
```

### 4. Fine-Tuning

#### Fine-Tuning on Shakespeare with LoRA

The `train-gpt2.py` script fine-tunes the `gpt2-medium` model on the prepared Shakespeare dataset using LoRA.

```bash
python train-gpt2.py
```

The fine-tuned model adapter will be saved in the `gpt2-lora-shakespeare/` directory.

#### Fine-Tuning on Alpaca with SFT

The `sft-train.py` script fine-tunes the `gpt2-medium` model on the Alpaca dataset using Supervised Fine-Tuning (SFT) from the TRL library.

```bash
python sft-train.py
```

The final model will be saved in the `alpaca-sft-final/` directory.

### 5. Evaluation and Inference

#### Evaluate Shakespeare Model

To generate text with the fine-tuned Shakespeare model, run:

```bash
python evaluate_shakespeare.py
```

#### Prompt Engineering Example

The `prompt_engineering.py` script demonstrates how to use the fine-tuned model and compares its output to the base model.

```bash
python prompt_engineering.py
```
```