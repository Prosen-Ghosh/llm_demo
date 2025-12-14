import os
import time
import requests
from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST, Counter, Histogram, Gauge

app = FastAPI(title="AI Observability Gateway")

# --- CONFIG ---
# We use an environment variable so we can change this in Docker Compose later
OLLAMA_URL = os.getenv("OLLAMA_BASE_URL", "http://host.docker.internal:11434")

# --- METRICS ---
REQUEST_COUNT = Counter('app_request_count_total', 'Total requests', ['method', 'endpoint', 'status'])
REQUEST_LATENCY = Histogram('app_request_latency_seconds', 'End-to-end latency', ['endpoint'])

# AI Specifics
LLM_TOKENS_GENERATED = Counter('llm_tokens_generated_total', 'Total tokens', ['model_name'])
LLM_TOKEN_RATE = Gauge('llm_token_rate_tps', 'Tokens per second', ['model_name'])
LLM_LOAD_TIME = Gauge('llm_model_load_seconds', 'Time to load model into VRAM', ['model_name'])
PROMPT_TOKENS = Histogram('llm_prompt_tokens_count', 'Prompt size', ['model_name'], buckets=[10, 100, 500, 1000])

# --- DATA MODELS ---
class GenerateRequest(BaseModel):
    prompt: str
    model: str = "llama3:latest" # Default model

# --- ROUTES ---

@app.get("/health")
def health():
    return {"status": "ok", "ollama_url": OLLAMA_URL}

@app.get("/metrics")
def metrics():
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.post("/generate")
def generate_text(req: GenerateRequest):
    endpoint = "/generate"
    start_time = time.time()
    
    # Payload for Ollama
    payload = {
        "model": req.model,
        "prompt": req.prompt,
        "stream": False  # We disable streaming to get the full metrics JSON at once
    }

    try:
        # 1. Call Ollama
        response = requests.post(f"{OLLAMA_URL}/api/generate", json=payload)
        response.raise_for_status()
        
        # 2. Parse Ollama's Metrics
        data = response.json()
        
        # Extract specific AI metrics
        # Ollama returns durations in NANOSECONDS. Divide by 1e9 to get Seconds.
        eval_count = data.get("eval_count", 0)
        eval_duration_ns = data.get("eval_duration", 0)
        load_duration_ns = data.get("load_duration", 0)
        prompt_eval_count = data.get("prompt_eval_count", 0)

        # 3. Update Prometheus
        LLM_TOKENS_GENERATED.labels(model_name=req.model).inc(eval_count)
        PROMPT_TOKENS.labels(model_name=req.model).observe(prompt_eval_count)
        
        # Handle Load Time (Convert ns to s)
        if load_duration_ns > 0:
            LLM_LOAD_TIME.labels(model_name=req.model).set(load_duration_ns / 1e9)
            
        # Handle TPS Calculation
        if eval_duration_ns > 0:
            # tokens / (nanoseconds / 1 billion)
            tps = eval_count / (eval_duration_ns / 1e9)
            LLM_TOKEN_RATE.labels(model_name=req.model).set(tps)

        # Record Success
        REQUEST_COUNT.labels(method='POST', endpoint=endpoint, status='200').inc()
        
        if req.prompt == 'fire':
            raise Exception("Something terrible happened!")
        return {
            "response": data.get("response"),
            "meta": {
                "tokens": eval_count,
                "tps": round(tps, 2) if eval_duration_ns > 0 else 0,
                "load_time": round(load_duration_ns / 1e9, 4)
            }
        }

    except Exception as e:
        REQUEST_COUNT.labels(method='POST', endpoint=endpoint, status='500').inc()
        raise HTTPException(status_code=500, detail=str(e))
        
    finally:
        duration = time.time() - start_time
        REQUEST_LATENCY.labels(endpoint=endpoint).observe(duration)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)