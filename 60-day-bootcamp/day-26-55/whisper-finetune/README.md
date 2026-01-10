[<- Back to Main README](../../../README.md)

# Whisper Fine-Tuning for Bengali Speech-to-Text

This project fine-tunes the OpenAI Whisper model for Bengali speech-to-text transcription using the Mozilla Common Voice dataset. It is built to run on local machines (including Apple Silicon with MPS) and is also containerized with Docker for portability.

## Table of Contents

- [Project Overview](#project-overview)
- [Prerequisites](#prerequisites)
- [Setup and Installation](#setup-and-installation)
- [Usage](#usage)
- [Docker Usage](#docker-usage)
- [Monitoring with TensorBoard](#monitoring-with-tensorboard)
- [Project Structure](#project-structure)
- [Future Improvements](#future-improvements)
- [Contributing](#contributing)

## Project Overview

The core of this project is the `train.py` script, which performs the following steps:

1.  **Loads Data**: Fetches the Bengali speech dataset from `arifulFarhad/mozilla-bangla-dataset` on Hugging Face.
2.  **Preprocesses Data**: Initializes the Whisper feature extractor and tokenizer, and processes the audio and text data for training.
3.  **Loads Model**: Loads the pre-trained `openai/whisper-medium` model.
4.  **Trains**: Fine-tunes the model on the Bengali dataset using the `Seq2SeqTrainer` from the `transformers` library.
5.  **Evaluates**: Monitors training progress using Word Error Rate (WER) and saves the best model.
6.  **Logs**: Logs training metrics to TensorBoard for visualization.

## Prerequisites

*   Python 3.8+
*   Pip (Python package installer)
*   Docker (if you plan to use Docker for training)

## Setup and Installation

1.  **Install dependencies:**
    It is recommended to use a virtual environment.
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

## Usage

To start the training process, run the `train.py` script:

```bash
python3 train.py
```

The script will automatically detect and use an available MPS device (for Apple Silicon) or fall back to the CPU.

The final trained model will be saved in the `final_model` directory.

## Docker Usage

This project is fully containerized, allowing you to run the training in an isolated environment.

1.  **Build the Docker image:**
    ```bash
    docker-compose build
    ```

2.  **Run the training:**
    ```bash
    docker-compose up
    ```

This will start the training process inside a Docker container.

## Monitoring with TensorBoard

Training progress and metrics are logged to TensorBoard.

1.  **Start TensorBoard:**
    The training script saves TensorBoard logs to the `output/` directory. To view them, run:
    ```bash
    tensorboard --logdir=output
    ```

2.  Open your browser and navigate to `http://localhost:6006` to view the training dashboards.

## Project Structure

```
.
├── . dockerignore          # Specifies files and directories to exclude from the Docker build context.
├── .gitignore              # Specifies intentionally untracked files to ignore.
├── docker-compose.yml      # Docker Compose configuration for multi-container Docker applications.
├── Dockerfile              # Defines how to build the Docker image for the application.
├── linkedin.md             # LinkedIn article related to the project.
├── README.md               # This README file.
├── requirements.txt        # Lists all Python dependencies.
├── train.py                # Main script for fine-tuning the Whisper model.
├── data/                   # Directory for storing dataset-related files (e.g., cached data, processed data).
├── final_model/            # Directory where the final fine-tuned model will be saved.
├── huggingface_cache/      # Cache directory for Hugging Face models and datasets.
├── output/                 # Output directory for training logs and checkpoints.
└── tensorboard_logs/       # Directory for TensorBoard logs.
```

## Future Improvements

*   Experiment with different Whisper model sizes (e.g., `whisper-small`, `whisper-large`).
*   Integrate with other datasets for different languages or domains.
*   Implement more advanced evaluation metrics beyond WER.
*   Add a serving component for the fine-tuned model.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue if you have any suggestions or find any bugs.