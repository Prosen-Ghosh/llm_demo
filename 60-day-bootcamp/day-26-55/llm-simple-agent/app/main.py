from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
load_dotenv() 

from app.agents import run_agent

app = FastAPI(title="Simple Tool Agent")

class QueryRequest(BaseModel):
    query: str

class HealthResponse(BaseModel):
    status: str

@app.post("/ask")
async def ask_agent(request: QueryRequest):
    try:
        # Pass the query to our LangGraph agent
        answer = run_agent(request.query)
        return {"response": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def read_root():
    return {"status": "Agent is ready. Use /ask to interact."}

@app.get("/health", response_model=HealthResponse)
async def health():
    return HealthResponse(status="ok")