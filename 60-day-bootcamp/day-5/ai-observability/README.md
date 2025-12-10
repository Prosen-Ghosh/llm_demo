# AI Observability

This directory contains a basic setup for AI observability using Prometheus and Grafana.

## Components

*   **Prometheus**: A monitoring and alerting toolkit. It scrapes and stores time-series data. The configuration is in `prometheus/prometheus.yml`.
*   **Grafana**: A visualization and analytics software. It allows you to query, visualize, alert on, and explore your metrics. It can be connected to Prometheus as a data source.
*   **Docker Compose**: The `docker-compose.yml` file is used to orchestrate the deployment of Prometheus and Grafana containers.

## Getting Started

To get started, you will need to have Docker and Docker Compose installed.

1.  **Start the services:**
    ```bash
    docker-compose up -d
    ```

2.  **Access Grafana:**
    Grafana will be available at [http://localhost:3000](http://localhost:3000). The default credentials are `admin`/`admin`.

3.  **Access Prometheus:**
    Prometheus will be available at [http://localhost:9090](http://localhost:9090).

## Configuration

*   **Prometheus (`prometheus/prometheus.yml`):**
    This file configures the scrape targets for Prometheus. By default, it is configured to scrape itself. You will need to add your AI application endpoints here to collect metrics.

*   **Grafana (`grafana/`):**
    Grafana's configuration and data are persisted in this directory. You can add dashboard configurations here.
