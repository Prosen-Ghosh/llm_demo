# Function Calling Demo

This project is a FastAPI-based application that demonstrates an enterprise-grade function calling system using a Large Language Model (LLM). The application is designed to be a pluggable and extensible system, with an example implementation using Ollama. It allows the LLM to use a set of external tools, such as a calculator, weather service, and web search, to provide more accurate and context-aware responses.

## Table of Contents

- [Purpose](#purpose)
- [Features](#features)
- [Project Structure](#project-structure)
- [API Documentation](#api-documentation)
  - [GET /health](#get-health)
  - [GET /tools](#get-tools)
  - [POST /chat](#post-chat)
- [How to Run the Project](#how-to-run-the-project)
  - [Prerequisites](#prerequisites)
  - [Running Locally](#running-locally)
  - [Running with Docker](#running-with-docker)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [Future Improvements](#future-improvements)

## Purpose

The primary purpose of this demo is to showcase a robust implementation of a function-calling system. LLMs have limitations in their knowledge, which is often static and does not include real-time information. They also cannot perform external actions like calculations or accessing databases. This project addresses these limitations by providing a framework where an LLM can intelligently decide to use external tools to fulfill a user's request.

## Features

- **Function Calling:** The core feature that enables the LLM to call predefined tools to access external information or functionality.
- **Tool Registry:** A centralized and extensible registry for managing and exposing tools to the LLM.
- **Parallel Tool Execution:** The ability to execute multiple tool calls concurrently, improving performance and efficiency.
- **Configurable LLM Client:** The `LLMClient` is designed to be adaptable, allowing for integration with various LLM providers. The current implementation uses Ollama.
- **Included Tools:**
  - `calculator`: For performing mathematical calculations.
  - `weather`: To get the weather forecast for a specific location.
  - `web_search`: To search the web for real-time information.
- **FastAPI Backend:** Built on a modern, high-performance web framework for building APIs with Python.
- **Docker Support:** Includes Docker and Docker Compose configurations for easy setup, deployment, and development.
- **Hot Reloading:** A development-focused Docker setup for an improved developer experience with automatic application reloading on code changes.

## Project Structure

```
.
├── .env.example
├── .gitignore
├── docker-compose.dev.yml
├── docker-compose.yml
├── Dockerfile
├── README.md
├── requirements.txt
├── app/
│   ├── __init__.py
│   ├── main.py               # FastAPI application entry point
│   ├── api/                  # API endpoint definitions
│   │   ├── __init__.py
│   │   ├── chat.py
│   │   ├── health.py
│   │   └── tools.py
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py           # Application settings
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py          # Pydantic schemas for API requests and responses
│   ├── services/
│   │   ├── __init__.py
│   │   ├── llm_client.py       # Client for interacting with the LLM
│   │   └── tool_executor.py    # Logic for executing tools
│   ├── tools/                  # Directory for all the tools
│   │   ├── __init__.py
│   │   ├── base.py             # Base class for tools
│   │   ├── calculator.py
│   │   ├── registry.py         # Tool registry
│   │   ├── weather.py
│   │   └── web_search.py
│   └── utils/
│       ├── __init__.py
│       └── logger.py           # Logging configuration
└── logs/
```

## API Documentation

### GET /health

Checks the health of the application and lists the number of registered tools.

- **Response (200 OK)**
  ```json
  {
    "status": "healthy",
    "tools_registered": 3
  }
  ```

### GET /tools

Lists the available tools that the LLM can use.

- **Response (200 OK)**
  ```json
  {
    "tools": [
      {
        "name": "calculator",
        "description": "A tool to perform mathematical calculations.",
        "parameters": { ... }
      },
      {
        "name": "weather",
        "description": "A tool to get the weather forecast for a specific location.",
        "parameters": { ... }
      },
      {
        "name": "web_search",
        "description": "A tool to search the web for real-time information.",
        "parameters": { ... }
      }
    ]
  }
  ```

### POST /chat

The main endpoint for interacting with the LLM.

- **Request Body**
  ```json
  {
    "message": "What is the weather in San Francisco?",
    "conversation_history": [],
    "temperature": 0.7,
    "max_tokens": 1000
  }
  ```

- **Response (200 OK)**
  ```json
  {
    "response": "The weather in San Francisco is sunny with a high of 70 degrees.",
    "tool_results": [ ... ],
    "conversation_history": [ ... ]
  }
  ```

## How to Run the Project

### Prerequisites

- Python 3.8+
- Docker and Docker Compose
- An Ollama instance running. Ensure the base URL is correctly configured in your environment.

### Running Locally

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Create a virtual environment and activate it:**
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure your environment:**
    -   Create a `.env` file by copying the example:
        ```bash
        cp .env.example .env
        ```
    -   Edit the `.env` file to set your environment variables, especially `OLLAMA_BASE_URL`.

5.  **Run the application:**
    ```bash
    uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    ```

### Running with Docker

This method is recommended for a consistent and isolated environment.

1.  **Ensure your `.env` file is configured correctly.** The `OLLAMA_BASE_URL` should be accessible from within the Docker container. If you are running Ollama on your host machine, `http://host.docker.internal:11434` is often the correct address.

2.  **Build and run the container using Docker Compose:**
    ```bash
    docker-compose up -d --build
    ```
    The application will be available at `http://localhost:8000`.

### Running with Docker (Hot Reload for Development)

For development, you can use the hot-reloading setup to automatically apply code changes without rebuilding the container.

1.  **Use the `docker-compose.dev.yml` file:**
    ```bash
    docker-compose -f docker-compose.dev.yml up -d --build
    ```

This will mount the application code into the container, and `uvicorn` will automatically reload the application when it detects changes.

## Deployment

This application is containerized using Docker, which makes it easy to deploy to any cloud provider that supports Docker containers.

1. **Build the Docker image:**
   ```bash
   docker build -t function-calling-demo .
   ```

2. **Push the Docker image to a container registry:**
   ```bash
   docker push your-container-registry/function-calling-demo
   ```

3. **Configure the environment variables in your cloud provider's environment.**

4. **Deploy the container.**

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue if you have any suggestions or find any bugs.

## Future Improvements

- Add more tools to the registry.
- Implement a more sophisticated error handling and retry mechanism for tool execution.
- Add support for more LLM providers.
- Implement user authentication and authorization.
