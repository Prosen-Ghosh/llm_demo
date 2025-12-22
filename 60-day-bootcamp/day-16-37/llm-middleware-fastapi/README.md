# LLM Middleware with FastAPI

This project demonstrates how to build a FastAPI application with a custom middleware for processing requests and a simple LangGraph agent.

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

### Agent

The `run_agent` function in `app/agent.py` creates a simple LangGraph agent with a single node. The agent takes a payload and returns a processed output.

## Project Structure

```
.
├── .env.example              # Example environment file for API keys.
├── .gitignore                # Git ignore file.
├── docker-compose.yml        # Docker compose file for development.
├── Dockerfile                # Dockerfile for building the application container.
├── README.md                 # This README file.
├── app/                      # Source code for the application.
│   ├── __init__.py           #
│   ├── agent.py              # LangGraph agent.
│   ├── graph.py              # LangGraph graph.
│   ├── main.py               # Main entry point for the FastAPI application.
│   ├── middleware.py         # Custom middleware.
│   └── tools.py              # Tools for the LangGraph agent.
└── requirements.txt          # Lists all Python dependencies.
```

## Getting Started

### Prerequisites

- Python 3.7+
- Docker

### Installation

1. Clone the repository:
   ```bash
   git clone git@github.com:Prosen-Ghosh/llm_demo.git
   cd 60-day-bootcamp/day-16-37/llm-middleware-fastapi
   ```

2. Create a virtual environment and install the dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

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
