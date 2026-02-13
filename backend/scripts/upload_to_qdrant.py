#!/usr/bin/env python3
"""
Upload embedded chunks to Qdrant vector database.

Populates the physical-ai-textbook collection with embeddings and metadata.
"""
import os
import sys
import uuid
from pathlib import Path
from typing import List, Dict
from dotenv import load_dotenv
import httpx

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from embed_chunks import main as generate_embeddings_main

# Load environment variables
load_dotenv()


def upload_to_qdrant(chunks: List[Dict]) -> int:
    """
    Upload chunks with embeddings to Qdrant.

    Args:
        chunks: List of chunks with embeddings

    Returns:
        Number of successfully uploaded chunks
    """
    qdrant_url = os.getenv("QDRANT_URL")
    qdrant_key = os.getenv("QDRANT_API_KEY")
    collection_name = "physical-ai-textbook"

    if not qdrant_url or not qdrant_key:
        raise ValueError("QDRANT_URL or QDRANT_API_KEY not found in environment")

    print("=" * 60)
    print("⬆️  Uploading to Qdrant")
    print("=" * 60)
    print(f"Collection: {collection_name}")
    print(f"Total chunks: {len(chunks)}")
    print()

    headers = {"Authorization": f"Bearer {qdrant_key}"}

    # Prepare points for upload
    points = []
    for i, chunk in enumerate(chunks):
        # Generate unique ID for this chunk
        point_id = str(uuid.uuid4())

        # Prepare metadata (payload)
        payload = {
            'text': chunk['text'],
            'heading': chunk['heading'],
            'heading_level': chunk['heading_level'],
            'section_id': chunk['section_id'],
            'module_id': chunk['metadata']['module_id'],
            'chapter_id': chunk['metadata']['chapter_id'],
            'title': chunk['metadata']['title'],
            'file_path': chunk['metadata']['file_path'],
            'relative_path': chunk['metadata']['relative_path'],
            'navigation_url': chunk['metadata']['navigation_url'],
            'sidebar_position': chunk['metadata']['sidebar_position'],
            'image_references': chunk.get('image_references', []),
        }

        # Add parent section if exists
        if 'parent_section' in chunk:
            payload['parent_section'] = chunk['parent_section']

        points.append({
            'id': point_id,
            'vector': chunk['embedding'],
            'payload': payload
        })

    # Upload in batches (Qdrant recommends 100-500 points per request)
    batch_size = 100
    uploaded = 0
    failed = 0

    for i in range(0, len(points), batch_size):
        batch = points[i:i + batch_size]
        batch_num = (i // batch_size) + 1
        total_batches = (len(points) + batch_size - 1) // batch_size

        print(f"Uploading batch {batch_num}/{total_batches} ({len(batch)} points)...")

        try:
            response = httpx.put(
                f"{qdrant_url}/collections/{collection_name}/points",
                json={"points": batch},
                headers=headers,
                timeout=30.0
            )

            if response.status_code == 200:
                uploaded += len(batch)
                print(f"  ✅ Success: {len(batch)} points uploaded")
            else:
                failed += len(batch)
                print(f"  ❌ Failed: HTTP {response.status_code}")
                print(f"     Response: {response.text[:200]}")

        except Exception as e:
            failed += len(batch)
            print(f"  ❌ Error: {str(e)}")

    print()
    print("=" * 60)
    print("📊 Upload Summary")
    print("=" * 60)
    print(f"Successfully uploaded: {uploaded}/{len(points)}")
    print(f"Failed: {failed}/{len(points)}")

    return uploaded


def main():
    """Main execution function."""
    # Generate embeddings
    print("Step 1: Generating embeddings...")
    chunks = generate_embeddings_main()

    if not chunks:
        print("❌ No embedded chunks to upload!")
        return 0

    # Upload to Qdrant
    print("\nStep 2: Uploading to Qdrant...")
    uploaded = upload_to_qdrant(chunks)

    return uploaded


if __name__ == "__main__":
    main()
