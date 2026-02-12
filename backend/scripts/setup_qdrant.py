#!/usr/bin/env python3
"""
Setup script to create and configure Qdrant collection.
Run this once to initialize the vector database.
"""
import os
import sys
from dotenv import load_dotenv

load_dotenv()

print("=" * 60)
print("🔧 Setting up Qdrant Collection")
print("=" * 60)
print()

try:
    import httpx

    qdrant_url = os.getenv("QDRANT_URL")
    qdrant_key = os.getenv("QDRANT_API_KEY")

    if not qdrant_url or not qdrant_key:
        print("❌ Error: QDRANT_URL or QDRANT_API_KEY not found in .env")
        sys.exit(1)

    collection_name = "physical-ai-textbook"

    # Collection configuration
    collection_config = {
        "vectors": {
            "size": 1536,  # OpenAI text-embedding-3-small dimension
            "distance": "Cosine"
        }
    }

    print(f"📦 Creating collection: {collection_name}")
    print(f"   Vector size: 1536")
    print(f"   Distance metric: Cosine")
    print()

    # Create collection using HTTP API
    # Try Bearer token authentication
    headers = {"Authorization": f"Bearer {qdrant_key}"}

    response = httpx.put(
        f"{qdrant_url}/collections/{collection_name}",
        json=collection_config,
        headers=headers,
        timeout=30.0
    )

    if response.status_code == 200:
        print("✅ Collection created successfully!")
        print()

        # Get collection info
        info_response = httpx.get(
            f"{qdrant_url}/collections/{collection_name}",
            headers=headers,
            timeout=10.0
        )

        if info_response.status_code == 200:
            info = info_response.json()
            print("📊 Collection Details:")
            print(f"   Status: {info['result']['status']}")
            print(f"   Vector count: {info['result']['points_count']}")
            print(f"   Indexed: {info['result']['indexed_vectors_count']}")

    elif response.status_code == 409:
        print("ℹ️  Collection already exists!")
        print()

        # Get existing collection info
        info_response = httpx.get(
            f"{qdrant_url}/collections/{collection_name}",
            headers=headers,
            timeout=10.0
        )

        if info_response.status_code == 200:
            info = info_response.json()
            print("📊 Existing Collection Details:")
            print(f"   Status: {info['result']['status']}")
            print(f"   Vector count: {info['result']['points_count']}")
            print(f"   Indexed: {info['result']['indexed_vectors_count']}")
    else:
        print(f"❌ Failed to create collection")
        print(f"   Status code: {response.status_code}")
        print(f"   Response: {response.text}")
        sys.exit(1)

    print()
    print("=" * 60)
    print("✅ Qdrant setup complete!")
    print("=" * 60)

except Exception as e:
    print(f"❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
