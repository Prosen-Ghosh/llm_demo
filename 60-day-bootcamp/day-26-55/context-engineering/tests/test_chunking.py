# tests/test_chunking.py
import pytest
from src.utils.chunking import ChunkingService
from src.models.schema import Document

@pytest.fixture
def sample_doc():
    return Document(
        title="Test", 
        content="Word " * 200, # 200 words approx
        source="test"
    )

def test_chunk_size_strictness(sample_doc):
    # Set limit to 50 tokens
    service = ChunkingService(chunk_size=50, chunk_overlap=0)
    chunks = service.chunk_document(sample_doc)
    
    for chunk in chunks:
        token_count = service._token_len(chunk.content)
        # Allow small margin for error due to splitter behavior, but shouldn't exceed massively
        assert token_count <= 55, f"Chunk too large: {token_count}"

def test_overlap_existence():
    text = "A B C D E F G H I J"
    doc = Document(title="Alpha", content=text)
    # Size 5, Overlap 2 -> [A B C D E], [D E F G H], ...
    # 'D E' should appear in both
    service = ChunkingService(chunk_size=5, chunk_overlap=2)
    chunks = service.chunk_document(doc)
    
    # Simple check if there is content duplication
    assert len(chunks) > 1
    # Overlap check is complex to exact match due to whitespace, 
    # but we can check if total text length > original length
    total_len = sum([len(c.content) for c in chunks])
    assert total_len > len(text)

def test_hierarchical_linking(sample_doc):
    service = ChunkingService()
    chunks = service.chunk_document_hierarchical(sample_doc, parent_size=100, child_size=20)
    
    children = [c for c in chunks if c.metadata.get("type") == "child"]
    parents = [c for c in chunks if c.metadata.get("type") == "parent"]
    
    assert len(children) > 0
    assert len(parents) > 0
    
    # Check that child links to a valid parent
    first_child = children[0]
    parent_id = first_child.metadata["parent_id"]
    assert any(str(p.id) == parent_id for p in parents)