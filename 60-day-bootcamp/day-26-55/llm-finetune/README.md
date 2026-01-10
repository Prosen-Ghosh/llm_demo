[<- Back to Main README](../../../README.md)

# LLM Finetuning Project

This project provides a comprehensive guide to fine-tuning Large Language Models (LLMs) using various techniques and datasets. It covers data preparation, model training (including parameter-efficient methods), and evaluation.

## Table of Contents

- [LLM Finetuning Project](#llm-finetuning-project)
  - [Project Structure](#project-structure)
  - [Features](#features)
  - [Prerequisites](#prerequisites)
  - [How to Use](#how-to-use)
    - [1. Setup](#1-setup)
    - [2. Verify Hardware](#2-verify-hardware)
    - [3. Data Preparation](#3-data-preparation)
      - [Shakespeare Dataset](#shakespeare-dataset)
      - [Alpaca Dataset](#alpaca-dataset)
    - [4. Fine-Tuning](#4-fine-tuning)
      - [Fine-Tuning on Shakespeare with LoRA](#fine-tuning-on-shakespeare-with-lora)
      - [Fine-Tuning on Alpaca with SFT](#fine-tuning-on-alpaca-with-sft)
    - [5. Evaluation and Inference](#5-evaluation-and-inference)
      - [Evaluate Shakespeare Model](#evaluate-shakespeare-model)
      - [Prompt Engineering Example](#prompt-engineering-example)

## Project Structure
```
.
├── alpaca-sft-final/       # Directory for the final Alpaca SFT model.
├── alpaca_prepared/        # Directory for the prepared Alpaca dataset.
├── data/                   # General directory for datasets.
├── gpt2-lora-shakespeare/  # Directory for the GPT2 LoRA Shakespeare model.
├── gpt2-shakespeare-finetuned/ # Directory for the GPT2 Shakespeare finetuned model.
├── shakespeare_prepared/   # Directory for the prepared Shakespeare dataset.
├── exercise/               # Directory for exercises or supplementary materials.
├── .gitignore              # Specifies intentionally untracked files to ignore.
├── chat_instruction_uning.py # Script for chat instruction tuning.
├── evaluate_shakespeare.py # Script to evaluate the Shakespeare model.
├── load_shakespeare.py     # Script to load the Shakespeare dataset.
├── prepare_alpaca.py       # Script to prepare the Alpaca dataset.
├── prepare_shakespeare.py  # Script to prepare the Shakespeare dataset.
├── prompt_engineering.py   # Script demonstrating prompt engineering.
├── README.md               # This README file.
├── requirements.txt        # Lists all Python dependencies.
├── sft-train.py            # Script for Supervised Fine-Tuning (SFT).
├── train-gpt2.py           # Script to fine-tune GPT2.
└── verify_hardware.py      # Script to verify hardware compatibility.
```

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

## Prerequisites

- Python 3.8 or higher
- `pip` for package installation

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