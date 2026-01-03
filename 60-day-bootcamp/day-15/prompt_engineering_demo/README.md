[<- Back to Main README](../../README.md)

# Prompt Engineering Demo

This project is a FastAPI application that demonstrates and allows for experimentation with various prompt engineering strategies.

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
├── app/
│   ├── main.py
│   ├── services/
│   │   ├── analyzer.py
│   │   ├── llm_client.py
│   │   └── prompt_manager.py
│   └── strategies/
│       ├── base.py
│       ├── chain_of_thought.py
│       ├── react.py
│       └── self_consistency.py
├── data/
│   └── prompts.db
└── ...
```

*   `app/main.py`: The entry point of the FastAPI application, defining the API endpoints.
*   `app/services/`: Contains the business logic, including the `LLMClient` for interacting with the LLM, the `PromptManager` for handling prompt versioning, and the `QueryAnalyzer` for suggesting prompt strategies.
*   `app/strategies/`: Implements the different prompt engineering strategies.
*   `data/prompts.db`: A SQLite database for storing prompt versions.

## API Documentation

### GET /
Lists all prompts from the database.

### GET /health
Health check endpoint.

### POST /v1/query
The main query endpoint with auto-strategy selection.

### POST /v1/query/stream
Streaming query endpoint.

### POST /v1/prompts/version
Create a new prompt version.

### GET /v1/prompts/versions
List all prompt versions.

### POST /v1/prompts/compare
A/B test two prompt versions.

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

## Future Improvements
*   Add more prompt engineering strategies.
*   Implement a more sophisticated A/B testing framework.
*   Add a UI for managing prompt versions.

## Contributing
Contributions are welcome! Please feel free to submit a pull request or open an issue if you have any suggestions or find any bugs.
