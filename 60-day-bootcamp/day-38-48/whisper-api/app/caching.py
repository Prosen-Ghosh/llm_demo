import hashlib
import logging
from collections import OrderedDict
from typing import Optional, Dict, Any
from threading import Lock

logger = logging.getLogger("whisper-api")

def compute_file_hash(file_path: str) -> str:
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

class ResultsCache:
    def __init__(self, capacity: int = 100):
        self.cache = OrderedDict()
        self.capacity = capacity
        self.lock = Lock()

    def get(self, file_hash: str) -> Optional[Dict[str, Any]]:
        with self.lock:
            if file_hash not in self.cache:
                return None
            self.cache.move_to_end(file_hash)
            logger.info(f"Cache HIT for hash: {file_hash[:8]}...")
            return self.cache[file_hash]

    def put(self, file_hash: str, result: Dict[str, Any]):
        with self.lock:
            if file_hash in self.cache:
                self.cache.move_to_end(file_hash)
            self.cache[file_hash] = result
            
            if len(self.cache) > self.capacity:
                removed_hash, _ = self.cache.popitem(last=False) # pop from start (FIFO/LRU)
                logger.info(f"Cache full. Evicted: {removed_hash[:8]}...")

results_cache = ResultsCache(capacity=100)