from fastapi import FastAPI, Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST, Counter, Histogram, Gauge
import time
import random

app = FastAPI(title="AI Observability Gateway")

REQUEST_COUNT = Counter(
    'app_request_count_total',
    'Total number of requests received',
    ['method', 'endpoint']
)

REQUEST_LATENCY = Histogram(
    'app_request_latency_seconds', 
    'Request latency in seconds',
    ['endpoint']
)

ACTIVE_REQUESTS = Gauge(
    'app_active_requests_gauge',
    'Number of requests currently in progress'
)

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "ai-gateway"}

@app.get("/metrics")
def metrics():
    """
    This endpoint is what Prometheus scrapes.
    It returns all metrics in the specific text format Prometheus understands.
    """
    data = generate_latest()
    return Response(content=data, media_type=CONTENT_TYPE_LATEST)

@app.post("/generate")
def generate_text(prompt: str):
    ACTIVE_REQUESTS.inc()

    start_time = time.time()
    try:
        time.sleep(random.uniform(0.5, 2))
        REQUEST_COUNT.labels(method='POST', endpoint='/generate').inc()

        response_text = f"Mock AI response to: {prompt}"
        return {"response": response_text }
    finally:
        duration = time.time() - start_time
        REQUEST_LATENCY.labels(endpoint='/generate').observe(duration)

        ACTIVE_REQUESTS.dec()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)