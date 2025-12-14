# AI Observability Blueprint

## 1. Components
- **Inference Engine:** Ollama (Port 11434) running Llama3 or Mistral.
- **Backend:** FastAPI (Port 8000).
- **Vector DB:** Weaviate/Chroma (Port 8080).

## 2. Metric Strategy
- I will NOT log the actual user prompts (Privacy/Security).
- I WILL log the *length* of the prompt (Token Count).
- I WILL log the *model name* used (e.g., "llama3:latest").

## 3. Alert Thresholds (Draft)
- [ ] Alert if `llm_token_generation_rate` < 10 tokens/sec.
- [ ] Alert if `gpu_vram_usage_bytes` > 90% of Total VRAM.
- [ ] Alert if `rag_documents_retrieved_count` == 0 (Silent Failure).