# 60-Day Bootcamp

This repository documents a 60-day journey of building various AI/ML-powered applications and services. Each project, organized by day, tackles a specific problem and demonstrates the practical application of different concepts.

The primary goal of this bootcamp is to rapidly prototype and learn by building. Each project is self-contained and includes its own documentation, dependencies, and deployment configurations.

## Projects

### Day 1: Foundational Services

*   **[Async LLM Orchestrator](./day-1/async_llm_orchestrator/README.md):** A service designed to orchestrate asynchronous calls to various Large Language Models (LLMs).
    *   **Why we built this:** To manage the complexity of interacting with multiple LLM providers, handle concurrent requests efficiently, and provide a unified interface for downstream services.

*   **[Profile Enricher](./day-1/profile-enricher/README.md):** A FastAPI-based microservice that takes a user's profile, validates it, and enriches it with additional information.
    *   **Why we built this:** To demonstrate data enrichment patterns, where initial data is augmented from external sources, a common task in building comprehensive user profiles.

### Day 2: Streaming and Scalability

*   **[Streaming LLM API](./day-2/streaming-llm-api/README.md):** A production-grade RESTful API for interacting with LLMs, with a focus on streaming responses.
    *   **Why we built this:** To provide a real-time, responsive user experience in chat-like applications by streaming tokens from the LLM as they are generated, rather than waiting for the full response.

### Day 3: Advanced LLM Capabilities

*   **[Function Calling Demo](./day-3/function-calling-demo/README.md):** A FastAPI application demonstrating an enterprise-grade function calling system with an LLM.
    *   **Why we built this:** To showcase how LLMs can be used to call external tools and APIs, enabling them to interact with the real world and perform actions beyond text generation.

### Day 4: Practical AI Applications

*   **[Invoice Extraction Demo](./day-4/invoice-extraction-demo/README.md):** An enterprise-grade solution for extracting structured data from unstructured invoice text using LLMs.
    *   **Why we built this:** To solve the common business problem of digitizing and structuring data from documents like invoices, reducing manual data entry and errors.

### Day 5-14: MLOps and Observability

*   **[AI Observability](./day-5-14/ai-observability/README.md):** A basic setup for AI observability using Prometheus and Grafana.
    *   **Why we built this:** To establish a foundation for monitoring AI applications, tracking performance metrics, and visualizing model behavior, which are crucial for maintaining production-grade AI systems.

### Day 15: Prompt Engineering

*   **[Prompt Engineering Demo](./day-15/prompt_engineering_demo/README.md):** A FastAPI application for experimenting with and demonstrating various prompt engineering strategies.
    *   **Why we built this:** To explore and showcase how different prompt engineering techniques (like Chain of Thought, ReAct, and Self-Consistency) can improve the performance and reasoning abilities of LLMs.

### Day 16-37: LLM Middleware

*   **[LLM Middleware with FastAPI](./day-16-37/llm-middleware-fastapi/README.md):** A project demonstrating how to build a FastAPI application with a custom middleware for processing requests and a simple LangGraph agent.
    *   **Why we built this:** To showcase a simple example of how to add custom middleware to a FastAPI application to process incoming requests and add context to them.

Each project within the day-specific folders has its own `README.md` with detailed setup and usage instructions.

```
Size	Parameters	English-only	Multilingual
tiny	39 M	✓	✓
base	74 M	✓	✓
small	244 M	✓	✓
medium	769 M	✓	✓
large	1550 M	x	✓
large-v2	1550 M	x	✓
```