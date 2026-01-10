import random
import time
from prometheus_client import Histogram, Counter

# --- RAG SPECIFIC METRICS ---
RAG_STEP_LATENCY = Histogram('rag_step_latency_seconds', 'Latency of each step in the RAG pipeline', ['step'])
RAG_CONTEXT_SIZE = Histogram('rag_context_tokens_count', 'Number of tokens retrieved from Vector DB', buckets=[100, 500, 1000, 3000, 5000])
RAG_RETRIEVAL_COUNT = Counter('rag_documents_retrieved_total', 'Number of docs returned by vector search', ['status'])

def mock_rag_pipeline(prompt: str):
    with RAG_STEP_LATENCY.labels(step='embedding').time():
        time.sleep(random.uniform(0.1, 0.3))
    
    with RAG_STEP_LATENCY.labels(step='retrieval').time():
        time.sleep(random.uniform(0.05, 0.5))
        
        num_docs = random.randint(0, 5) # Sometimes we find 0 docs!
        context_tokens = num_docs * 300 # Approx 300 tokens per doc
        
        # Record metrics
        RAG_CONTEXT_SIZE.observe(context_tokens)
        
        if num_docs == 0:
            RAG_RETRIEVAL_COUNT.labels(status='empty').inc()
            return None, 0
        else:
            RAG_RETRIEVAL_COUNT.labels(status='success').inc()
            return f"Context from {num_docs} documents...", context_tokens