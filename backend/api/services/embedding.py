"""
Embedding generation service using OpenAI API.
"""
import os
from openai import OpenAI
from typing import List


class EmbeddingService:
    """Service for generating embeddings using OpenAI text-embedding-3-small."""

    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = "text-embedding-3-small"
        self.dimensions = 1536

    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for a single text.

        Args:
            text: Input text to embed

        Returns:
            List of floats representing the embedding vector

        Raises:
            Exception: If OpenAI API call fails
        """
        try:
            response = self.client.embeddings.create(
                model=self.model,
                input=text
            )
            return response.data[0].embedding

        except Exception as e:
            raise Exception(f"Failed to generate embedding: {str(e)}")

    def generate_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts in one API call.

        Args:
            texts: List of input texts (max 100)

        Returns:
            List of embedding vectors

        Raises:
            Exception: If OpenAI API call fails
        """
        if len(texts) > 100:
            raise ValueError("Maximum 100 texts per batch")

        try:
            response = self.client.embeddings.create(
                model=self.model,
                input=texts
            )
            return [item.embedding for item in response.data]

        except Exception as e:
            raise Exception(f"Failed to generate embeddings batch: {str(e)}")
