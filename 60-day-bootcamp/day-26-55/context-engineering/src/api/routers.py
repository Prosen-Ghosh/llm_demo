# src/api/routers.py
from fastapi import APIRouter, HTTPException
from src.models.schema import IngestRequest, IngestResponse, SearchRequest, SearchResult
import uuid
from src.utils.chunking import ChunkingService

router = APIRouter()

@router.get("/health")
async def health_check():
    return {"status": "ok", "service": "context-engine"}

@router.post("/ingest", response_model=IngestResponse)
async def ingest_documents(request: IngestRequest):
    chunker = ChunkingService(chunk_size=500, chunk_overlap=50)

    total_chunk = 0
    doc_ids = []
    for doc in request.documents:
        chunks = chunker.chunk_document(doc)

        total_chunk += len(chunks)
        doc_ids.append(doc.id)
        print(f"Doc {doc.title}: Created {len(chunks)} chunks.")
    
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