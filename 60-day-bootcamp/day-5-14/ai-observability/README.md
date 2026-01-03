[<- Back to Main README](../../README.md)

# AI Observability

This directory contains a basic setup for AI observability using Prometheus and Grafana, designed to monitor AI applications.

## Table of Contents
- [Purpose](#purpose)
- [Components](#components)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Configuration](#configuration)
- [Simulated RAG Pipeline](#simulated-rag-pipeline)
- [The `app` Directory](#the-app-directory)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [Future Improvements](#future-improvements)

## Purpose

The main purpose of this project is to provide a simple, ready-to-use stack for monitoring and visualizing metrics from AI applications. In a production environment, it is crucial to have insight into the performance, resource usage, and behavior of your AI models. This setup provides the foundational tools to collect and analyze that data.

## Components

*   **Prometheus**: A monitoring and alerting toolkit. It scrapes and stores time-series data. The configuration is in `prometheus/prometheus.yml`.
*   **Grafana**: A visualization and analytics software. It allows you to query, visualize, alert on, and explore your metrics. It can be connected to Prometheus as a data source.
*   **Docker Compose**: The `docker-compose.yml` file is used to orchestrate the deployment of Prometheus and Grafana containers.
*   **Ollama Exporter**: A custom exporter that scrapes metrics from an Ollama instance and exposes them in a format that Prometheus can understand. This is useful for monitoring the performance and resource usage of your local AI models.
*   **Weaviate**: A vector database used to store and retrieve vector embeddings. In this project, it's a standalone component for demonstrating database observability.
*   **weaviate-seed**: A service that seeds the Weaviate database with initial data.
*   **Loki**: A log aggregation system designed to store and query logs from all your applications and infrastructure.
*   **Promtail**: An agent that ships the contents of local logs to a private Loki instance.

## Project Structure

```
.
├── docker-compose.yml
├── README.md
├── grafana/
│   └── ... (Grafana data and configuration will be stored here)
├── prometheus/
│   ├── prometheus.yml
│   └── rules.yml
├── ollama-exporter/
│   ├── Dockerfile
│   ├── exporter.py
│   └── requirements.txt
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── seed_weaviate.py
│   └── utils.py
├── Dockerfile.seed
└── load_test.sh
```

## Getting Started

To get started, you will need to have Docker and Docker Compose installed.

### Prerequisites

*   **Ollama**: This project assumes you have Ollama installed and running on your host machine. Please see the [Ollama documentation](https://ollama.ai/) for installation instructions.

### Steps

1.  **Start the services:**
    ```bash
    docker-compose up -d
    ```

    This will start Prometheus, Grafana, the Ollama Exporter, Weaviate, and the weaviate-seed service.

2.  **Access Grafana:**
    Grafana will be available at [http://localhost:3000](http://localhost:3000). The default credentials are `admin`/`admin`.

3.  **Access Prometheus:**
    Prometheus will be available at [http://localhost:9090](http://localhost:9090). You should see the `ollama_exporter` and `weaviate` targets in the "Targets" section.

4.  **Access Weaviate:**
    Weaviate will be available at [http://localhost:8080](http://localhost:8080).
    
5.  **Access Loki:**
    Loki will be available at [http://localhost:3100](http://localhost:3100).

## Simulated RAG Pipeline

This project includes a **simulated** RAG (Retrieval-Augmented Generation) pipeline for demonstration purposes. The primary goal of this simulation is to generate realistic metrics for the observability stack (Prometheus and Grafana) without the complexity of a full RAG implementation.

*   **`/rag_generate` endpoint:** An endpoint in `app/main.py` that takes a prompt and uses a `mock_rag_pipeline` to simulate the steps of a RAG pipeline (embedding and retrieval).
*   **Metric Generation:** The mock pipeline generates realistic latency and metrics for each step of the RAG process, which can be visualized in Grafana.
*   **No Real Retrieval:** It's important to note that this simulation **does not** actually perform retrieval from the Weaviate database. The Weaviate instance in this project is a standalone component to demonstrate database monitoring.

## The `app` Directory

The `app` directory contains the source code for the FastAPI application that acts as a gateway to the Ollama service and generates metrics for the observability stack.

*   `main.py`: The entry point of the FastAPI application. It defines the API endpoints, including `/generate` and `/rag_generate`, and exposes Prometheus metrics at the `/metrics` endpoint.
*   `seed_weaviate.py`: A script that creates a schema in Weaviate and inserts dummy data. This is run as a separate service to seed the Weaviate database.
*   `utils.py`: Contains the `mock_rag_pipeline` function, which simulates the steps of a RAG pipeline and records Prometheus metrics.

## Configuration

*   **Prometheus (`prometheus/prometheus.yml`):**
    This file configures the scrape targets for Prometheus. By default, it is configured to scrape itself, the Ollama Exporter, and Weaviate.

*   **Prometheus Rules (`prometheus/rules.yml`):**
    This file contains alerting and recording rules for Prometheus.

*   **Grafana (`grafana/`):**
    Grafana's configuration and data are persisted in this directory. You can add dashboard configurations here.

*   **Promtail (`app/loki/promtail-config.yml`):**
    This file configures Promtail to read logs from the application and send them to Loki.

## Deployment

This setup is designed to be deployed using Docker Compose. You can run the `docker-compose up -d` command on any server with Docker and Docker Compose installed. For a production setup, you would typically run this on a dedicated monitoring server.

## Contributing

Contributions are welcome! If you have suggestions for improving this setup, please feel free to open an issue or submit a pull request.

## Future Improvements

*   Add pre-built Grafana dashboards for common AI metrics.
*   Include Alertmanager for proactive alerting on key metrics.
*   Provide examples of how to instrument an AI application to expose Prometheus metrics.
*   Replace the mock RAG pipeline with a real implementation.