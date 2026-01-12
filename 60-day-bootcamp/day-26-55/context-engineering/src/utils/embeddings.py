# src/utils/embeddings.py
import logging
from typing import List
from sentence_transformers import SentenceTransformer
import numpy as np

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VectorEncoder:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model_name = model_name
        logger.info(f"Loading embedding model: {model_name} on CPU...")

        try:
            self.model = SentenceTransformer(model_name, device='cpu')
            logger.info("Model loaded successfully.")
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            raise e
        
    def encode(self, texts: List[str]) -> List[List[float]]:
        if not texts:
            return []
        
        embeddings = self.model.encode(texts, convert_to_numpy=True, normalize_embeddings=True)
        return embeddings.tolist()
    
    def encode_single(self, text: str) -> List[float]:
        return self.encode([text])[0]
    
    @property
    def embedding_dim(self) -> int:
        return self.model.get_sentence_embedding_dimension()