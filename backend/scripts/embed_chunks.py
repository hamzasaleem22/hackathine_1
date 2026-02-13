#!/usr/bin/env python3
"""
Generate embeddings for content chunks using OpenAI API.

Batch-processes chunks to generate vector embeddings using
text-embedding-3-small model (1536 dimensions).
"""
import os
import sys
from pathlib import Path
from typing import List, Dict
import time
from dotenv import load_dotenv
from openai import OpenAI

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from chunk_content import process_all_files

# Load environment variables
load_dotenv()


def generate_embeddings(chunks: List[Dict], batch_size: int = 100) -> List[Dict]:
    """
    Generate embeddings for chunks in batches.

    Args:
        chunks: List of content chunks
        batch_size: Number of chunks to process per API call (max 100)

    Returns:
        List of chunks with embeddings added
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    print("=" * 60)
    print("🔢 Generating Embeddings")
    print("=" * 60)
    print(f"Total chunks: {len(chunks)}")
    print(f"Batch size: {batch_size}")
    print(f"Model: text-embedding-3-small")
    print()

    embedded_chunks = []
    failed_chunks = []

    # Process in batches
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i + batch_size]
        batch_num = (i // batch_size) + 1
        total_batches = (len(chunks) + batch_size - 1) // batch_size

        print(f"Processing batch {batch_num}/{total_batches} ({len(batch)} chunks)...")

        try:
            # Prepare texts for embedding
            texts = []
            for chunk in batch:
                # Combine heading and text for better context
                combined_text = f"{chunk['heading']}\n\n{chunk['text']}"
                texts.append(combined_text)

            # Generate embeddings
            start_time = time.time()
            response = client.embeddings.create(
                model="text-embedding-3-small",
                input=texts
            )
            elapsed = time.time() - start_time

            # Add embeddings to chunks
            for j, chunk in enumerate(batch):
                chunk['embedding'] = response.data[j].embedding
                chunk['embedding_model'] = 'text-embedding-3-small'
                chunk['embedding_dimensions'] = len(response.data[j].embedding)
                embedded_chunks.append(chunk)

            print(f"  ✅ Success: {len(batch)} embeddings in {elapsed:.2f}s")

            # Rate limiting: OpenAI has 3000 RPM limit for embeddings
            # Sleep briefly between batches to avoid rate limits
            if i + batch_size < len(chunks):
                time.sleep(0.5)

        except Exception as e:
            print(f"  ❌ Error in batch {batch_num}: {str(e)}")
            failed_chunks.extend(batch)
            continue

    print()
    print("=" * 60)
    print("📊 Embedding Summary")
    print("=" * 60)
    print(f"Successfully embedded: {len(embedded_chunks)}/{len(chunks)}")
    print(f"Failed: {len(failed_chunks)}/{len(chunks)}")

    if embedded_chunks:
        print(f"Embedding dimensions: {embedded_chunks[0]['embedding_dimensions']}")

    if failed_chunks:
        print("\n⚠️  Failed chunks:")
        for chunk in failed_chunks[:5]:  # Show first 5
            print(f"  - {chunk['metadata']['relative_path']}: {chunk['heading']}")

    return embedded_chunks


def main():
    """Main execution function."""
    # Get docs directory
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent
    docs_dir = project_root / 'frontend' / 'docs'

    # Process files and create chunks
    chunks = process_all_files(str(docs_dir))

    if not chunks:
        print("❌ No chunks to embed!")
        return []

    # Generate embeddings
    embedded_chunks = generate_embeddings(chunks, batch_size=100)

    return embedded_chunks


if __name__ == "__main__":
    main()
