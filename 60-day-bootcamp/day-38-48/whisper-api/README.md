# Whisper API

This project provides a high-performance, CPU-based Speech-to-Text API using the `faster-whisper` library and FastAPI. It is designed for efficient transcription of audio files.

## Table of Contents

- [Features](#features)
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

## Configuration

The following environment variables can be set to configure the application:

| Variable             | Description                                     | Default |
| -------------------- | ----------------------------------------------- | ------- |
| `WHISPER_MODEL_SIZE` | The size of the Whisper model to use.           | `large-v3`  |
| `DEVICE`             | The device to run the model on (`cpu` or `cuda`). | `cpu`   |
| `COMPUTE_TYPE`       | The compute type for the model.                 | `int8_float32`  |
| `CPU_THREADS`        | The number of CPU threads to use.               | `1`     |
| `MODEL_CACHE_DIR`    | The directory to cache the model in.            | `/root/.cache/huggingface` |


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

**Note:** The default transcription language is set to Bengali (`bn`).

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
      "cpu_threads": 1
    }
    ```

- **`POST /test-transcribe`**
  - **Description:** Performs a test transcription of a dummy audio file. This endpoint is useful for a quick check to see if the model is loaded and working.
  - **Response:**
    ```json
    {
        "status": "success",
        "processing_time": 0.123,
        "result": {
            "language": "bn",
            "language_probability": 0.99,
            "duration": 1.0,
            "text": "হ্যালো বিশ্ব।",
            "segments": [
                {
                    "start": 0.0,
                    "end": 1.0,
                    "text": "হ্যালো বিশ্ব।"
                }
            ]
        }
    }
    ```

- **`POST /transcribe`**
  - **Description:** Transcribes an uploaded audio file.
  - **Request:** `multipart/form-data` with a `file` field containing the audio file.
  - **Example:**
    ```bash
    curl -X POST "http://localhost:8000/transcribe" -F "file=@/path/to/your/audio.wav"
    ```
  - **Response:**
    ```json
    {
        "filename": "audio.wav",
        "language": "bn",
        "duration": 10.0,
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
│   ├── test_main.py
│   └── whisper.py
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```
