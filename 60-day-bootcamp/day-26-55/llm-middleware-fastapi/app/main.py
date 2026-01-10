from fastapi import FastAPI
from app.middleware import request_context_middleware
from app.agent import run_agent
from pydantic import BaseModel

app = FastAPI()
app.middleware("http")(request_context_middleware)
class HealthResponse(BaseModel):
    status: str

@app.post("/agent/run")
async def agent_run(payload: dict):
    return await run_agent(payload)

@app.get("/health", response_model=HealthResponse)
async def health():
    return HealthResponse(status="ok")