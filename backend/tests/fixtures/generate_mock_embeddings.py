"""
Generate mock embeddings for test questions.

This script creates pre-computed mock embeddings to avoid OpenAI API calls during testing.
Uses pure Python (no NumPy dependency).
"""
import json
import random
import math
from pathlib import Path

# Configuration
EMBEDDING_DIM = 1536  # OpenAI text-embedding-3-small dimension
OUTPUT_FILE = Path(__file__).parent / "mock_embeddings.json"
QUESTIONS_FILE = Path(__file__).parent / "sample_questions.json"


def generate_mock_embeddings():
    """
    Generate deterministic mock embeddings for test questions.

    Uses a simple hash-based approach to create consistent embeddings
    that won't change between test runs.
    """
    # Load questions
    with open(QUESTIONS_FILE, 'r') as f:
        data = json.load(f)
    questions = data['questions']

    # Generate mock embeddings (deterministic based on question ID)
    embeddings = {}

    for q in questions:
        question_id = q['id']
        question_text = q['question']

        # Create a deterministic seed from question ID
        seed = sum(ord(c) for c in question_id)
        random.seed(seed)

        # Generate random embedding
        embedding = [random.gauss(0, 1) for _ in range(EMBEDDING_DIM)]

        # L2 normalization
        norm = math.sqrt(sum(x ** 2 for x in embedding))
        embedding = [x / norm for x in embedding]

        embeddings[question_id] = embedding

    # Save embeddings as JSON
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(embeddings, f)

    print(f"Generated {len(embeddings)} mock embeddings")
    print(f"Saved to: {OUTPUT_FILE}")
    print(f"Embedding dimension: {EMBEDDING_DIM}")

    # Verify file
    with open(OUTPUT_FILE, 'r') as f:
        loaded = json.load(f)
    print(f"Verified: {len(loaded)} embeddings loaded successfully")


if __name__ == "__main__":
    generate_mock_embeddings()
