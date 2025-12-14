# Prompt Engineering Demo

This project is a FastAPI application that demonstrates and allows for experimentation with various prompt engineering strategies.

## Table of Contents
- [Purpose](#purpose)
- [Strategies Implemented](#strategies-implemented)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)

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

## Getting Started

To get started, you will need to have Python and Docker installed.

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
