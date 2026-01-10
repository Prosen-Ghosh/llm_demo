import os
import time
import requests
from fastapi import FastAPI, HTTPException, Response, Request
from pydantic import BaseModel
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST, Counter, Histogram, Gauge
from app.utils import mock_rag_pipeline, RAG_STEP_LATENCY
import uuid
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ai_gateway")

def log_with_id(message: str, request: Request = None):
    req_id = getattr(request.state, "request_id", "system")
    logger.info(f"[ReqID: {req_id}] {message}")

app = FastAPI(title="AI Observability Gateway")

@app.middleware("http")
async def add_correlation_id(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    request.state.request_id = request_id
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response

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
def generate_text(req: GenerateRequest, request: Request):
    log_with_id(f"Received prompt: {req.prompt[:10]}...", request)
    endpoint = "/generate"
    start_time = time.time()

    payload = {
        "model": req.model,
        "prompt": req.prompt,
        "stream": False 
    }

    try:
        response = requests.post(f"{OLLAMA_URL}/api/generate", json=payload)
        response.raise_for_status()
        
        data = response.json()
        eval_count = data.get("eval_count", 0)
        eval_duration_ns = data.get("eval_duration", 0)
        load_duration_ns = data.get("load_duration", 0)
        prompt_eval_count = data.get("prompt_eval_count", 0)

        LLM_TOKENS_GENERATED.labels(model_name=req.model).inc(eval_count)
        PROMPT_TOKENS.labels(model_name=req.model).observe(prompt_eval_count)
        
        if load_duration_ns > 0:
            LLM_LOAD_TIME.labels(model_name=req.model).set(load_duration_ns / 1e9)
            
        if eval_duration_ns > 0:
            tps = eval_count / (eval_duration_ns / 1e9)
            LLM_TOKEN_RATE.labels(model_name=req.model).set(tps)

        if req.prompt == 'fire':
            raise Exception("Something terrible happened!")
        
        REQUEST_COUNT.labels(method='POST', endpoint=endpoint, status='200').inc()
        
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

@app.post("/rag_generate")
def rag_generate(req: GenerateRequest):
    start = time.time()
    endpoint = "/rag_generate"
    
    try:
        context, context_tokens = mock_rag_pipeline(req.prompt)
        
        if context:
            full_prompt = f"Context: {context}\nUser: {req.prompt}"
        else:
            full_prompt = req.prompt
            
        start_gen = time.time()
        payload = {"model": req.model, "prompt": full_prompt, "stream": False}
        response = requests.post(f"{OLLAMA_URL}/api/generate", json=payload)
        data = response.json()
        
        duration_gen = time.time() - start_gen
        RAG_STEP_LATENCY.labels(step='generation').observe(duration_gen)
        return {"response": data.get("response"), "rag_meta": {"docs_found": bool(context)}}

    except Exception as e:
        REQUEST_COUNT.labels(method='POST', endpoint=endpoint, status='500').inc()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        REQUEST_LATENCY.labels(endpoint=endpoint).observe(time.time() - start)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)