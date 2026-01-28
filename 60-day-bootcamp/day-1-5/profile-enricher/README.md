[<- Back to Main README](../../README.md)

# Profile Enricher

This project is part of a 60-day bootcamp, and this specific service is a **Profile Enricher**.

## Table of Contents

- [Features](#features)
- [Purpose](#purpose)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Local Development](#local-development)
  - [Using Docker](#using-docker)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [Future Improvements](#future-improvements)

## Features

- **User Profile Validation**: Validates incoming user profile data against a predefined schema using Pydantic, ensuring data integrity and consistency.
- **Data Enrichment**: Communicates with an external API to fetch additional information related to the user profile.
- **Resiliency**: Includes a retry mechanism with exponential backoff for external API calls, making the enrichment process more robust.
- **Concurrency Limiting**: Limits the number of concurrent requests to the external API to prevent overloading the service.

## Purpose

The Profile Enricher is a FastAPI-based microservice that takes a user's profile, validates it, and enriches it with additional information from an external service.

In many applications, there's a need to enrich user profiles with data from other sources (e.g., social media profiles, demographic data, etc.). This enrichment process can be complex and involve interacting with external services, which might be unreliable or slow.

This Profile Enricher service was built to:
- **Decouple the enrichment logic**: By creating a separate microservice, we decouple the enrichment logic from the main application.
- **Improve Scalability**: The service can be scaled independently of the main application.
- **Increase Resilience**: The built-in retry mechanism handles transient errors from the external enrichment service.
- **Centralize Enrichment**: It provides a single, centralized point for all user profile enrichment.

## Getting Started

### Prerequisites

- Python 3.8+
- Docker (optional)

### Local Development

1.  **Create a virtual environment and install dependencies**:
    ```bash
    python -m venv .profile-enricher-env
    source .profile-enricher-env/bin/activate
    pip install -r requirements.txt
    ```

2.  **Set up environment variables**:
    Copy the `.env.example` to a new file named `.env` and fill in the required values if necessary.
    ```bash
    cp .env.example .env
    ```

3.  **Run the application**:
    ```bash
    uvicorn app.main:app --reload
    ```
    The application will be running at `http://127.0.0.1:8000`.

### Using Docker

1.  **Set up environment variables**:
    Create a `.env` file as described in the local development section.

2.  **Run with Docker Compose**:
    ```bash
    docker-compose up --build
    ```
    The API will be available at `http://127.0.0.1:8000`.

## API Documentation

### Health Check (`GET /health`)

A simple endpoint to check the service's operational status.

**Endpoint:** `GET /health`

**Response:**
```json
{
  "status": "ok"
}
```

### Enrich Profile (`POST /users`)

You can test the `/users` endpoint by sending a POST request with a user profile. Here's an example using `curl`:

```bash
curl -X POST "http://127.0.0.1:8000/users" -H "Content-Type: application/json" -d '{
    "userId": "12345",
    "username": "testuser",
    "email": "testuser@example.com",
    "age": 30,
    "address": {
        "street": "123 Main St",
        "city": "Anytown",
        "state": "CA",
        "zip_code": "12345"
    },
    "signupTs": "2023-01-01T12:00:00Z"
}'
```

#### Expected Response

If the request is successful, you will receive a JSON response containing the original user data and the enrichment data from the external service.

```json
{
    "user": {
        "userId": "12345",
        "username": "testuser",
        "email": "testuser@example.com",
        "age": 30,
        "address": {
            "street": "123 Main St",
            "city": "Anytown",
            "state": "CA",
            "zip_code": "12345"
        },
        "signupTs": "2023-01-01T12:00:00Z"
    },
    "enrichment": {
        ...
    }
}
```

## Project Structure

```
.
├── .env.example
├── .gitignore
├── Dockerfile
├── README.md
├── app/
│   ├── __init__.py
│   ├── __pycache__/
│   ├── main.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── __pycache__/
│   │   ├── address.py
│   │   └── user_profile.py
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── __pycache__/
│   │   ├── enrich.py
│   │   ├── health.py
│   │   └── users.py
│   └── utils/
│       ├── __init__.py
│       ├── __pycache__/
│       ├── enrichment.py
│       └── logging.py
├── docker-compose.yml
├── .profile-enricher-env/
├── .pytest_cache/
└── requirements.txt
```
**Note:**
* The `.env.example` file serves as a template for the environment variables required by the application. Copy this file to `.env` and customize it with your specific settings.
* The `.pytest_cache` directory is automatically generated by `pytest` and contains cached information about your test runs. It is recommended to add this directory to your `.gitignore` file.

## Deployment

This application is containerized using Docker, which makes it easy to deploy to any cloud provider that supports Docker containers.

1. **Build the Docker image:**
   ```bash
   docker build -t profile-enricher .
   ```

2. **Push the Docker image to a container registry:**
   ```bash
   docker push your-container-registry/profile-enricher
   ```

3. **Configure the environment variables in your cloud provider's environment.**

4. **Deploy the container.**

## Contributing

Contributions are welcome! If you have suggestions for improvements or new features, please feel free to open an issue or submit a pull request.

## Future Improvements

*   Add more data sources for enrichment.
*   Implement asynchronous processing for enrichment requests.
*   Add authentication and authorization to the API.