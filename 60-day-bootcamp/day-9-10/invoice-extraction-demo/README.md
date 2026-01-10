[<- Back to Main README](/README.md)

# Invoice Extraction Demo

This demo showcases an enterprise-grade solution for extracting structured data from unstructured invoice text using Large Language Models (LLMs). It leverages both local models via Ollama and commercial models via OpenRouter, with a built-in repair engine to handle extraction failures and ensure data quality.

## The Problem

Enterprises receive invoices in a multitude of formats (PDF, text, images). Manually extracting key information like invoice numbers, amounts, and line items is time-consuming, error-prone, and doesn't scale. While traditional OCR can digitize text, it doesn't provide the structured, validated data needed for accounting and ERP systems.

This demo tackles the "last mile" problem: converting raw, unstructured text into validated, schema-compliant JSON data ready for downstream processing.

## What This Demo Does

This application is a FastAPI-based REST API that:

-   **Accepts Unstructured Text**: Takes raw invoice text as input.
-   **Dual Extraction Strategy**:
    1.  **Ollama (Primary)**: Uses a local LLM (e.g., `llama3.1`) with JSON schema enforcement for cost-effective and private data processing.
    2.  **OpenRouter (Fallback)**: If the primary strategy fails, it can fall back to a powerful model on OpenRouter (e.g., `meta-llama/llama-3.2-3b-instruct:free`) using function calling for higher accuracy.
-   **Self-Correcting Repair Engine**: If an extraction attempt fails Pydantic validation, the system automatically retries, feeding the validation errors back to the LLM to correct its output.
-   **Data Validation**: All extracted data is rigorously validated against a Pydantic schema (`InvoiceData`) to ensure type safety, format correctness, and logical consistency (e.g., `total_amount` equals `subtotal` + `tax_amount`).
-   **Rich API Response**: Returns not just the extracted data, but also metadata including the strategy used, confidence scores, number of retries, and any validation errors.

## Project Structure

```
.
├── .env.example              # Example environment variables for configuring LLM keys and other settings.
├── .gitignore                # Specifies intentionally untracked files to ignore.
├── docker-compose.dev.yml    # Docker Compose configuration for development with hot-reloading.
├── Dockerfile                # Defines how to build the Docker image for the application.
├── README.md                 # This README file.
├── requirements.txt          # Lists all Python dependencies.
└── app/                      # Source code for the FastAPI application.
    ├── __init__.py           # Initializes the app package.
    ├── main.py               # Main FastAPI application entry point, defining API routes.
    ├── api/                  # Contains API endpoint definitions.
    │   ├── __init__.py
    │   └── routes.py         # Defines the API routes, such as '/extract' and '/health'.
    ├── core/                 # Core components like configuration and logging.
    │   ├── __init__.py
    │   ├── config.py         # Application settings and environment variable loading.
    │   └── logging.py        # Custom logging configuration.
    ├── models/               # Pydantic models for data validation and serialization.
    │   ├── __init__.py
    │   └── schemas.py        # Defines the InvoiceData schema and other data models.
    ├── sample_invoices/      # Contains sample invoice text files for testing and demonstration.
    │   └── sample_invoice.txt
    └── services/             # Business logic and LLM interaction services.
        ├── __init__.py
        ├── ollama_extractor.py     # Service for extracting data using Ollama models.
        ├── openrouter_extractor.py # Service for extracting data using OpenRouter models.
        └── repair_engine.py        # Handles validation failures and retries extraction with LLM feedback.
```

## API Documentation

The API is served by a FastAPI application.

### Health Check

-   **Endpoint**: `GET /api/v1/health`
-   **Description**: A simple health check endpoint to confirm the service is running.
-   **Success Response** (`200 OK`):
    ```json
    {
      "status": "healthy",
      "service": "invoice-extraction-demo"
    }
    ```

### Extract Invoice Data

-   **Endpoint**: `POST /api/v1/extract`
-   **Description**: Extracts structured data from invoice text.
-   **Request Body**:
    ```json
    {
      "invoice_text": "...",
      "prefer_strategy": "auto"
    }
    ```
    -   `invoice_text` (string, required): The raw text content of the invoice.
    -   `prefer_strategy` (string, optional): Can be `'ollama'`, `'openrouter'`, or `'auto'` (default).

-   **Example `curl` Request**:

    ```bash
    curl -X POST http://localhost:8000/api/v1/extract \
    -H "Content-Type: application/json" \
    -d '{
      "invoice_text": "INVOICE Invoice Number: INV-2024-001234 Date: 2024-03-15 Due Date: 2024-04-15 VENDOR: TechSupply Corp. 1234 Silicon Valley Blvd San Francisco, CA 94105 Tax ID: 94-1234567 Email: billing@techsupply.com BILL TO: Acme Industries 5678 Business Park Dr Austin, TX 78701 LINE ITEMS: Description                  Qty    Unit Price    Line Total ----------------------------------------------------------- Dell Laptop XPS 15          10      $1,299.00    $12,990.00 Wireless Mouse              25        $24.99       $624.75 USB-C Hub                   10        $49.99       $499.90 24\" Monitor                 15       $299.00     $4,485.00 Subtotal:    $18,599.65 Sales Tax:    $1,487.97 TOTAL DUE:   $20,087.62 Payment Terms: Net 30 Currency: USD Notes: Please include invoice number with payment."
    }'
    ```

-   **Example Success Response** (`200 OK`):

    ```json
    {
        "success": true,
        "data": {
            "invoice_number": "INV-2024-001234",
            "invoice_date": "2024-03-15",
            "due_date": "2024-04-15",
            "vendor": {
                "name": "TechSupply Corp.",
                "address": "1234 Silicon Valley Blvd, San Francisco, CA 94105",
                "tax_id": "94-1234567",
                "contact_email": null
            },
            "line_items": [
                {
                    "description": "Dell Laptop XPS 15",
                    "quantity": "10",
                    "unit_price": "1299.0",
                    "line_total": "12990.0"
                },
                {
                    "description": "Wireless Mouse",
                    "quantity": "25",
                    "unit_price": "24.99",
                    "line_total": "624.75"
                },
                {
                    "description": "USB-C Hub",
                    "quantity": "10",
                    "unit_price": "49.99",
                    "line_total": "499.9"
                },
                {
                    "description": "24\" Monitor",
                    "quantity": "15",
                    "unit_price": "299.0",
                    "line_total": "4485.0"
                }
            ],
            "subtotal": "18599.65",
            "tax_amount": "1487.97",
            "total_amount": "20087.62",
            "currency": "USD",
            "notes": "Please include invoice number with payment."
        },
        "errors": [],
        "confidence_score": 1.0,
        "strategy_used": "ollama",
        "retry_count": 0,
        "partial_data": null
    }
    ```

## How to Run the Application

This project is containerized using Docker.

### Prerequisites

-   Docker and Docker Compose
-   A running Ollama instance accessible to Docker.

### Steps

1.  **Clone the repository.**
2.  **Create an environment file**:
    Copy the `.env.example` to `.env` and fill in the required values.
    ```bash
    cp .env.example .env
    ```
    -   `OPENROUTER_API_KEY`: Your API key from [OpenRouter.ai](https://openrouter.ai/).
    -   `OLLAMA_BASE_URL`: The base URL for your Ollama instance. If running Ollama locally on the host machine, the default `http://host.docker.internal:11434` should work on most systems.
    **Note:** The `.env.example` file provides a template for the environment variables required to run the application. Copy this file to `.env` and customize it with your specific settings.

3.  **Build and run the Docker container**:
    ```bash
    docker-compose -f docker-compose.dev.yml up --build
    ```
4.  The API will be available at `http://localhost:8000`.

## Configuration

The application is configured via environment variables:

| Variable                     | Description                                                                 | Default                                 |
| ---------------------------- | --------------------------------------------------------------------------- | --------------------------------------- |
| `ENVIRONMENT`                | Application environment (`development` or `production`).                    | `development`                           |
| `LOG_LEVEL`                  | Logging level (`INFO`, `DEBUG`, `WARNING`, `ERROR`).                        | `INFO`                                  |
| `OLLAMA_MODEL`               | The Ollama model to use for extraction.                                     | `llama3.1`                         |
| `OLLAMA_BASE_URL`            | The base URL of the Ollama API.                                             | `http://host.docker.internal:11434`     |
| `OPENROUTER_API_KEY`         | Your OpenRouter API key.                                                    | `your_openrouter_key_here`              |
| `OPENROUTER_MODEL`           | The OpenRouter model to use as a fallback.                                  | `meta-llama/llama-3.2-3b-instruct:free` |
| `MAX_RETRIES`                | Maximum number of repair attempts before failing completely.                | `2`                                     |
| `ENABLE_OPENROUTER_FALLBACK` | Set to `true` to enable falling back to OpenRouter if Ollama fails.         | `true`                                  |
