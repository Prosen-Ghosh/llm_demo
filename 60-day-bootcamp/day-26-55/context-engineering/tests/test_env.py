# tests/test_env.py
import pytest
from src.utils.db_checks import check_weaviate, check_postgres, check_redis, check_ollama

def test_weaviate_connection():
    assert check_weaviate() is True

def test_postgres_connection():
    assert check_postgres() is True

def test_redis_connection():
    assert check_redis() is True

def test_ollama_connection():
    assert check_ollama() is True