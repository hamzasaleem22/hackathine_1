"""
RAG completion service using OpenAI GPT-4o-mini.
"""
import os
from openai import OpenAI
from typing import Dict
import time


class RAGCompletionService:
    """Service for generating RAG completions using GPT-4o-mini."""

    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = "gpt-4o-mini"
        self.timeout = 30  # seconds

    def generate_completion(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.3,
        max_tokens: int = 800
    ) -> Dict:
        """
        Generate completion using GPT-4o-mini.

        Args:
            system_prompt: System instructions
            user_prompt: User question with context
            temperature: Sampling temperature (default: 0.3 for factual answers)
            max_tokens: Maximum response length (default: 800)

        Returns:
            Dict with answer text and metadata

        Raises:
            Exception: If OpenAI API call fails
        """
        start_time = time.time()

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=0.9,
                timeout=self.timeout
            )

            elapsed_ms = int((time.time() - start_time) * 1000)

            return {
                "answer": response.choices[0].message.content,
                "model": self.model,
                "response_time_ms": elapsed_ms,
                "tokens_used": response.usage.total_tokens
            }

        except Exception as e:
            raise Exception(f"OpenAI completion failed: {str(e)}")

    def generate_with_retry(
        self,
        system_prompt: str,
        user_prompt: str,
        max_retries: int = 2
    ) -> Dict:
        """
        Generate completion with retry logic.

        Args:
            system_prompt: System instructions
            user_prompt: User question with context
            max_retries: Maximum number of retry attempts (default: 2)

        Returns:
            Dict with answer and metadata

        Raises:
            Exception: If all retries fail
        """
        last_error = None

        for attempt in range(max_retries + 1):
            try:
                return self.generate_completion(system_prompt, user_prompt)
            except Exception as e:
                last_error = e
                if attempt < max_retries:
                    # Wait before retry (exponential backoff)
                    wait_time = (attempt + 1) * 2
                    time.sleep(wait_time)
                    continue

        raise Exception(f"All retry attempts failed: {str(last_error)}")
