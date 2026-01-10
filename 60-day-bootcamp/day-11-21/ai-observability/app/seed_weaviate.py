import requests
import time
import random

WEAVIATE_URL = "http://localhost:8080"

def create_schema():
    class_obj = {
        "class": "Document",
        "description": "A demo document",
        "vectorizer": "none", # We will provide dummy vectors
        "properties": [{"name": "text", "dataType": ["text"]}]
    }
    requests.post(f"{WEAVIATE_URL}/v1/schema", json=class_obj)

def insert_batch(count=100):
    batch = []
    for _ in range(count):
        batch.append({
            "class": "Document",
            "properties": {"text": f"This is document number {random.randint(0,999999)}"},
            "vector": [random.random() for _ in range(1536)] # Mock 1536-dim vector
        })
    
    # Weaviate Batch API
    payload = {"objects": batch}
    start = time.time()
    resp = requests.post(f"{WEAVIATE_URL}/v1/batch/objects", json=payload)
    print(f"Inserted {count} objects in {time.time()-start:.2f}s. Status: {resp.status_code}")

if __name__ == "__main__":
    try:
        create_schema()
    except:
        pass # Class might exist
        
    print("Seeding Weaviate with dummy vectors...")
    for i in range(5):
        insert_batch(100)
        time.sleep(1)