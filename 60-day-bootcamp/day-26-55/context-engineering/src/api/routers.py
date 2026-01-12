# src/api/routers.py
from fastapi import APIRouter, HTTPException
from src.models.schema import IngestRequest, IngestResponse, SearchRequest, SearchResult
import uuid

router = APIRouter()

@router.get("/health")
async def health_check():
    return {"status": "ok", "service": "context-engine"}

@router.post("/ingest", response_model=IngestResponse)
async def ingest_documents(request: IngestRequest):
    doc_ids = [doc.id for doc in request.documents]
    print(f"Received {len(request.documents)} documents for ingestion.")
    
    return IngestResponse(
        processed_count=len(request.documents),
        document_ids=doc_ids,
        status="queued"
    )

@router.post("/search", response_model=list[SearchResult])
async def search(request: SearchRequest):
    return [
        SearchResult(
            score=0.95,
            content="This is a mock result matching your query.",
            document_id=uuid.uuid4(),
            metadata={"source": "mock"}
        )
    ]