# tests/test_embeddings.py
import pytest
from src.utils.embeddings import VectorEncoder

@pytest.fixture(scope="module")
def encoder():
    return VectorEncoder()

def test_embedding_dimensions(encoder):
    text = "Hello world"
    vector = encoder.encode_single(text)
    assert len(vector) == 384  # MiniLM dimension
    assert isinstance(vector, list)
    assert isinstance(vector[0], float)

def test_batch_encoding(encoder):
    texts = ["Hello", "World", "Python"]
    vectors = encoder.encode(texts)
    assert len(vectors) == 3
    assert len(vectors[0]) == 384

def test_empty_input(encoder):
    vectors = encoder.encode([])
    assert vectors == []

def test_semantic_logic(encoder):
    vec_king = encoder.encode_single("King")
    vec_queen = encoder.encode_single("Queen")
    vec_car = encoder.encode_single("Car")
    
    from sklearn.metrics.pairwise import cosine_similarity
    import numpy as np
    
    sim_king_queen = cosine_similarity([vec_king], [vec_queen])[0][0]
    sim_king_car = cosine_similarity([vec_king], [vec_car])[0][0]
    
    assert sim_king_queen > sim_king_car