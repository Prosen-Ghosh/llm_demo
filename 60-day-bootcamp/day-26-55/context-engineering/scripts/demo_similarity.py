# scripts/demo_similarity.py
import sys
import os
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.utils.embeddings import VectorEncoder

def main():
    encoder = VectorEncoder()
    print(f"Model dimensions: {encoder.embedding_dim}")

    sentences = [
        "The cat sits on the mat.",       # 0: Anchor
        "A kitten is resting on a rug.",   # 1: Semantically similar to 0
        "The dog chases the ball.",        # 2: Different topic
        "I love coding in Python.",        # 3: Completely unrelated
        "The mat sits on the cat."         # 4: Same words, different meaning (Word2Vec fails here, Transformers succeed)
    ]

    print("\n--- Generating Embeddings ---")
    vectors = encoder.encode(sentences)

    vec_np = np.array(vectors)

    similarity_matrix = cosine_similarity(vec_np)
    print("\n--- Semantic Similarity Analysis ---")
    anchor_idx = 0
    print(f"Anchor Sentence: '{sentences[anchor_idx]}'\n")

    for i in range(len(sentences)):
        if i == anchor_idx: continue
        score = similarity_matrix[anchor_idx][i]
        print(f"Score: {score:.4f} | vs: '{sentences[i]}'")

    print("\n------------------------------------------------")
    print("INTERPRETATION:")
    print(" > 0.80 : Very similar (Paraphrases)")
    print(" 0.50-0.80 : Related topic")
    print(" < 0.30 : Unrelated")

if __name__ == "__main__":
    main()