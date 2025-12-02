# 60-Day Bootcamp: Profile Enricher

This project is part of a 60-day bootcamp, and this specific service is a **Profile Enricher**.

## 🚀 Getting Started

1.  **Navigate to the project directory**: `cd 60-day-bootcamp/day-1/profile-enricher`
2.  **Setup**: Create a virtual environment, install dependencies from `requirements.txt`.
3.  **Environment Variables**: Copy `.env.example` to `.env`.
4.  **Run**: Execute `uvicorn app.main:app --reload` to start the application.

## What does this codebase do?

The Profile Enricher is a FastAPI-based microservice that takes a user's profile, validates it, and enriches it with additional information from an external service.

The core functionalities include:
- **User Profile Validation**: It validates the incoming user profile data against a predefined schema using Pydantic. This ensures data integrity and consistency.
- **Data Enrichment**: It communicates with an external API to fetch additional information related to the user profile.
- **Resiliency**: It includes a retry mechanism with exponential backoff for the external API calls, making the enrichment process more robust and resilient to transient failures.
- **Concurrency Limiting**: It limits the number of concurrent requests to the external API to prevent overloading the service.

## Why did we build this and what purpose does it serve?

In many applications, there's a need to enrich user profiles with data from other sources (e.g., social media profiles, demographic data, etc.). This enrichment process can be complex and involve interacting with external services, which might be unreliable or slow.

This Profile Enricher service was built to:
- **Decouple the enrichment logic**: By creating a separate microservice, we decouple the enrichment logic from the main application. This makes the main application simpler and more focused on its core responsibilities.
- **Improve Scalability**: The service can be scaled independently of the main application, allowing for better resource management.
- **Increase Resilience**: The built-in retry mechanism with exponential backoff helps to handle transient errors from the external enrichment service, making the overall system more reliable.
- **Centralize Enrichment**: It provides a single, centralized point for all user profile enrichment, which is easier to maintain and update.

## How to test the feature/API?

To test the Profile Enricher API, you first need to set up and run the application.

### 1. Setup

1.  **Navigate to the project directory**:
    ```bash
    cd 60-day-bootcamp/day-1/profile-enricher
    ```

2.  **Create a virtual environment and install dependencies**:
    ```bash
    python -m venv .profile-enricher-env
    source .profile-enricher-env/bin/activate
    pip install -r requirements.txt
    ```

3.  **Set up environment variables**:
    Copy the `.env.example` to a new file named `.env` and fill in the required values if necessary. The default values are sufficient for testing with the mock API.
    ```bash
    cp .env.example .env
    ```

4.  **Run the application**:
    ```bash
    uvicorn app.main:app --reload
    ```
    The application will be running at `http://127.0.0.1:8000`.

### 2. Testing the API

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
        ... enrichment data from the external service ...
    }
}
```

If the user profile validation fails, you will receive a `422 Unprocessable Entity` response with details about the validation errors. If the enrichment service fails, you will receive a `502 Bad Gateway` response.

## Project Structure

```
.
├── Dockerfile              # Dockerfile for building the application container.
├── README.md               # This README file.
├── app/                    # Source code for the application.
│   ├── __init__.py         #
│   ├── main.py             # Main entry point for the FastAPI application.
│   ├── models/             # Pydantic models for data validation.
│   │   ├── __init__.py
│   │   ├── address.py
│   │   └── user_profile.py
│   ├── routers/            # API routers for different endpoints.
│   │   ├── __init__.py
│   │   ├── enrich.py
│   │   ├── health.py
│   │   └── users.py
│   └── utils/              # Utility functions.
│       ├── __init__.py
│       ├── enrichment.py
│       └── logging.py
├── docker-compose.yml      # Docker Compose file for running the application.
└── requirements.txt        # Lists all Python dependencies.
```

## 🤝 Contributing

Contributions are welcome! If you have suggestions for improvements or new features, please feel free to open an issue or submit a pull request.