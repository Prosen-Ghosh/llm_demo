[<- Back to Main README](../../../README.md)

# LangChain Streaming SSE

The LangChain Streaming SSE project enables real-time LLM token streaming using Server-Sent Events (SSE) with FastAPI and LangChain.

## 🚀 Quick Start


1. Copy environment file:
   ```bash
   cp .env.example .env
   ```

2. Start services:
   ```bash
   docker compose up --build
   ```

3. Access the application:
   - **Web UI**: http://localhost:8000
   - **API Docs**: http://localhost:8000/docs
   - **Health Check**: http://localhost:8000/health

## 🧪 Testing

### Test with curl (SSE)
```bash
# Stream response
curl -N -X POST http://localhost:8000/stream \
  -H "Content-Type: application/json" \
  -d '{"query": "Explain quantum computing in simple terms", "temperature": 0.7}'

# Stream with chat history
curl -N -X POST http://localhost:8000/stream/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is AI?", "session_id": "user123"}'
```

### Test with Python
```python
import requests

url = "http://localhost:8000/stream"
data = {"query": "Tell me a short story"}

with requests.post(url, json=data, stream=True) as response:
    for line in response.iter_lines():
        if line:
            print(line.decode())
```

### Test with Browser
Open http://localhost:8000 for interactive streaming UI.

## 📊 API Endpoints

- `GET /` - Interactive web UI
- `POST /stream` - Stream LLM response (SSE)
- `POST /stream/chat` - Stream with conversation memory
- `POST /generate` - Non-streaming generation (comparison)
- `GET /health` - Health check

## 🎯 How it Works

The application uses a simple yet powerful architecture:

-   **FastAPI Backend**: Handles HTTP requests, manages conversation history, and serves the frontend UI.
-   **LangChain**: Provides the core logic for interacting with large language models (LLMs) and managing prompts.
-   **Server-Sent Events (SSE)**: Enables efficient, real-time streaming of LLM responses from the server to the client without the overhead of traditional polling or WebSockets.
-   **Docker**: Containerizes the application and its dependencies for easy deployment and scaling.

When a user sends a query, the FastAPI backend passes it to LangChain, which generates a response from the configured LLM. The response is streamed back to the client token-by-token using SSE, creating a real-time, interactive experience.

## ✨ Features

-   ✅ **Real-time Token Streaming**: Get instant feedback from the LLM with token-by-token streaming using SSE.
-   ✅ **Interactive Web UI**: A simple and intuitive web interface for sending queries and viewing streamed responses.
-   ✅ **Conversation Memory**: Maintains conversation history for follow-up questions and context-aware interactions.
-   ✅ **Flexible Configuration**: Easily configure the LLM model, temperature, and max tokens via environment variables.
-   ✅ **Performance Metrics**: Monitor key performance indicators like time-to-first-token and tokens per second.
-   ✅ **Built-in Error Handling**: Gracefully manages API errors and provides retry logic.
-   ✅ **Containerized**: Packaged with Docker for consistent and hassle-free deployment.
-   ✅ **Health and API Docs**: Includes `/health` for monitoring and `/docs` for interactive API documentation.

## Project Structure
```
.
├── app/
│   ├── __init__.py           # Initializes the app package.
│   ├── callbacks.py          # LangChain callbacks for streaming.
│   ├── main.py               # The FastAPI application entry point, defining API endpoints.
│   ├── models.py             # Pydantic models for request and response validation.
│   └── streaming.py          # Handles the SSE streaming logic.
├── static/
│   ├── action.js             # Frontend JavaScript for interactive elements.
│   ├── index.html            # Frontend HTML for the interactive streaming UI.
│   └── styles.css            # Frontend CSS for styling the UI.
├── tests/
│   └── test_streaming.py     # Unit tests for streaming functionality.
├── .env.example              # Example environment variables.
├── .gitignore                # Specifies intentionally untracked files to ignore.
├── docker-compose.yml        # Docker Compose configuration for the project.
├── Dockerfile                # Dockerfile for building the application container.
├── linkedin.md               # LinkedIn article related to the project.
├── README.md                 # This README file.
└── requirements.txt          # Lists Python package dependencies.
```

*   `app/`: Contains the core application logic.
    *   `main.py`: The FastAPI application entry point, defining API endpoints.
    *   `streaming.py`: Handles the SSE streaming logic.
    *   `callbacks.py`: LangChain callbacks for streaming.
    *   `models.py`: Pydantic models for request and response validation.
*   `static/`: Contains the frontend HTML, CSS, and JavaScript files.
*   `tests/`: Contains tests for the application.

## 🔧 Environment Variables

- `OLLAMA_API_URL` - Ollama API endpoint
- `OLLAMA_MODEL` - Model name (default: llama2)
- `MAX_TOKENS` - Maximum tokens per response
- `DEFAULT_TEMPERATURE` - Default temperature (0.0-1.0)

**Note:**
* The `.env.example` file serves as a template for the environment variables required by the application. Copy this file to `.env` and customize it with your specific settings.

## Future Improvements
*   Add support for more LLM providers.
*   Implement a more sophisticated caching mechanism.
*   Add more detailed logging and tracing.

## Contributing
Contributions are welcome! Please feel free to submit a pull request or open an issue if you have any suggestions or find any bugs.