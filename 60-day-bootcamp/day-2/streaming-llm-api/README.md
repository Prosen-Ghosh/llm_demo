# Production-Grade Streaming LLM API

This project provides a production-grade RESTful API for interacting with Large Language Models (LLMs) with a focus on streaming responses, modular provider integration, and robust architecture.

## About This Project

This project implements a FastAPI application that acts as a proxy to various LLM providers like Ollama and OpenRouter. It is designed to be a "production-grade" solution, incorporating concepts such as:

*   **Dependency Injection:** FastAPI's dependency injection is used to manage services like the `ProviderManager` and for handling API key verification and rate limiting.
*   **Streaming Support:** The API provides a streaming endpoint (`/v1/chat/stream`) that uses Server-Sent Events (SSE) to send real-time responses from the LLM. This is crucial for applications like chatbots where a responsive user experience is important.
*   **Provider Abstraction:** The `providers` module uses a base class to define a common interface for all LLM providers. This makes it easy to add new providers without changing the core application logic.
*   **Configuration Management:** The application uses `pydantic-settings` to manage configuration from environment variables, allowing for easy customization of the application's behavior.
*   **Rate Limiting:** The API includes a rate-limiting feature to control the number of requests a client can make in a given time period.

## Project Structure

The project is organized as follows:

```
├── app/
│   ├── api/
│   │   ├── deps.py
│   │   └── v1/
│   │       ├── router.py
│   │       └── endpoints/
│   │           ├── chat.py
│   │           └── health.py
│   ├── core/
│   │   ├── config.py
│   │   └── dependencies.py
│   ├── models/
│   │   ├── chat.py
│   │   └── usage.py
│   ├── providers/
│   │   ├── base.py
│   │   ├── ollama.py
│   │   └── openrouter.py
│   ├── services/
│   │   └── provider_manager.py
│   └── main.py
├── .env.example
├── docker-compose.yml
├── Dockerfile
├── README.md
└── requirements.txt
```

*   `app/main.py`: The entry point of the FastAPI application.
*   `app/api/`: Contains the API-related modules, including routes and dependencies.
*   `app/core/`: Core components like configuration and dependencies.
*   `app/models/`: Pydantic models for data validation and serialization.
*   `app/providers/`: Integration with different LLM providers.
*   `app/services/`: Business logic and services.

## API Documentation

### Authentication

All API endpoints (except for the health check) require an API key. The API key should be included in the `Authorization` header as a Bearer token.

`Authorization: Bearer YOUR_API_KEY`

You can set your API key in the `.env` file (see "Running the Project" section).

### Endpoints

#### Health Check

*   **Endpoint:** `GET /v1/health`
*   **Description:** Checks the health of the application and lists the available LLM providers.
*   **Example:**
    ```bash
    curl -X GET http://localhost:8000/v1/health
    ```

#### Chat Completions (Non-streaming)

*   **Endpoint:** `POST /v1/chat/completions`
*   **Description:** Sends a prompt to the LLM and receives a complete response.
*   **Request Body:** `application/json`
    ```json
    {
      "provider": "openrouter",
      "model": "meta-llama/llama-3.2-3b-instruct:free",
      "messages": [
        {
          "role": "user",
          "content": "Hello, who are you?"
        }
      ],
      "temperature": 0.7,
      "max_tokens": 100,
      "stream": false
    }
    ```
*   **Example:**
    ```bash
    curl -X POST http://localhost:8000/v1/chat/completions \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer your-secret-api-key" \
    -d '{
      "provider": "openrouter",
      "model": "meta-llama/llama-3.2-3b-instruct:free",
      "messages": [
        {
          "role": "user",
          "content": "Tell me a joke."
        }
      ]
    }'
    ```

#### Chat Completions (Streaming)

*   **Endpoint:** `POST /v1/chat/stream`
*   **Description:** Sends a prompt to the LLM and receives a stream of events as the response is generated.
*   **Request Body:** Same as the non-streaming endpoint, but `stream` should ideally be set to `true`.
*   **Example:**
    ```bash
    curl -X POST http://localhost:8000/v1/chat/stream \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer your-secret-api-key" \
    -d '{
      "provider": "openrouter",
      "model": "meta-llama/llama-3.2-3b-instruct:free",
      "messages": [
        {
          "role": "user",
          "content": "Tell me a story about a brave knight."
        }
      ],
      "stream": true
    }'
    ```

## How to Run the Project

### Local Development

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd streaming-llm-api
    ```

2.  **Create a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables:**
    Create a `.env` file by copying the example:
    ```bash
    cp .env.example .env
    ```
    Now, edit the `.env` file and add your API keys and other settings. You must set `API_KEYS` to a comma-separated list of valid keys.

5.  **Run the application:**
    ```bash
    uvicorn app.main:app --reload
    ```
    The API will be available at `http://localhost:8000`.

### Using Docker

1.  **Set up environment variables:**
    Create a `.env` file as described in the local development section.

2.  **Run with Docker Compose:**
    ```bash
    docker-compose up --build
    ```
    The API will be available at `http://localhost:8000`.
