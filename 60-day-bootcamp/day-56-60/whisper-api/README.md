[<- Back to Main README](../../../README.md)

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
- **Versatile Transcription:** Supports a `/transcribe` endpoint for single audio files and a `/v2/batch-transcribe` for multiple files, with optional language specification.
- **Job Management:** Track batch transcription status using `/v2/jobs/{job_id}`.
- **Real-time Streaming:** A `/stream` endpoint for real-time transcription streaming.
- **Health Check:** Includes a `/health` endpoint for monitoring service status and model information.
- **Model Management:** Ability to switch between different Whisper models at runtime via `PUT /system/model`.
- **Audio Preprocessing:** Automatically normalizes audio and detects language for better transcription accuracy.
- **Configurable Processing Modes:** Choose between `ACCURATE`, `BALANCED`, and `TURBO` modes to control transcription speed and accuracy.
- **Custom Keywords:** Provide `initial_prompt` for custom keywords to guide the transcription process.
- **Detailed Metrics:** Transcription results include `inference_time` and `real_time_factor`.

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
- `make` (optional, for simplified commands)

### Installation

1.  **Build and run the container:**
    ```bash
    make up
    ```
    or
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
    *   `language` (optional, default: `auto`): The language of the audio file. Set to "auto" for automatic detection.
    *   `mode` (optional, default: `BALANCED`): Processing mode. Options: `ACCURATE`, `BALANCED`, `TURBO`.
    *   `initial_prompt` (optional): Custom keywords or phrases to guide the transcription.
  - **Request:** `multipart/form-data` with a `file` field containing the audio file.
  - **Example:**
    ```bash
    curl -X POST "http://localhost:8000/transcribe?language=bn&mode=ACCURATE&initial_prompt=Hello" -F "file=@/path/to/your/audio.wav"
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
        ],
        "inference_time": 1.23,
        "real_time_factor": 0.12
    }
    ```

- **`POST /stream`**
  - **Description:** Streams transcription results in real-time.
  - **Query Parameters:** Same as `/transcribe` endpoint.
  - **Request:** `multipart/form-data` with a `file` field containing the audio file.
  - **Example:**
    ```bash
    curl -N -X POST "http://localhost:8000/stream?language=en" -F "file=@/path/to/your/audio.wav"
    ```
  - **Response:**
    (Server-Sent Events stream of transcription segments)

## What's New

*   **Batch Transcription Endpoint:** A new endpoint (`/v2/batch-transcribe`) for transcribing multiple files at once.
*   **Job Status Endpoint:** A new endpoint (`/v2/jobs/{job_id}`) to check the status of transcription jobs.

## API Endpoints (V2)

- **`POST /v2/batch-transcribe`**
  - **Description:** Transcribes a batch of audio files asynchronously.
  - **Request:** `multipart/form-data` with a `files` field containing the audio files.
  - **Query Parameters:**
    *   `language` (optional, default: `auto`): The language of the audio files. Set to "auto" for automatic detection.
    *   `mode` (optional, default: `BALANCED`): Processing mode. Options: `ACCURATE`, `BALANCED`, `TURBO`.
    *   `initial_prompt` (optional): Custom keywords or phrases to guide the transcription.
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
            "language": "en",
            "inference_time": 1.23,
            "real_time_factor": 0.12
        }
    }
    ```

## Running Tests

To run the tests, execute the following command:

```bash
make test
```
or
```bash
docker-compose exec whisper-api pytest
```

## Project Structure

```
.
├── app/                      # Source code for the FastAPI application.
│   ├── __init__.py           # Initializes the app package.
│   ├── caching.py            # Caching utilities.
│   ├── config.py             # Configuration settings for the application.
│   ├── jobs.py               # Asynchronous job management.
│   ├── main.py               # Main FastAPI application entry point.
│   ├── monitoring.py         # Application monitoring and health checks.
│   ├── preprocessing.py      # Audio preprocessing utilities.
│   ├── test_main.py          # Unit tests for the main application logic.
│   ├── utils.py              # Utility functions.
│   ├── whisper.py            # Integration with the faster-whisper library.
│   └── worker.py             # Background worker for processing tasks.
├── tests/                    # Additional tests for the project.
├── .dockerignore             # Specifies files and directories to exclude from the Docker build context.
├── .gitignore                # Specifies intentionally untracked files to ignore.
├── CHANGELOG.md              # Project changelog.
├── docker-compose.yml        # Docker Compose configuration.
├── Dockerfile                # Dockerfile for building the application container.
├── Makefile                  # Makefile for common development tasks.
├── README.md                 # This README file.
├── requirements.txt          # Lists Python package dependencies.
└── whisper-api-arc.png       # Architectural diagram of the Whisper API.
```

## Future Improvements
*   Add support for more output formats (e.g., SRT, VTT).
*   Implement a webhook system to notify clients when a transcription job is complete.
*   Add a user interface for uploading files and viewing transcriptions.

## Contributing
Contributions are welcome! Please feel free to submit a pull request or open an issue if you have any suggestions or find any bugs.
```
