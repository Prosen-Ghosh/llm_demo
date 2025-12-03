# Function Calling Demo

This project is a FastAPI-based application that demonstrates an enterprise-grade function calling system using a Large Language Model (LLM). The application is designed to be a pluggable and extensible system, with an example implementation using Ollama. It allows the LLM to use a set of external tools, such as a calculator, weather service, and web search, to provide more accurate and context-aware responses.

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
