[<- Back to Main README](../../../README.md)

# LLM Middleware FastAPI

The LLM Middleware FastAPI project demonstrates how to build a FastAPI application with a custom middleware for processing requests and a simple LangGraph agent.

## Purpose
The main purpose of this project is to showcase how to integrate a custom middleware with a FastAPI application to process incoming requests and add context to them. It also demonstrates how to build a simple agent using LangGraph.

## How it Works

The application uses the following technologies:

- **FastAPI:** A modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints.
- **LangGraph:** A library for building stateful, multi-actor applications with LLMs.
- **Middleware:** A custom middleware to process incoming requests and add a request ID to the response headers.

### Middleware

The `request_context_middleware` in `app/middleware.py` intercepts incoming requests and performs the following actions:

- Generates a unique request ID using `uuid.uuid4()` and stores it in `request.state.req_id`.
- Retrieves the `q` query parameter, strips leading/trailing whitespace, and stores it in `request.state.sanitized_q`.
- Adds the request ID to the response headers as `X-Request-ID`.

### Agent and Graph

The `run_agent` function in `app/agent.py` creates a simple LangGraph agent with a single node. The agent takes a payload and returns a processed output. The graph is defined in `app/graph.py` and consists of a single node that calls a tool.

## Project Structure

```
.
├── Dockerfile
├── README.md
├── __init__.py
├── app/
│   ├── __init__.py
│   ├── agent.py
│   ├── graph.py
│   ├── main.py
│   ├── middleware.py
│   └── tools.py
├── docker-compose.yml
├── linkedin.md
├── requirements.txt
```

## Getting Started

### Prerequisites

- Python 3.7+
- Docker

### Installation


1. Create a virtual environment and install the dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. Set up environment variables:
   Copy the `.env.example` file to `.env` and fill in the required API keys and configurations.
   **Note:** The `.env.example` file provides a template for the environment variables required to run the application. Copy this file to `.env` and customize it with your specific settings.

3. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```

### Running with Docker

1. Build the Docker image:
   ```bash
   docker-compose build
   ```

2. Run the application:
   ```bash
   docker-compose up
   ```

## API Endpoints

### Agent

- **Endpoint:** `/agent/run`
- **Method:** `POST`
- **Description:** Runs the LangGraph agent.
- **Request Body:**
  ```json
  {
    "input": "hello"
  }
  ```
- **Curl Example:**
  ```bash
  curl -X POST "http://localhost:8000/agent/run" \
  -H "Content-Type: application/json" \
  -d '{
    "input": "hello"
  }'
  ```

### Health Check

- **Endpoint:** `/health`
- **Method:** `GET`
- **Description:** Checks the health of the application.
- **Curl Example:**
  ```bash
  curl -X GET "http://localhost:8000/health"
  ```

## Future Improvements
*   Add more complex agents and graphs.
*   Implement a more sophisticated middleware for authentication and authorization.
*   Add more tools to the agent.

## Contributing
Contributions are welcome! Please feel free to submit a pull request or open an issue if you have any suggestions or find any bugs.
