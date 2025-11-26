# 📚 RAG Document Q&A System

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

## Setup and Installation

The `setup.sh` script automates the setup process.

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd <your-repo-name>
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

## How to Run

1.  **Activate the virtual environment:**
    ```bash
    source venv/bin/activate
    ```
    *(On Windows, use `venv\Scripts\activate`)*

2.  **Run the Streamlit application:**
    ```bash
    streamlit run app.py
    ```

The application will open in your web browser.

## Project Structure

```
.
├── app.py              # Main entry point for the Streamlit application.
├── chat.py             # Handles the core RAG chain logic and chat history display.
├── document_handler.py # Manages loading and processing of uploaded documents.
├── embeddings.py       # Handles document chunking and vector embedding creation/storage.
├── requirements.txt    # Lists all Python dependencies.
├── setup.sh            # Automates the project setup.
├── ui/                 # Module for Streamlit UI components.
│   ├── main.py         # Renders the main body of the app (upload and chat columns).
│   ├── sidebar_config.py # Renders the sidebar for configuration.
│   └── footer.py       # Renders the application footer.
└── utils.py            # Utility functions, including session state initialization.
```
