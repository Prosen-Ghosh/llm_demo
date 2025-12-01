# LLM Proxy

This project is intended to serve as a proxy for Large Language Models (LLMs), providing a centralized and configurable interface for routing requests to various LLM providers. It is built using FastAPI and designed to handle features like request routing, load balancing, API key management, and potentially caching.

## Features (Intended)

*   **Unified Endpoint**: Provide a single API endpoint for interacting with multiple LLM providers.
*   **Provider Abstraction**: Abstract away the specifics of different LLM APIs, allowing for easy switching between providers.
*   **Concurrency Control**: Manage and limit the number of concurrent requests to upstream LLM APIs to prevent rate limiting or overloading.
*   **Retry Mechanisms**: Implement automatic retries with exponential backoff for transient errors from upstream LLM providers.
*   **Environment-based Configuration**: Easily configure upstream providers, API keys, and other settings via environment variables.

## Getting Started

To get this LLM Proxy running, follow these steps:

### Prerequisites

*   Python 3.12+
*   `pip` for dependency management.
*   (Optional) Docker and Docker Compose for containerized deployment.

### 1. Setup Environment Variables

Copy the example environment file and populate it with your specific configurations and API keys.

```bash
cp .env.example .env
```

Edit the `.env` file and replace placeholders like `replace_me_with_real_key` with actual values for the LLM providers you intend to use.

### 2. Install Dependencies

It is recommended to use a virtual environment.

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
```

### 3. Run the Application

#### Locally with Uvicorn

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

This will start the FastAPI application, typically accessible at `http://localhost:8000`. The `--reload` flag enables live reloading during development.

#### With Docker Compose

If you have Docker and Docker Compose installed, you can build and run the service using:

```bash
docker-compose up --build
```

This will containerize the application and start it, usually mapping to `http://localhost:8000` on your host machine.

## API Endpoints (Planned)

The specific API endpoints will depend on the implemented LLM integration. Typically, a proxy would expose endpoints for:

*   **Health Check**: `GET /health` to verify the service is running.
*   **Chat Completions**: `POST /chat/completions` to send requests to LLMs and receive responses.
*   **Embeddings**: `POST /embeddings` for generating text embeddings.

Please refer to the source code (`app/main.py` and related router files) for the exact implemented endpoints and their request/response schemas.

## Project Structure

```
.
├── .env.example              # Example environment variables
├── docker-compose.yml        # Docker Compose configuration
├── dockerfile                # Dockerfile for containerization
├── requirements.txt          # Python dependencies
└── app/
    ├── __init__.py           # Python package initializer
    └── main.py               # FastAPI application entry point
```
