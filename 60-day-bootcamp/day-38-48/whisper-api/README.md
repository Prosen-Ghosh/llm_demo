# Whisper API

This project provides a high-performance, CPU-based Speech-to-Text API using the `faster-whisper` library and FastAPI. It is designed for efficient transcription of audio files.

## Table of Contents

- [Features](#features)
- [Recent Changes](#recent-changes)
- [Configuration](#configuration)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
  - [API Endpoints](#api-endpoints)
- [Running Tests](#running-tests)
- [Project Structure](#project-structure)

## Features

- **Fast and Efficient:** Built on `faster-whisper`, a reimplementation of OpenAI's Whisper model that is up to 4 times faster.
- **CPU-Optimized:** Runs efficiently on CPU, making it accessible without specialized hardware.
- **Easy to Deploy:** Containerized with Docker for simple setup and deployment.
- **Transcription Endpoint:** A `/transcribe` endpoint to upload audio files and get transcriptions.
- **Health Check:** Includes a `/health` endpoint for monitoring service status and model information.
- **Model Switching:** Ability to switch between different Whisper models at runtime.
- **Audio Normalization:** Automatically normalizes audio for better transcription accuracy.

## Recent Changes

*   **Dockerfile:**
    *   Added `ffmpeg` to the Docker image.

*   **`app/config.py`:**
    *   Renamed `WHISPER_MODEL_SIZE` to `DEFAULT_MODEL_SIZE`.
    *   Added `ALLOWED_MODELS` to specify a list of allowed models.
    *   Increased `CPU_THREADS` to 2.
    *   Added `NUMBER_OF_WORKERS` with a value of 4.

*   **`app/main.py`:**
    *   Added `Query` to the imports.
    *   Imported `check_model_suitability` and `normalize_audio`.
    *   The `/` endpoint now returns the `DEFAULT_MODEL_SIZE` instead of `WHISPER_MODEL_SIZE`.
    *   The `/transcribe` endpoint now accepts a `language` parameter.
    *   The `/transcribe` endpoint now normalizes the audio before transcription.
    *   The `/transcribe` endpoint now checks for model suitability based on the language.
    *   The `/transcribe` endpoint now includes more information in the response, such as `model_used`, `language_probability`, and an optional `system_warning`.
    *   The `/transcribe` endpoint now deletes the processed file after transcription.
    *   Removed the `/test-transcribe` endpoint.
    *   Added a new `/system/model` endpoint to switch the model at runtime.

*   **`app/utils.py`:**
    *   Added `.ogg` to the list of `SUPPORTED_EXTENSIONS`.
    *   Added `LANGUAGE_MODEL_REQUIREMENTS` to define recommended models for different languages.
    *   Added `check_model_suitability` function to check if the current model is suitable for the given language.

*   **`app/whisper.py`:**
    *   Imported `gc`.
    *   The `load_model` method now accepts a `model_size` parameter to switch models.
    *   The `load_model` method now unloads the previous model before loading a new one.
    *   The `transcribe_file` method now accepts a `language` parameter.
    *   The `transcribe_file` method now uses more advanced transcription options like `beam_size`, `best_of`, `temperature`, `vad_filter`, and `patience`.
    *   The `transcribe_file` method now returns the `model_used` in the result.

*   **`requirements.txt`:**
    *   Added `ffmpeg-python`.

## Configuration

The following environment variables can be set to configure the application:

| Variable | Description | Default |
| --- | --- | --- |
| `DEFAULT_MODEL_SIZE` | The size of the Whisper model to use. | `large-v3` |
| `ALLOWED_MODELS` | A list of allowed models. | `["tiny", "base", "small", "medium", "large-v2", "large-v3"]` |
| `DEVICE` | The device to run the model on (`cpu` or `cuda`). | `cpu` |
| `COMPUTE_TYPE` | The compute type for the model. | `int8_float32` |
| `CPU_THREADS` | The number of CPU threads to use. | `2` |
| `NUMBER_OF_WORKERS` | The number of workers to use for transcription. | `4` |
| `MODEL_CACHE_DIR` | The directory to cache the model in. | `/root/.cache/huggingface` |


## Getting Started

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd whisper-api
    ```

2.  **Build and run the container:**
    ```bash
    docker-compose up -d --build
    ```
    The API will be available at `http://localhost:8000`.

## Usage

**Note:** The default transcription language is set to English (`en`). You can specify the language using the `language` query parameter in the `/transcribe` endpoint.

### API Endpoints

- **`GET /`**
  - **Description:** Returns a welcome message.
  - **Response:**
    ```json
    {
      "message": "Welcome to Whisper API v1.0.0"
    }
    ```

- **`GET /health`**
  - **Description:** Provides a health check of the API.
  - **Response:**
    ```json
    {
      "status": "healthy",
      "version": "1.0.0",
      "uptime_seconds": 123.45,
      "cpu_cores_available": 8,
      "model_loaded": true,
      "model_size": "large-v3",
      "cpu_threads": 2
    }
    ```

- **`PUT /system/model`**
  - **Description:** Switch the Whisper model at runtime.
  - **Request Body:**
    ```json
    {
        "model_size": "base"
    }
    ```
  - **Response:**
    ```json
    {
        "status": "success",
        "current_model": "base"
    }
    ```

- **`POST /transcribe`**
  - **Description:** Transcribes an uploaded audio file.
  - **Query Parameters:**
    *   `language` (optional, default: `en`): The language of the audio file.
  - **Request:** `multipart/form-data` with a `file` field containing the audio file.
  - **Example:**
    ```bash
    curl -X POST "http://localhost:8000/transcribe?language=bn" -F "file=@/path/to/your/audio.wav"
    ```
  - **Response:**
    ```json
    {
        "filename": "audio.wav",
        "model": "large-v3",
        "language": "bn",
        "duration": 10.0,
        "language_probability": 0.99,
        "text": "আপনার অডিও ফাইলের প্রতিলিপি এখানে থাকবে।",
        "segments": [
            {
                "start": 0.0,
                "end": 5.0,
                "text": "আপনার অডিও ফাইলের প্রতিলিপি"
            },
            {
                "start": 5.0,
                "end": 10.0,
                "text": "এখানে থাকবে।"
            }
        ]
    }
    ```

## Running Tests

To run the tests, execute the following command:

```bash
docker-compose exec whisper-api pytest
```

## Project Structure

```
.
├── app
│   ├── config.py
│   ├── main.py
│   ├── preprocessing.py
│   ├── test_main.py
│   ├── utils.py
│   └── whisper.py
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```
