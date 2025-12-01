# Profile Enricher

This service enriches user profiles with additional information.

## APIs

### Health Check

* **GET /health**

  Returns the status of the service.

  **Example Response:**
  ```json
  {
    "status": "ok",
    "env": "development"
  }
  ```

### Create and Enrich User

* **POST /users**

  Creates a new user and enriches their profile.

  **Example Request Body:**
  ```json
  {
    "user_id": "123",
    "email": "test@example.com",
    "age": 30,
    "address": {
      "street": "123 Main St",
      "city": "Anytown",
      "state": "CA",
      "postal_code": "12345"
    }
  }
  ```

  **Example Response:**
  ```json
  {
    "user": {
      "user_id": "123",
      "email": "test@example.com",
      "age": 30,
      "address": {
        "street": "123 Main St",
        "city": "Anytown",
        "state": "CA",
        "postal_code": "12345"
      }
    },
    "enrichment": {
      "risk_score": 0.5,
      "is_adult": true,
      "postal_hash": 1234,
      "user_category": "high_value",
      "source_user_id": "123"
    }
  }
  ```

### Dummy Enrich

* **POST /dummy-enrich**

  Returns dummy enrichment data for a user.

  **Example Request Body:**
  ```json
  {
    "user_id": "123",
    "age": 30,
    "address": {
      "postal_code": "12345"
    }
  }
  ```

  **Example Response:**
  ```json
  {
    "risk_score": 0.5,
    "is_adult": true,
    "postal_hash": 1234,
    "user_category": "high_value",
    "source_user_id": "123"
  }
  ```
