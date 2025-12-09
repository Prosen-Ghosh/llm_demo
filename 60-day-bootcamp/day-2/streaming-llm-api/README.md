# Demo: A Production-Ready Streaming LLM API

This project is a demonstration of a production-ready API gateway for interacting with Large Language Models (LLMs). It showcases production-grade features and best practices, acting as a central hub to connect your applications to various LLM providers like Ollama and OpenRouter. It offers essential features for scalability, monitoring, and cost management. Whether you're building a chatbot, a content generation tool, or any other AI-powered application, this project provides a robust architectural foundation.

## Table of Contents

- [Why is this project required?](#why-is-this-project-required)
- [Features](#features)
- [Project Structure](#project-structure)
- [API Documentation](#api-documentation)
  - [Authentication](#authentication)
  - [Endpoints](#endpoints)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Local Development](#local-development)
  - [Using Docker](#using-docker)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [Future Improvements](#future-improvements)


## Why is this project required?

Building a scalable and reliable application on top of LLMs presents several challenges. This project is designed to address them:

*   **Simplified Integration:** Instead of writing separate integrations for each LLM provider, you can use a single, unified API. This dramatically reduces complexity and development time.
*   **Centralized Control & Monitoring:** Gain a single pane of glass for monitoring usage, tracking costs, and enforcing policies across all LLM providers and applications.
*   **Cost Management:** With built-in cost tracking and estimation, you can keep a close eye on your expenses and avoid surprises on your bill.
*   **Enhanced Performance & User Experience:** Support for streaming responses ensures that your users get real-time feedback from the LLM, which is critical for interactive applications.
*   **Resource Efficiency:** Automatic cancellation of requests when a client disconnects prevents wasted resources on the server and with the LLM provider.
*   **Future-Proof Your Application:** The modular provider system makes it easy to adopt new models and providers as they become available, without requiring a major overhaul of your application.

## Features

This project comes with a range of features designed for a production environment:

*   **Unified API for Multiple Providers:** A single, consistent API endpoint for chat completions, regardless of the backend LLM provider (e.g., Ollama, OpenRouter).
*   **Streaming with Server-Sent Events (SSE):** For real-time, interactive applications, the `/v1/chat/stream` endpoint provides a seamless streaming experience.
*   **Automatic Request Cancellation:** If a client disconnects from a streaming request, the connection to the LLM provider is automatically terminated. This saves computational resources and costs.
*   **Usage and Cost Tracking:** The API monitors the number of requests, prompt tokens, and completion tokens for each API key. It also provides a cost estimate in USD.
*   **Rate Limiting:** Protect your API from abuse and control costs with a configurable, per-API-key rate limiter.
*   **Modular Provider System:** The project is designed to be easily extensible. Adding a new LLM provider is as simple as creating a new class that inherits from a common base and implementing the required methods.
*   **Configuration via Environment Variables:** All settings, including API keys and provider configurations, are managed through a `.env` file for easy setup and deployment.

## Project Structure

The project is organized as follows:

```
.
├── .env.example
├── .gitignore
├── docker-compose.dev.yml
├── docker-compose.yml
├── Dockerfile
├── README.md
├── requirements.txt
└── app/
    ├── __init__.py
    ├── main.py
    ├── api/
    │   ├── __init__.py
    │   ├── deps.py
    │   └── v1/
    │       ├── __init__.py
    │       ├── router.py
    │       └── endpoints/
    │           ├── __init__.py
    │           ├── chat.py
    │           ├── health.py
    │           └── usage.py
    ├── core/
    │   ├── __init__.py
    │   ├── config.py
    │   └── dependencies.py
    ├── models/
    │   ├── __init__.py
    │   ├── chat.py
    │   └── usage.py
    ├── providers/
    │   ├── __init__.py
    │   ├── base.py
    │   ├── ollama.py
    │   └── openrouter.py
    └── services/
        ├── __init__.py
        ├── cost_tracker.py
        └── provider_manager.py
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
*   **Description:** Sends a prompt to the LLM and receives a stream of events as the response is generated. If the client disconnects, the request is automatically cancelled.
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

#### Get Usage Statistics

*   **Endpoint:** `GET /v1/usage/stats`
*   **Description:** Retrieves usage statistics for the authenticated API key.
*   **Example:**
    ```bash
    curl -X GET http://localhost:8000/v1/usage/stats \
    -H "Authorization: Bearer your-secret-api-key"
    ```

## Getting Started

### Prerequisites

- Python 3.8+
- Docker (optional)

### Local Development

1. **Clone the repository:**
   ```bash
   git clone git@github.com:Prosen-Ghosh/llm_demo.git
   cd streaming-llm-api
   ```

2. **Create a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   Create a `.env` file by copying the example:
   ```bash
   cp .env.example .env
   ```
   Now, edit the `.env` file and add your API keys and other settings. You must set `API_KEYS` to a comma-separated list of valid keys.

5. **Run the application:**
   ```bash
   uvicorn app.main:app --reload
   ```
   The API will be available at `http://localhost:8000`.

### Using Docker

1. **Set up environment variables:**
   Create a `.env` file as described in the local development section.

2. **Run with Docker Compose:**
   ```bash
   docker-compose up --build
   ```
   The API will be available at `http://localhost:8000`.

## Deployment

This application is containerized using Docker, which makes it easy to deploy to any cloud provider that supports Docker containers. Here are the general steps to deploy this application:

1. **Build the Docker image:**
   ```bash
   docker build -t streaming-llm-api .
   ```

2. **Push the Docker image to a container registry:**
   ```bash
   docker push your-container-registry/streaming-llm-api
   ```

3. **Configure the environment variables in your cloud provider's environment.**

4. **Deploy the container.**

For more detailed instructions, please refer to your cloud provider's documentation.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue if you have any suggestions or find any bugs.

## Future Improvements

This project provides a solid foundation for a production-grade LLM API, but there are several areas where it could be extended and improved:

*   **Persistent Storage for Usage Data:** The current implementation of the `CostTracker` uses in-memory storage. For a production system, this should be replaced with a persistent database like Redis or a relational database to ensure that usage data is not lost when the application restarts.
*   **More Accurate Cost-Estimation Model:** The cost estimation is currently based on a rough estimate. This could be improved by integrating with the pricing APIs of the respective LLM providers to get real-time cost information.
*   **Time-Based Usage Reporting:** The API could be enhanced to provide more granular usage reports, allowing users to view their usage data for specific time periods (e.g., daily, weekly, or monthly).
*   **Administrative Dashboard:** A web-based dashboard could be developed to provide administrators with a comprehensive overview of API usage, including the ability to view statistics for all users, manage API keys, and configure rate limits.
*   **Budget Alerts and Management:** The system could be extended to allow users to set budgets for their API usage and receive alerts when they are close to exceeding their budget.
