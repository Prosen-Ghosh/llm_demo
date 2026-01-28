# Queryable Doc

This is a demo application that showcases a Retrieval-Augmented Generation (RAG) pipeline using LangChain, OpenAI, and ChromaDB. It allows you to upload your documents and ask questions about their content. The application is built with Streamlit.

## Key Features

-   **Document Upload:** Supports multiple file types including PDF (`.pdf`), Word documents (`.doc`, `.docx`), and text files (`.txt`).
-   **Configurable Chunking:** Customize the `chunk size` and `chunk overlap` for document processing directly from the UI.
-   **Vector Embeddings:** Creates vector embeddings from document chunks using OpenAI's models and stores them in a ChromaDB vector store.
-   **Retrieval-Augmented Generation (RAG):** Utilizes a LangChain RAG chain to retrieve relevant document chunks and generate answers to user questions.
-   **Chat Interface:** Displays the conversation history, including the source chunks used to generate each answer.
-   **Flexible LLM:** Uses OpenRouter to connect to OpenAI models, allowing for easy model switching.

## How It Works

The application follows a standard RAG pipeline:

1.  **Upload & Load:** The user uploads one or more documents through the Streamlit interface. The application uses LangChain's document loaders to read the content.
2.  **Split (Chunking):** The loaded documents are split into smaller, manageable chunks using `RecursiveCharacterTextSplitter`.
3.  **Embed & Store:** Each chunk is converted into a vector embedding using an OpenAI embedding model. These embeddings are then stored in a ChromaDB vector database.
4.  **Retrieve:** When a user asks a question, the application embeds the query and uses the ChromaDB store to retrieve the most relevant document chunks (based on vector similarity).
5.  **Generate:** The retrieved chunks (context) and the user's original question are passed to an OpenAI language model via a LangChain chain, which generates a final, context-aware answer.

## Technology Stack

-   **Application Framework:** [Streamlit](https://streamlit.io/)
-   **LLM & RAG Orchestration:** [LangChain](https://www.langchain.com/)
-   **LLM Provider:** [OpenAI](https://openai.com/) via [OpenRouter](https://openrouter.ai/)
-   **Vector Store:** [ChromaDB](https://www.trychroma.com/)
-   **Document Loaders:** `pypdf`, `python-docx`
-   **Python Version:** 3.11

## Getting Started

### Prerequisites

- Python 3.11+
- Docker (optional)

### Local Development

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Prosen-Ghosh/llm_demo.git
    cd queryable_doc
    ```

2.  **Run the setup script:**
    This script will create a virtual environment, activate it, and install all the required dependencies.
    ```bash
    bash setup.sh
    ```
    *Note: If you are on Windows, you may need to run the commands in `setup.sh` manually in a terminal.*

3.  **Set up your API Key:**
    The application requires an OpenAI-compatible API key provided through [OpenRouter](https://openrouter.ai/).
    -   Create a `.env` file in the root of the project.
    -   Add your API key to the `.env` file like this:
        ```
        OPENROUTER_API_KEY="your-api-key-here"
        ```
    -   Alternatively, you can enter the key directly in the application's sidebar.

4.  **Activate the virtual environment:**
    ```bash
    source venv/bin/activate
    ```
    *(On Windows, use `venv\Scripts\activate`)*

5.  **Run the Streamlit application:**
    ```bash
    streamlit run app.py
    ```
    The application will open in your web browser.

### Using Docker

1.  **Set up your API Key:**
    - Create a `.env` file as described in the local development section.

2.  **Build and Run with Docker:**
    ```bash
    docker build -t queryable-doc .
    docker run -p 8501:8501 -v $(pwd)/data:/app/data --env-file .env queryable-doc
    ```
    The application will be available at `http://localhost:8501`.

## Project Structure

```
.
├── Dockerfile
├── README.md
├── app.py
├── chat.py
├── document_handler.py
├── embeddings.py
├── requirements.txt
├── setup.sh
├── ui/
│   ├── footer.py
│   ├── main.py
│   └── sidebar_config.py
├── utils.py
└── venv/
```

## Deployment

This application is containerized using Docker, which makes it easy to deploy to any cloud provider that supports Docker containers. Here are the general steps to deploy this application:

1. **Build the Docker image:**
   ```bash
   docker build -t queryable-doc .
   ```

2. **Push the Docker image to a container registry:**
   ```bash
   docker push your-container-registry/queryable-doc
   ```

3. **Configure the environment variables in your cloud provider's environment.**

4. **Deploy the container.**

For more detailed instructions, please refer to your cloud provider's documentation.

## 🤝 Contributing

Contributions are welcome! If you have suggestions for improvements or new features, please feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License.
