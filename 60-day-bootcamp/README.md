# 60-Day Bootcamp

This repository documents a 60-day journey of building various AI/ML-powered applications and services. Each project, organized by day, tackles a specific problem and demonstrates the practical application of different concepts.

The primary goal of this bootcamp is to rapidly prototype and learn by building. Each project is self-contained and includes its own documentation, dependencies, and deployment configurations.

## Table of Contents

- [Projects](#projects)
  - [Day 1-5: Foundational Services](#day-1-5-foundational-services)
  - [Day 6-7: Streaming and Scalability](#day-6-7-streaming-and-scalability)
  - [Day 8-9: Advanced LLM Capabilities](#day-8-9-advanced-llm-capabilities)
  - [Day 9-10: Practical AI Applications](#day-9-10-practical-ai-applications)
  - [Day 11-21: MLOps and Observability](#day-11-21-mlops-and-observability)
  - [Day 22-25: Prompt Engineering](#day-22-25-prompt-engineering)
  - [Day 26-55: LLM Agents, Middleware, and Finetuning](#day-26-55-llm-agents-middleware-and-finetuning)
  - [Day 56-60: Speech-to-Text](#day-56-60-speech-to-text)
- [License](#license)

## Projects

### Day 1-5: Foundational Services

*   **[Async LLM Orchestrator](./day-1-5/async_llm_orchestrator/README.md):** A service designed to orchestrate asynchronous calls to various Large Language Models (LLMs).
    *   **Why we built this:** To manage the complexity of interacting with multiple LLM providers, handle concurrent requests efficiently, and provide a unified interface for downstream services.
*   **[Profile Enricher](./day-1-5/profile-enricher/README.md):** A FastAPI-based microservice that takes a user's profile, validates it, and enriches it with additional information.
    *   **Why we built this:** To demonstrate data enrichment patterns, where initial data is augmented from external sources, a common task in building comprehensive user profiles.

### Day 6-7: Streaming and Scalability

*   **[Streaming LLM API](./day-6-7/streaming-llm-api/README.md):** A production-grade RESTful API for interacting with LLMs, with a focus on streaming responses.
    *   **Why we built this:** To provide a real-time, responsive user experience in chat-like applications by streaming tokens from the LLM as they are generated, rather than waiting for the full response.

### Day 8-9: Advanced LLM Capabilities

*   **[Function Calling Demo](./day-8-9/function-calling-demo/README.md):** A FastAPI application demonstrating an enterprise-grade function calling system with an LLM.
    *   **Why we built this:** To showcase how LLMs can be used to call external tools and APIs, enabling them to interact with the real world and perform actions beyond text generation.

### Day 9-10: Practical AI Applications

*   **[Invoice Extraction Demo](./day-9-10/invoice-extraction-demo/README.md):** An enterprise-grade solution for extracting structured data from unstructured invoice text using LLMs.
    *   **Why we built this:** To solve the common business problem of digitizing and structuring data from documents like invoices, reducing manual data entry and errors.

### Day 11-21: MLOps and Observability

*   **[AI Observability](./day-11-21/ai-observability/README.md):** A basic setup for AI observability using Prometheus and Grafana.
    *   **Why we built this:** To establish a foundation for monitoring AI applications, tracking performance metrics, and visualizing model behavior, which are crucial for maintaining production-grade AI systems.

### Day 22-25: Prompt Engineering

*   **[Prompt Engineering Demo](./day-22-25/prompt_engineering_demo/README.md):** A FastAPI application for experimenting with and demonstrating various prompt engineering strategies.
    *   **Why we built this:** To explore and showcase how different prompt engineering techniques (like Chain of Thought, ReAct, and Self-Consistency) can improve the performance and reasoning abilities of LLMs.

### Day 26-55: LLM Agents, Middleware, and Finetuning

*   **[Context Engineering](./day-26-55/context-engineering/README.md):** A Retrieval-Augmented Generation (RAG) API built with FastAPI. It allows users to ingest documents, chunk them, and perform semantic searches.
    *   **Why we built this:** To provide a robust and scalable solution for building RAG pipelines, with a focus on different chunking strategies and a modern tech stack.
*   **[LangChain Streaming with SSE](./day-26-55/langchain-streaming-sse/README.md):** A project demonstrating real-time LLM token streaming using Server-Sent Events (SSE) with FastAPI and LangChain.
    *   **Why we built this:** To showcase how to build a responsive, real-time application that streams data from a large language model to a client.
*   **[LLM Finetune](./day-26-55/llm-finetune/README.md):** A project demonstrating various techniques for finetuning Large Language Models.
*   **[LLM Middleware with FastAPI](./day-26-55/llm-middleware-fastapi/README.md):** A project demonstrating how to build a FastAPI application with a custom middleware for processing requests and a simple LangGraph agent.
    *   **Why we built this:** To showcase a simple example of how to add custom middleware to a FastAPI application to process incoming requests and add context to them.
*   **[LLM Simple Agent](./day-26-55/llm-simple-agent/README.md):** A simple demonstration of a tool-calling agent built with LangChain and FastAPI. The agent is capable of understanding user queries and routing them to the appropriate tool, either a calculator or a web search tool.
    *   **Why we built this:** To illustrate the concept of LLM agents and how they can use external tools to perform actions.
*   **[Whisper Finetune](./day-26-55/whisper-finetune/README.md):** A project demonstrating fine-tuning of the OpenAI Whisper model for speech-to-text transcription.

### Day 56-60: Speech-to-Text

*   **[Whisper API](./day-56-60/whisper-api/README.md):** A high-performance, CPU-based Speech-to-Text API using the `faster-whisper` library and FastAPI. It is designed for efficient transcription of audio files.
    *   **Why we built this:** To provide a solution for fast and accurate speech-to-text transcription that can run on commodity hardware.

Each project within the day-specific folders has its own `README.md` with detailed setup and usage instructions.

## License

This project is licensed under the MIT License.