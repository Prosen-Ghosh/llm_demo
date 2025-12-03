# Asynchronous LLM Orchestrator

This project implements an asynchronous LLM (Large Language Model) orchestrator service using FastAPI. It is designed to efficiently process multiple LLM requests in a batch, abstracting away different LLM providers and adding features like rate limiting, retry mechanisms, and detailed response metrics.

## Table of Contents

- [Features](#features)
- [Purpose](#purpose)
- [Core Concepts & Architecture](#core-concepts--architecture)
- [Project Structure](#project-structure)
- [Supported LLM Providers](#supported-llm-providers)
- [API Documentation](#api-documentation)
  - [Health Check (`GET /health`)](#health-check-get-health)
  - [Batch LLM Request (`POST /batch`)](#batch-llm-request-post-batch)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Environment Variables](#environment-variables)
  - [Running with Docker Compose](#running-with-docker-compose)
  - [Running Locally for Development](#running-locally-for-development)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [Future Improvements](#future-improvements)

## Features

*   **Asynchronous Batch Processing**: Efficiently handles multiple LLM requests concurrently.
*   **Provider Abstraction**: Unified API for interacting with different LLM providers (e.g., OpenRouter, Ollama).
*   **Rate Limiting**: Configurable semaphore to control concurrent requests to LLM providers, preventing API overuse.
*   **Retry Mechanism**: Automatic retries with exponential backoff for transient errors (timeouts, rate limits).
*   **Detailed Response Metrics**: Provides latency, token usage, and success/failure counts for each request and batch.
*   **Pydantic Models**: Robust request and response validation and serialization.
*   **Containerized Deployment**: Ready for Docker and Docker Compose deployment.
*   **Health Checks**: Integrated health check endpoint for monitoring.

## Purpose

The main purpose of this project is to provide a scalable and resilient service that can handle a high volume of LLM requests. It aims to simplify the process of interacting with various LLM providers by offering a single, unified API. This is particularly useful for applications that need to leverage multiple models from different providers without implementing custom logic for each one.

## Core Concepts & Architecture

The project is built around the `LLMOrchestrator` located in `app/core/orchestrator.py`. This class is responsible for:

1.  **Initializing Providers**: Based on environment variables, it initializes instances of `LLMProviderBase` subclasses (e.g., `OpenRouterProvider`, `OllamaProvider`).
2.  **Managing Concurrency**: Uses `asyncio.Semaphore` to limit the number of concurrent requests sent to external LLM APIs.
3.  **Executing Requests**: For each `LLMRequest` in a `BatchLLMRequest`, it selects the appropriate provider and executes the request, applying retry logic and error handling.
4.  **Aggregating Responses**: Collects individual `LLMResponse` objects into a `BatchLLMResponse`, including overall batch metrics.

Each LLM provider (`app/providers/*.py`) inherits from `LLMProviderBase` and implements the `_make_request` method, which handles the specific API calls and response parsing for that provider.

The API endpoints are defined using FastAPI in `app/routers/`.

## Project Structure

```
.
├── .env
├── .env.example
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── README.md
├── requirements.txt
├── app/
│   ├── __init__.py
│   ├── main.py                     # FastAPI application entry point
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py               # Application settings and configuration
│   │   └── orchestrator.py         # Core LLM orchestration logic
│   ├── models/
│   │   ├── __init__.py
│   │   └── models.py               # Pydantic models for requests and responses
│   ├── providers/
│   │   ├── __init__.py
│   │   ├── base.py                 # Abstract base class for LLM providers
│   │   ├── ollama.py               # Ollama LLM provider implementation
│   │   └── openrouter.py           # OpenRouter LLM provider implementation
│   └── routers/
│       ├── __init__.py
│       ├── batch.py                # API router for batch LLM requests
│       ├── dependencies.py         # FastAPI dependency injection utilities
│       └── health.py               # API router for health checks
└── logs/
```

## Supported LLM Providers

*   **OpenRouter**: A unified API for various LLMs. Requires `OPENROUTER_API_KEY`.
*   **Ollama**: For running LLMs locally. Requires `OLLAMA_API_KEY`.

## API Documentation

The API uses standard HTTP methods and JSON payloads.

### Health Check (`GET /health`)

A simple endpoint to check the service's operational status.

**Endpoint:** `GET /health`

**Response:**
```json
{
  "status": "ok"
}
```

### Batch LLM Request (`POST /batch`)

Processes a batch of LLM requests concurrently.

**Endpoint:** `POST /batch`

**Request Body (`BatchLLMRequest`):**

A list of `LLMRequest` objects.

| Field          | Type                     | Description                                                                                                                                                                                                            |
| :------------- | :----------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `requests`     | `List[LLMRequest]`       | A list of individual LLM requests. Maximum 100 requests per batch. Each `LLMRequest` can optionally have a unique `request_id`.                                                                                        |

**`LLMRequest` Fields:**

| Field          | Type                     | Description                                                                                                                                                                                                            |
| :------------- | :----------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `provider`     | `Enum[openrouter, ollama]` | The LLM provider to use (e.g., `"openrouter"`, `"ollama"`).                                                                                                                                                            |
| `model`        | `str`                    | The specific model to use (e.g., `"google/gemma-3-27b-it:free"` for OpenRouter, `"deepseek-r1:8b"` for Ollama). Model name is case-insensitive.                                                                       |
| `messages`     | `List[Message]`          | A list of message objects for the chat completion. Must contain at least one message.                                                                                                                                  |
| `temperature`  | `float`                  | Controls randomness. Lower values are more deterministic. Range: `0.0` to `2.0`. Default: `0.7`.                                                                                                                       |
| `max_tokens`   | `int`                    | The maximum number of tokens to generate in the completion. Range: `1` to `32000`. Default: `1000`.                                                                                                                   |
| `request_id`   | `Optional[str]`          | An optional unique identifier for the request. If provided, must be unique within the batch.                                                                                                                           |

**`Message` Fields:**

| Field          | Type                     | Description                                                                                                                                                                                                            |
| :------------- | :----------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `role`         | `Enum[system, user, assistant]` | The role of the message sender.                                                                                                                                                                                        |
| `content`      | `str`                    | The content of the message. Cannot be empty or whitespace only. Maximum 50000 characters.                                                                                                                              |

**Example Request:**
```json
{
  "requests": [
    {
      "request_id": "req-1",
      "provider": "openrouter",
      "model": "google/gemma-3-27b-it:free",
      "messages": [
        { "role": "user", "content": "Tell me a short story about a cat." }
      ],
      "temperature": 0.5,
      "max_tokens": 150
    },
    {
      "request_id": "req-2",
      "provider": "ollama",
      "model": "deepseek-r1:8b",
      "messages": [
        { "role": "system", "content": "You are a helpful assistant." },
        { "role": "user", "content": "Explain the concept of quantum entanglement in simple terms." }
      ],
      "temperature": 0.7,
      "max_tokens": 200
    }
  ]
}
```

**Response Body (`BatchLLMResponse`):**

Contains a list of `LLMResponse` objects and overall batch statistics.

| Field                | Type                | Description                                                                  |
| :------------------- | :------------------ | :--------------------------------------------------------------------------- |
| `responses`          | `List[LLMResponse]` | A list of responses for each individual LLM request in the batch.            |
| `total_requests`     | `int`               | Total number of requests in the batch.                                       |
| `successful`         | `int`               | Number of successfully processed requests.                                   |
| `failed`             | `int`               | Number of failed requests.                                                   |
| `total_latency_ms`   | `float`             | Total time taken to process the entire batch (in milliseconds).              |
| `average_latency_ms` | `float`             | Average latency per request in the batch (in milliseconds).                  |

**`LLMResponse` Fields:**

| Field            | Type        | Description                                                              |
| :--------------- | :---------- | :----------------------------------------------------------------------- |
| `request_id`     | `Optional[str]` | The ID of the original request, if provided.                             |
| `provider`       | `str`       | The LLM provider used for this request.                                  |
| `model`          | `str`       | The model used for this request.                                         |
| `content`        | `str`       | The generated text content from the LLM. Empty if an error occurred.     |
| `prompt_tokens`  | `int`       | Number of tokens in the input prompt.                                    |
| `completion_tokens` | `int`       | Number of tokens in the generated completion.                            |
| `total_tokens`   | `int`       | Total tokens (prompt + completion).                                      |
| `latency_ms`     | `float`     | Latency for this specific request (in milliseconds).                     |
| `timestamp`      | `datetime`  | UTC timestamp of when the response was generated.                        |
| `error`          | `Optional[str]` | Error message if the request failed, otherwise `null`.                   |

**Example Response:**
```json
{
  "responses": [
    {
      "request_id": "req-1",
      "provider": "openrouter",
      "model": "google/gemma-3-27b-it:free",
      "content": "Whiskers, a tabby of great renown...",
      "prompt_tokens": 15,
      "completion_tokens": 80,
      "total_tokens": 95,
      "latency_ms": 345.67,
      "timestamp": "2023-10-27T10:00:00.123456",
      "error": null
    },
    {
      "request_id": "req-2",
      "provider": "ollama",
      "model": "deepseek-r1:8b",
      "content": "Quantum entanglement is a phenomenon...",
      "prompt_tokens": 20,
      "completion_tokens": 120,
      "total_tokens": 140,
      "latency_ms": 567.89,
      "timestamp": "2023-10-27T10:00:00.987654",
      "error": null
    }
  ],
  "total_requests": 2,
  "successful": 2,
  "failed": 0,
  "total_latency_ms": 913.56,
  "average_latency_ms": 456.78
}
```

## Getting Started

### Prerequisites

*   Python 3.12+
*   Docker and Docker Compose (if running via Docker)

### Environment Variables

Create a `.env` file in the project root based on `.env.example`.

```dotenv
# API Keys (Get from OpenRouter or direct providers)
OLLAMA_API_KEY=your_ollama_api_key_here
OPENROUTER_API_KEY=your_openrouter_api_key_here

# Service Configuration
MAX_CONCURRENT_REQUESTS=10
REQUEST_TIMEOUT=30
MAX_RETRIES=3
LOG_LEVEL=INFO
```

**Note:** For OpenRouter, you might also need to set `HTTP-Referer` in your environment (or within the `OpenRouterProvider` code if you change `http://localhost:8000`). The current setup assumes the orchestrator will be accessed from `http://localhost:8000` when running OpenRouter.

### Running with Docker Compose

1.  **Build and Run**:
    ```bash
    docker-compose up --build
    ```
2.  **Verify**: The service should be running on `http://localhost:8000`. You can check the health:
    ```bash
    curl http://localhost:8000/health
    ```
    Expected output: `{"status":"ok"}`

### Running Locally for Development

For local development, you can use the `fastapi dev` command, which provides a convenient way to run your application with auto-reloading. Alternatively, you can use `uvicorn` directly.

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
2.  **Set Environment Variables**: Ensure your `.env` file is configured or set environment variables directly.
3.  **Run the Application (Recommended for Development)**:
    ```bash
    fastapi dev app/main.py
    ```
    This command starts the development server, automatically reloading it on code changes. By default, it runs on `http://127.0.0.1:8000`. You can specify a host and port if needed (e.g., `fastapi dev app/main.py --host 0.0.0.0 --port 8001`).

4.  **Run the Application (Using Uvicorn Directly)**:
    ```bash
    uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    ```
    This command starts the Uvicorn server, which runs the FastAPI application.
    *   `app.main:app`: Specifies that the FastAPI application instance named `app` is found within the `main.py` file inside the `app` directory.
    *   `--host 0.0.0.0`: Makes the server accessible externally (useful in Docker or network environments).
    *   `--port 8000`: Sets the port the server listens on to 8000.
    *   `--reload`: Enables auto-reloading of the server when code changes are detected, which is very useful for local development.

5.  **Access API Docs**: Once running, you can access the interactive API documentation (Swagger UI) at `http://localhost:10000/docs` (or the port you specified).

## Deployment

This application is containerized using Docker, which makes it easy to deploy to any cloud provider that supports Docker containers. Here are the general steps to deploy this application:

1. **Build the Docker image:**
   ```bash
   docker build -t async-llm-orchestrator .
   ```

2. **Push the Docker image to a container registry:**
   ```bash
   docker push your-container-registry/async-llm-orchestrator
   ```

3. **Configure the environment variables in your cloud provider's environment.**

4. **Deploy the container.**

For more detailed instructions, please refer to your cloud provider's documentation.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue if you have any suggestions or find any bugs.

## Future Improvements

*   Add support for more LLM providers.
*   Implement a more sophisticated caching mechanism to reduce redundant API calls.
*   Add more detailed logging and tracing for better observability.
*   Implement user authentication and authorization.

