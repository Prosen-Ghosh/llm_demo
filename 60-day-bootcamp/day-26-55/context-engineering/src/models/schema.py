# src/models/schema.py
from pydantic import BaseModel, Field, UUID4
from typing import List, Dict, Any
from datetime import datetime, timezone
import uuid

class Document(BaseModel):
    id: UUID4 = Field(default_factory=uuid.uuid4)
    title: str = Field(..., min_length=1)
    content: str = Field(..., min_length=1)
    source: str = Field(default="manual", description="Source of the document (e.g., 'pdf', 'web')")
    created_at: datetime = Field(default_factory=datetime.now(timezone.utc))
    metadata: Dict[str, Any] = Field(default_factory=dict)

class Chunk(BaseModel):
    id: UUID4 = Field(default_factory=uuid.uuid4)
    document_id: UUID4
    content: str
    chunk_index: int
    embedding: List[float] | None = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

class IngestRequest(BaseModel):
    documents: List[Document]

class IngestResponse(BaseModel):
    processed_count: int
    document_ids: List[UUID4]
    status: str = "success"

class SearchRequest(BaseModel):
    query: str = Field(..., min_length=1)
    limit: int = Field(default=5, ge=1, le=100)
    filters: Dict[str, Any] | None = None

class SearchResult(BaseModel):
    score: float
    content: str
    document_id: UUID4
    metadata: Dict[str, Any]