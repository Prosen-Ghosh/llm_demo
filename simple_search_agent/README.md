# Simple Search Agent (LangChain + SerpAPI)

This project is a simple web-based AI agent that can answer questions about current events by searching the web. It's built using Python, LangChain, Streamlit, SerpAPI, and OpenRouter.

## What it does

The application provides a web interface where you can ask a question. The agent then:
1.  Takes the user's question.
2.  Uses the SerpAPI to perform a web search based on the question.
3.  Feeds the search results to a Large Language Model (LLM) via OpenRouter.
4.  The LLM generates an answer based on the provided search results.
5.  The application displays the answer and the original search snippets to the user.

## Getting Started

### Prerequisites

- Python 3.8+
- Docker (optional)

### Local Development

1.  **Clone the repository:**
    ```bash
    git clone git@github.com:Prosen-Ghosh/llm_demo.git
    cd simple_search_agent
    ```

2.  **Set up the environment:**
    - It's recommended to use a virtual environment.
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
    - Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up your API keys:**
    - Create a `.env` file by copying the example file:
    ```bash
    cp example.env .env
    ```
    - Edit the `.env` file and add your API keys:
        - `SERPAPI_API_KEY`: Get this from [SerpApi](https://serpapi.com/manage-api-key).
    - You will be prompted to enter your OpenRouter API key in the web interface. You can get one from [OpenRouter](https://openrouter.ai/keys).

4.  **Run the application:**
    ```bash
    streamlit run app.py
    ```
    The application will be available at `http://localhost:8501`.

### Using Docker

1.  **Set up your API keys:**
    - Create a `.env` file as described in the local development section.

2.  **Run with Docker:**
    ```bash
    docker build -t simple-search-agent .
    docker run -p 8501:8501 -v $(pwd):/app --env-file .env simple-search-agent
    ```
    The application will be available at `http://localhost:8501`.

## Project Structure

```
.
├── .gitignore          # Git ignore file.
├── Dockerfile          # Dockerfile for building the application container.
├── README.md           # This README file.
├── agent_tools.py      # Defines the tools available to the LangChain agent (e.g., web search).
├── app.py              # Main entry point for the Streamlit application.
├── example.env         # Example environment file for API keys.
├── requirements.txt    # Lists all Python dependencies.
├── setup.sh            # A shell script to automate the setup process.
├── simple_agent.py     # Contains the core logic for the LangChain agent.
└── utils.py            # Utility functions for the application.
```

## Deployment

This application is containerized using Docker, which makes it easy to deploy to any cloud provider that supports Docker containers. Here are the general steps to deploy this application:

1. **Build the Docker image:**
   ```bash
   docker build -t simple-search-agent .
   ```

2. **Push the Docker image to a container registry:**
   ```bash
   docker push your-container-registry/simple-search-agent
   ```

3. **Configure the environment variables in your cloud provider's environment.**

4. **Deploy the container.**

For more detailed instructions, please refer to your cloud provider's documentation.

## Demo App Preview

You can try the demo app live here: https://simple-search-agent.streamlit.app/

## Purpose and Learnings

This project serves as a practical example of how to build a simple but powerful AI agent. Key learnings include:

-   **Building an AI Agent:** Understand the basic components of an AI agent, including the agent itself, tools, and the orchestrating framework (LangChain).
-   **Using External Tools:** Learn how to give an AI agent access to external tools, in this case, a web search API (SerpAPI). This allows the agent to access up-to-date information that is not in its training data.
-   **LangChain for Orchestration:** See how LangChain can be used to easily connect and orchestrate different components like LLMs, prompts, and tools.
-   **Streamlit for UI:** Learn how to quickly build an interactive and user-friendly web interface for an AI application using Streamlit.
-   **Accessing LLMs via OpenRouter:** Understand how to use OpenRouter to access a variety of LLMs from different providers with a single API key.
-   **Environment and Key Management:** Best practices for managing API keys and environment variables using a `.env` file.

## 🤝 Contributing

Contributions are welcome! If you have suggestions for improvements or new features, please feel free to open an issue or submit a pull request.
