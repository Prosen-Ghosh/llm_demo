[<- Back to Main README](../../../README.md)

# Prompt Engineering Demo

The Prompt Engineering Demo project is a FastAPI application that demonstrates and allows for experimentation with various prompt engineering strategies.

## Table of Contents
- [Purpose](#purpose)
- [Strategies Implemented](#strategies-implemented)
- [Project Structure](#project-structure)
- [API Documentation](#api-documentation)
- [Getting Started](#getting-started)
- [Future Improvements](#future-improvements)
- [Contributing](#contributing)

## Purpose

The main purpose of this project is to provide a hands-on demonstration of how different prompt engineering techniques can be used to improve the quality and reliability of responses from Large Language Models (LLMs). By structuring prompts in specific ways, we can guide the LLM to perform more complex reasoning and generate more accurate results.

## Strategies Implemented

*   **Chain of Thought (CoT):** Encourages the LLM to break down a problem into a series of intermediate steps, mimicking a reasoning process.
*   **ReAct (Reason and Act):** A framework that combines reasoning and action, allowing the LLM to interact with external tools to gather information before generating a final response.
*   **Self-Consistency:** A technique that involves generating multiple responses from the LLM and then selecting the most consistent one, which can improve accuracy on complex reasoning tasks.

## Project Structure

The project is structured as a standard FastAPI application:

```
.
├── app/                      # Source code for the FastAPI application.
│   ├── __init__.py           # Initializes the app package.
│   ├── config.py             # Configuration settings for the application.
│   ├── main.py               # Main entry point of the FastAPI application.
│   ├── models/               # Contains Pydantic models for data validation.
│   │   ├── __init__.py       # Initializes the models package.
│   │   ├── prompts.py        # Pydantic models related to prompts.
│   │   └── schemas.py        # Pydantic schemas for API requests and responses.
│   ├── services/             # Contains business logic and services.
│   │   ├── __init__.py       # Initializes the services package.
│   │   ├── analyzer.py       # Service for analyzing queries.
│   │   ├── llm_client.py     # Client for interacting with the LLM.
│   │   └── prompt_manager.py # Service for managing prompt versions.
│   ├── strategies/           # Implements various prompt engineering strategies.
│   │   ├── __init__.py       # Initializes the strategies package.
│   │   ├── base.py           # Base class for prompt strategies.
│   │   ├── chain_of_thought.py # Implementation of Chain of Thought strategy.
│   │   ├── react.py          # Implementation of ReAct strategy.
│   │   └── self_consistency.py # Implementation of Self-Consistency strategy.
│   └── utils/                # Utility functions.
│       ├── __init__.py       # Initializes the utils package.
│       └── logger.py         # Logging configuration.
├── data/                     # Data directory.
│   └── prompts.db            # SQLite database for storing prompt versions.
├── logs/                     # Log directory.
│   └── app.log               # Log file for the application.
├── .env.example              # Example environment file for API keys and configurations.
├── .gitignore                # Specifies intentionally untracked files to ignore.
├── docker-compose.dev.yml    # Docker Compose configuration for development.
├── Dockerfile                # Defines how to build the Docker image for the application.
├── README.md                 # This README file.
└── requirements.txt          # Lists all Python dependencies.
```

*   `app/main.py`: The entry point of the FastAPI application, defining the API endpoints.
*   `app/services/`: Contains the business logic, including the `LLMClient` for interacting with the LLM, the `PromptManager` for handling prompt versioning, and the `QueryAnalyzer` for suggesting prompt strategies.
*   `app/strategies/`: Implements the different prompt engineering strategies.
*   `data/prompts.db`: A SQLite database for storing prompt versions.
*   `logs/app.log`: Log file for the application.

## API Documentation

### GET /
Lists all prompts from the database.
```bash
curl -X GET "http://127.0.0.1:8000/"
```

### GET /health
Health check endpoint.
```bash
curl -X GET "http://127.0.0.1:8000/health"
```

### POST /v1/query
The main query endpoint with auto-strategy selection.
```bash
curl -X POST "http://127.0.0.1:8000/v1/query" -H "Content-Type: application/json" -d '{
    "query": "Your query here"
}'
```

### POST /v1/query/stream
Streaming query endpoint.
```bash
curl -X POST "http://127.0.0.1:8000/v1/query/stream" -H "Content-Type: application/json" -d '{
    "query": "Your query here"
}'
```

### POST /v1/prompts/version
Create a new prompt version.
```bash
curl -X POST "http://127.0.0.1:8000/v1/prompts/version" -H "Content-Type: application/json" -d '{
    "prompt": "Your new prompt here"
}'
```

### GET /v1/prompts/versions
List all prompt versions.
```bash
curl -X GET "http://127.0.0.1:8000/v1/prompts/versions"
```

### POST /v1/prompts/compare
A/B test two prompt versions.
```bash
curl -X POST "http://127.0.0.1:8000/v1/prompts/compare" -H "Content-Type: application/json" -d '{
    "version1": 1,
    "version2": 2
}'
```

## Getting Started

To get started, you will need to have Python and Docker installed.

### Prerequisites
*   Python 3.8+
*   Docker and Docker Compose

### Running Locally
1.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Set up environment variables:**
    Copy the `.env.example` file to `.env` and fill in the required API keys and configurations.

3.  **Run the application:**
    ```bash
    uvicorn app.main:app --reload
    ```
The application will be available at `http://localhost:8000`.

### Running with Docker

1.  **Set up environment variables:**
    Create a `.env` file as described in the local development section.

2.  **Run with Docker Compose:**
    ```bash
    docker-compose -f docker-compose.dev.yml up --build
    ```
    The API will be available at `http://localhost:8000`.

**Note:**
* The `.env.example` file provides a template for the environment variables required to run the application. Copy this file to `.env` and fill in the required values.
* The `data/prompts.db` file is a SQLite database used to store prompt versions. It is created automatically when the application starts.
* The `logs` directory contains log files for the application.

## Future Improvements
*   Add more prompt engineering strategies.
*   Implement a more sophisticated A/B testing framework.
*   Add a UI for managing prompt versions.

## Contributing
Contributions are welcome! Please feel free to submit a pull request or open an issue if you have any suggestions or find any bugs.
