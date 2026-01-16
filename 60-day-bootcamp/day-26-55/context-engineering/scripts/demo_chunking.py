# scripts/demo_chunking.py
import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models.schema import Document
from src.utils.chunking import ChunkingService

def main():
    with open("data/sample_text.txt", "r") as f:
        content = f.read()

    doc = Document(title="Chunking Strategy", content=content, source="file")
    print("--- Strategy 1: Recursive (Size=50, Overlap=10) ---")

    service = ChunkingService(chunk_size=50, chunk_overlap=10)
    chunks = service.chunk_document(doc)

    for c in chunks:
        print(f"[{c.chunk_index}] ({c.metadata['chunk_size']} toks): {c.content!r}")
        print("-" * 40)

    print("\n--- Strategy 2: Hierarchical (Parent=100, Child=30) ---")
    h_chunks = service.chunk_document_hierarchical(doc, parent_size=100, child_size=30)

    parents = [c for c in h_chunks if c.metadata.get("type") == "parent"]
    children = [c for c in h_chunks if c.metadata.get("type") == "child"]
    
    print(f"Generated {len(parents)} parents and {len(children)} children.")

    if parents:
        p = parents[0]
        print(f"\nParent {p.id} content:\n{p.content[:60]}...")
        p_children = [c for c in children if c.metadata.get("parent_id") == str(p.id)]
        for child in p_children:
             print(f"  -> Child: {child.content!r}")


if __name__ == "__main__":
    main()