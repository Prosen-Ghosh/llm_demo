# LangChain Tool Demo

## Table of Contents
- [Overview](#overview)
- [Problem Solved](#problem-solved)
- [How it Works](#how-it-works)
- [Features](#features)
- [Available Tools](#available-tools)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running with Docker](#running-with-docker)
- [API Endpoints](#api-endpoints)
  - [Chat](#chat)
  - [Chat Stream](#chat-stream)
  - [Health Check](#health-check)
- [License](#license)

## Overview

This project is a demonstration of an AI-powered shopping assistant API built with FastAPI and LangChain. The API provides a conversational interface to a large language model (LLM) that can use a set of tools to answer shopping-related queries.

## Problem Solved

This project demonstrates how to build a tool-using agent with LangChain and a local LLM (via Ollama). It provides a practical example of how to create a conversational AI that can interact with external systems (in this case, a mock product database) to answer user questions.

## How it Works

The application uses the following technologies:

- **FastAPI:** A modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints.
- **LangChain:** A framework for developing applications powered by language models. We use LangChain to create a tool-using agent that can interact with our shopping tools.
- **Ollama:** A tool for running large language models locally. The agent uses a model served by Ollama to understand user queries and decide which tools to use.

The agent is created using `create_agent` from LangChain and is configured with a system prompt and a set of tools. When the user sends a query, the agent uses the LLM to understand the user's intent and then calls the appropriate tool to get the information it needs to answer the question.

## Features

- **Conversational AI:** A conversational interface to a shopping assistant.
- **Tool-Using Agent:** The agent can use a set of tools to search for products and check their inventory.
- **Streaming API:** A streaming endpoint that provides real-time updates, including the agent's reasoning and tool calls.
- **Local LLM:** The application uses a locally running LLM, which can be configured to use any model supported by Ollama.

## Available Tools

The following tools are available to the agent:

- **`search_products(query: str)`:** Searches for products by name.
- **`check_inventory(product_id: str)`:** Checks if a product is in stock.

## Project Structure
```
.
├── .env.example              # Example environment file for API keys and configuration.
├── .gitignore                # Specifies intentionally untracked files to ignore.
├── Dockerfile                # Dockerfile for building the application container.
├── README.md                 # This README file.
├── app/                      # Source code for the application.
│   ├── api/                  # Defines API endpoints and their dependencies.
│   │   ├── dependencies.py   # Dependency injection for API endpoints.
│   │   └── endpoints.py      # Actual API endpoints for chat, streaming, and health checks.
│   ├── core/                 # Contains core application logic and configurations.
│   │   ├── agents.py         # Defines the LangChain agent and its behavior.
│   │   ├── config.py         # Application configuration settings.
│   │   └── tools.py          # Definitions of tools the LangChain agent can use.
│   ├── main.py               # Main entry point for the FastAPI application.
│   ├── schemas/              # Pydantic schemas for request and response validation.
│   │   └── chat.py           # Pydantic models specifically for chat-related data.
│   └── utils/                # Utility functions.
│       └── streaming.py      # Utilities related to Server-Sent Events (SSE) streaming.
├── docker-compose.dev.yml    # Docker Compose configuration for development with hot-reloading.
└── requirements.txt          # Lists all Python dependencies.
```

## Getting Started

### Prerequisites

- Python 3.7+
- Docker
- Ollama

### Installation

1. Clone the repository:
   ```bash
   git clone git@github.com:Prosen-Ghosh/llm_demo.git
   cd langchain-tool-demo
   ```

2. Create a virtual environment and install the dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. Set up the environment variables:
   ```bash
   cp .env.example .env
   ```
   Update the `.env` file with your Ollama configuration.
   **Note:** The `.env.example` file provides a template for the environment variables required to run the application. Copy this file to `.env` and customize it with your specific settings.

4. Run the application:
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

### Chat

- **Endpoint:** `/api/v1/chat`
- **Method:** `POST`
- **Description:** Sends a query to the shopping assistant and receives a response.
- **Request Body:**
  ```json
  {
    "query": "Are wireless headphones in stock?"
  }
  ```
- **Curl Example:**
  ```bash
  curl -X POST "http://localhost:8000/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Are wireless headphones in stock?"
  }'
  ```

### Chat Stream

- **Endpoint:** `/api/v1/chat-stream`
- **Method:** `POST`
- **Description:** Sends a query to the shopping assistant and receives a stream of server-sent events (SSE) with real-time updates.
- **Request Body:**
  ```json
  {
    "query": "Are wireless headphones in stock?"
  }
  ```
- **Curl Example:**
  ```bash
  curl -X POST "http://localhost:8000/api/v1/chat-stream" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Are wireless headphones in stock?"
  }'
  ```

### Health Check

- **Endpoint:** `/api/v1/health`
- **Method:** `GET`
- **Description:** Checks the health of the application.
- **Curl Example:**
  ```bash
  curl -X GET "http://localhost:8000/api/v1/health"
  ```

## License

This project is licensed under the MIT License.
