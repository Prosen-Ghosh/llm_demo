# src/main.py
from fastapi import FastAPI
from src.api.routers import router
import uvicorn

app = FastAPI(
    title="Context Engineering RAG API",
    version="0.1.0",
    description="API for ingesting documents and performing RAG operations."
)

app.include_router(router, prefix="/api/v1")

if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)