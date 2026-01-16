# Context Engineering RAG API

This project is a FastAPI application that provides a Retrieval-Augmented Generation (RAG) API. It allows users to ingest documents, chunk them into smaller pieces, and perform semantic searches on them. The API is built with Python 3.12 and utilizes a stack of modern technologies including Docker, Weaviate, PostgreSQL, and Redis.

## Project Structure

- `.`
    - `.env.example`: Example file for environment variables.
    - `.gitignore`: Specifies intentionally untracked files to ignore.
    - `docker-compose.yml`: Defines the multi-container Docker application, including the API, Weaviate, PostgreSQL, and Redis services.
    - `Dockerfile`: Defines the Docker image for the FastAPI application.
    - `README.md`: This project documentation.
    - `requirements.txt`: Python dependencies.
    - `scripts/`: Contains utility scripts, such as for demonstrating chunking and similarity search.
    - `src/`:
        - `main.py`: The entry point for the FastAPI application.
        - `api/`: Contains the API routers.
        - `models/`: Contains the Pydantic data models (schemas).
        - `utils/`: Contains utility functions, such as for chunking and creating embeddings.
    - `tests/`: Contains the tests for the API and other components.
- `venv/`: Python virtual environment (ignored by Git).
- `.pytest_cache/`: pytest cache directory (ignored by Git).
- `__pycache__/`: Python cache directories (ignored by Git).


## Services

This project uses the following services, orchestrated by `docker-compose.yml`:

-   **app**: The FastAPI application.
-   **weaviate**: A vector database used for storing and searching document embeddings.
-   **postgres**: A PostgreSQL database for storing metadata.
-   **redis**: A Redis instance for caching.

## Chunking

This project supports two chunking strategies:

-   **Recursive Chunking**: Splits text recursively based on a set of separators. This is the default strategy.
-   **Hierarchical Chunking**: Creates parent and child chunks. Parent chunks are larger and contain the full context, while child chunks are smaller and are used for retrieval.

The chunking service is implemented in `src/utils/chunking.py`. You can see a demonstration of the chunking strategies by running `python scripts/demo_chunking.py`.

## Setup

### Prerequisites

-   Docker: [Install Docker](https://docs.docker.com/get-docker/)
-   Python 3.12+ (for local development without Docker)

### Local Development Environment

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-repo/context-engineering.git
    cd context-engineering
    ```

2.  **Set up environment variables:**
    Create a `.env` file based on `.env.example`:
    ```bash
    cp .env.example .env
    ```
    Edit `.env` and fill in your specific environment variables.

3.  **Build and run Docker containers:**
    ```bash
    docker-compose up --build -d
    ```
    This will start all the services defined in `docker-compose.yml` in detached mode.

## Running the Application

The FastAPI application will be running at `http://localhost:8000`. You can access the API documentation at `http://localhost:8000/docs`.

## API Usage

The API provides the following endpoints:

-   `GET /api/v1/health`: Health check endpoint.
-   `POST /api/v1/ingest`: Ingests and chunks documents into the system.
-   `POST /api/v1/search`: Performs a semantic search on the ingested documents.

For detailed information about the request and response models, please refer to the API documentation at `http://localhost:8000/docs`.

## Running Tests

Tests are written using `pytest`.

To run all tests, you can run the following command inside the `app` container:

```bash
docker-compose exec app pytest
```

Alternatively, you can run the tests locally after installing the dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pytest
```

## Contributing

(Guidelines for contributing to the project.)

## License

(Project license information.)