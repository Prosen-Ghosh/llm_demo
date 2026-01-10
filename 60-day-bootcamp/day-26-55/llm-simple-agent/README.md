[<- Back to Main README](../../../README.md)

# LLM Simple Agent

This project is a simple demonstration of a tool-calling agent built with LangChain and FastAPI. The agent is capable of understanding user queries and routing them to the appropriate tool, either a calculator or a web search tool.

![llm-simple-agent](llm-simple-agent.png)

## Purpose
The main purpose of this project is to provide a simple and easy-to-understand example of a tool-calling agent. It demonstrates how to build an agent that can use external tools to answer questions and perform actions.

## Tech Stack

*   **[LangChain](https://python.langchain.com/v0.1/docs/get_started/introduction/)**: A framework for developing applications powered by language models, used here for building the agent and managing its control flow.
*   **[Ollama](https://ollama.ai/)**: A tool for running large language models locally, enabling the use of models like Llama 3 without requiring external API access.
*   **[FastAPI](https://fastapi.tiangolo.com/)**: A modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints, used for serving the agent as a REST API.
*   **[Docker](https://www.docker.com/)**: A platform for developing, shipping, and running applications in containers, used here for containerizing the application for easy deployment and scalability.

## Getting Started

### Prerequisites

*   [Docker](https://docs.docker.com/get-docker/) installed on your machine.
*   [Ollama](https://ollama.ai/) installed and running.

### Installation

1.  **Pull the Ollama model:**

    ```bash
    ollama run gpt-oss:120b-cloud
    ```

2.  **Build and run the application:**

    ```bash
    docker-compose up --build
    ```

**Note:** The `.env.example` file provides a template for environment variables. Copy it to `.env` and configure as needed.

## Usage

Once the application is running, you can interact with the agent by sending POST requests to the `/ask` endpoint.

### Calculator

To perform a calculation, send a POST request with a JSON payload containing the query:

```bash
curl -X POST "http://localhost:8000/ask" -H "Content-Type: application/json" -d '{"query": "What is 25 * 4?"}'
```

### Web Search

To perform a web search, send a POST request with a JSON payload containing the query:

```bash
curl -X POST "http://localhost:8000/ask" -H "Content-Type: application/json" -d '{"query": "Who is the president of France?"}'
```

## Project Structure

```
.
├── app/
│   ├── __init__.py         # Initializes the app package.
│   ├── agents.py           # Defines the LangChain agent with its tools and logic.
│   └── main.py             # FastAPI application entry point, setting up endpoints.
├── .env.example            # Example environment variables for configuration.
├── .gitignore              # Specifies intentionally untracked files to ignore.
├── docker-compose.yml      # Docker Compose configuration for multi-container Docker applications.
├── Dockerfile              # Defines how to build the Docker image for the application.
├── linkedin.md             # LinkedIn article related to the project.
├── llm-simple-agent.png    # Diagram or image illustrating the LLM simple agent.
├── README.md               # Project README file.
└── requirements.txt        # Lists Python package dependencies.
```

## Future Improvements
*   Add more tools to the agent.
*   Implement a more sophisticated agent with memory.
*   Add a user interface for interacting with the agent.

## Contributing

Contributions are welcome! Please feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License.