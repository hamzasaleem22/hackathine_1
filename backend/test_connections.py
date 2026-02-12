#!/usr/bin/env python3
"""
Test script to validate all external service connections.
Run this to verify your .env credentials are working.
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("=" * 60)
print("🔍 Testing External Service Connections")
print("=" * 60)
print()

# Test 1: OpenAI API
print("1️⃣  Testing OpenAI API...")
try:
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    # Test embedding
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input="test connection"
    )
    print("   ✅ OpenAI API: Connected successfully")
    print(f"   📊 Embedding dimension: {len(response.data[0].embedding)}")
except Exception as e:
    print(f"   ❌ OpenAI API: Failed - {str(e)}")
    sys.exit(1)

print()

# Test 2: Qdrant
print("2️⃣  Testing Qdrant Vector Database...")
try:
    from qdrant_client import QdrantClient

    qdrant_url = os.getenv("QDRANT_URL")
    qdrant_key = os.getenv("QDRANT_API_KEY")

    client = QdrantClient(
        url=qdrant_url,
        api_key=qdrant_key,
    )

    # Test connection by listing collections
    collections = client.get_collections()
    print("   ✅ Qdrant: Connected successfully")
    print(f"   📊 Collections: {len(collections.collections)}")
except Exception as e:
    print(f"   ❌ Qdrant: Failed - {str(e)}")
    sys.exit(1)

print()

# Test 3: Neon Postgres
print("3️⃣  Testing Neon Postgres Database...")
try:
    import psycopg

    db_url = os.getenv("DATABASE_URL")

    # Connect to database
    with psycopg.connect(db_url) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT version();")
            version = cur.fetchone()[0]
            print("   ✅ Neon Postgres: Connected successfully")
            print(f"   📊 Version: {version.split(',')[0]}")
except Exception as e:
    print(f"   ❌ Neon Postgres: Failed - {str(e)}")
    sys.exit(1)

print()
print("=" * 60)
print("✅ All connections successful!")
print("=" * 60)
print()
print("Next steps:")
print("  1. Run: uvicorn api.main:app --reload")
print("  2. Visit: http://localhost:8000")
print("  3. Continue with Phase 2: Content Indexing")
