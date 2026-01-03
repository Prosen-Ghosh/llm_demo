[<- Back to Main README](../../README.md)

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
- [Future Improvements](#future-improvements)
- [Contributing](#contributing)

## Features

- **Fast and Efficient:** Built on `faster-whisper`, a reimplementation of OpenAI's Whisper model that is up to 4 times faster.
- **CPU-Optimized:** Runs efficiently on CPU, making it accessible without specialized hardware.
- **Easy to Deploy:** Containerized with Docker for simple setup and deployment.
- **Transcription Endpoint:** A `/transcribe` endpoint to upload audio files and get transcriptions.
- **Health Check:** Includes a `/health` endpoint for monitoring service status and model information.
- **Model Switching:** Ability to switch between different Whisper models at runtime.
- **Audio Normalization:** Automatically normalizes audio for better transcription accuracy.

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
    git clone https://github.com/Prosen-Ghosh/llm_demo.git
    cd 60-day-bootcamp/day-38-48/whisper-api
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

## What's New

*   **Batch Transcription Endpoint:** A new endpoint (`/v2/batch-transcribe`) for transcribing multiple files at once.
*   **Job Status Endpoint:** A new endpoint (`/v2/jobs/{job_id}`) to check the status of transcription jobs.

## API Endpoints (V2)

- **`POST /v2/batch-transcribe`**
  - **Description:** Transcribes a batch of audio files asynchronously.
  - **Request:** `multipart/form-data` with a `files` field containing the audio files.
  - **Query Parameters:**
    *   `language` (optional, default: `en`): The language of the audio files.
  - **Example:**
    ```bash
    curl -X POST "http://localhost:8000/v2/batch-transcribe?language=en" -F "files=@/path/to/audio1.wav" -F "files=@/path/to/audio2.mp3"
    ```
  - **Response:**
    ```json
    [
        "job_id_1",
        "job_id_2"
    ]
    ```

- **`GET /v2/jobs/{job_id}`**
  - **Description:** Retrieves the status of a transcription job.
  - **Example:**
    ```bash
    curl -X GET "http://localhost:8000/v2/jobs/job_id_1"
    ```
  - **Response:**
    ```json
    {
        "job_id": "job_id_1",
        "status": "completed",
        "result": {
            "text": "The transcribed text of the audio.",
            "segments": [
                {
                    "start": 0.0,
                    "end": 5.0,
                    "text": "The transcribed text"
                }
            ],
            "language": "en"
        }
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

## Future Improvements
*   Add support for more output formats (e.g., SRT, VTT).
*   Implement a webhook system to notify clients when a transcription job is complete.
*   Add a user interface for uploading files and viewing transcriptions.

## Contributing
Contributions are welcome! Please feel free to submit a pull request or open an issue if you have any suggestions or find any bugs.
```
