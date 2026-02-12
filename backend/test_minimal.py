#!/usr/bin/env python3
"""
Minimal connection tests that work with Python 3.14
"""
import os
from dotenv import load_dotenv

load_dotenv()

print("=" * 60)
print("🔍 Testing Service Credentials")
print("=" * 60)
print()

# Test 1: OpenAI
print("1️⃣  OpenAI API")
try:
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    response = client.embeddings.create(
        model="text-embedding-3-small",
        input="test"
    )
    print("   ✅ CONNECTED - Embedding dimension:", len(response.data[0].embedding))
except Exception as e:
    print(f"   ❌ FAILED: {str(e)[:100]}")

print()

# Test 2: Qdrant (HTTP test)
print("2️⃣  Qdrant Vector Database")
try:
    import httpx

    qdrant_url = os.getenv("QDRANT_URL")
    qdrant_key = os.getenv("QDRANT_API_KEY")

    # Simple HTTP health check
    response = httpx.get(
        f"{qdrant_url}",
        headers={"api-key": qdrant_key},
        timeout=10.0
    )
    print(f"   ✅ CONNECTED - HTTP Status: {response.status_code}")
except Exception as e:
    print(f"   ❌ FAILED: {str(e)[:100]}")

print()

# Test 3: Neon Postgres
print("3️⃣  Neon Postgres Database")
try:
    import psycopg

    db_url = os.getenv("DATABASE_URL")
    with psycopg.connect(db_url) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT version();")
            version = cur.fetchone()[0]
            print(f"   ✅ CONNECTED - {version.split(',')[0]}")
except Exception as e:
    print(f"   ❌ FAILED: {str(e)[:100]}")

print()
print("=" * 60)
print("✅ Credential validation complete!")
print("=" * 60)
