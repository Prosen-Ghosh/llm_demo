# AI Observability

This directory contains a basic setup for AI observability using Prometheus and Grafana, designed to monitor AI applications.

## Table of Contents
- [Purpose](#purpose)
- [Components](#components)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Configuration](#configuration)
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

## Project Structure

```
.
├── docker-compose.yml
├── README.md
├── grafana/
│   └── ... (Grafana data and configuration will be stored here)
└── prometheus/
    └── prometheus.yml
└── ollama-exporter/
    ├── Dockerfile
    ├── exporter.py
    └── requirements.txt
```

## Getting Started

To get started, you will need to have Docker and Docker Compose installed.

1.  **Start the services:**
    ```bash
    docker-compose up -d
    ```

    This will start Prometheus, Grafana, and the Ollama Exporter.

2.  **Access Grafana:**
    Grafana will be available at [http://localhost:3000](http://localhost:3000). The default credentials are `admin`/`admin`.

3.  **Access Prometheus:**
    Prometheus will be available at [http://localhost:9090](http://localhost:9090). You should see the `ollama_exporter` target in the "Targets" section.

## Configuration

*   **Prometheus (`prometheus/prometheus.yml`):**
    This file configures the scrape targets for Prometheus. By default, it is configured to scrape itself. You will need to add your AI application endpoints here to collect metrics.

*   **Grafana (`grafana/`):**
    Grafana's configuration and data are persisted in this directory. You can add dashboard configurations here.

## Deployment

This setup is designed to be deployed using Docker Compose. You can run the `docker-compose up -d` command on any server with Docker and Docker Compose installed. For a production setup, you would typically run this on a dedicated monitoring server.

## Contributing

Contributions are welcome! If you have suggestions for improving this setup, please feel free to open an issue or submit a pull request.

## Future Improvements

*   Add pre-built Grafana dashboards for common AI metrics.
*   Include Alertmanager for proactive alerting on key metrics.
*   Provide examples of how to instrument an AI application to expose Prometheus metrics.
