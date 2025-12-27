# Whisper API

This project provides a high-performance, CPU-based Speech-to-Text API using the `faster-whisper` library and FastAPI. It is designed for efficient transcription of audio files.

## Table of Contents

- [Features](#features)
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
- **Health Check:** Includes a `/health` endpoint for monitoring service status.

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

### API Endpoints

- **`GET /`**
  - **Description:** Returns a welcome message.
  - **Response:**
    ```json
    {
      "message": "Welcome to Whisper API v0.1.0"
    }
    ```

- **`GET /health`**
  - **Description:** Provides a health check of the API.
  - **Response:**
    ```json
    {
      "status": "healthy",
      "version": "0.1.0",
      "uptime_seconds": 123.45,
      "cpu_cores_available": 8
    }
    ```

- **`POST /transcribe`** (Not Yet Implemented)
  - **Description:** Transcribes an audio file.

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
│   └── test_main.py
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```
