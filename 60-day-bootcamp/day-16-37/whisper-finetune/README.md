# Whisper Fine-Tuning for Bengali Speech-to-Text

This project fine-tunes the OpenAI Whisper model for Bengali speech-to-text transcription using the Mozilla Common Voice dataset. It is built to run on local machines (including Apple Silicon with MPS) and is also containerized with Docker for portability.

## Project Overview

The core of this project is the `train.py` script, which performs the following steps:

1.  **Loads Data**: Fetches the Bengali speech dataset from `arifulFarhad/mozilla-bangla-dataset` on Hugging Face.
2.  **Preprocesses Data**: Initializes the Whisper feature extractor and tokenizer, and processes the audio and text data for training.
3.  **Loads Model**: Loads the pre-trained `openai/whisper-medium` model.
4.  **Trains**: Fine-tunes the model on the Bengali dataset using the `Seq2SeqTrainer` from the `transformers` library.
5.  **Evaluates**: Monitors training progress using Word Error Rate (WER) and saves the best model.
6.  **Logs**: Logs training metrics to TensorBoard for visualization.

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd whisper-finetune
    ```

2.  **Install dependencies:**
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

The final trained model will be saved in the `./whisper-medium-bn-final` directory.

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
    ```bash
    tensorboard --logdir=output/runs
    ```

2.  Open your browser and navigate to `http://localhost:6006` to view the training dashboards.

