#!/bin/bash
# T027C: Smoke test for /api/query endpoint

echo "=== Running Smoke Test for /api/query endpoint ==="

# Start FastAPI dev server in background
echo "Starting FastAPI server..."
source .venv/bin/activate
uvicorn api.main:app --host 127.0.0.1 --port 8000 &
SERVER_PID=$!

# Wait for server to start
echo "Waiting for server to start..."
sleep 3

# Test query endpoint
echo -e "\n1. Testing /api/query endpoint..."
RESPONSE=$(curl -s -X POST http://127.0.0.1:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What is reinforcement learning?", "session_id": "test-123"}')

echo "Response: $RESPONSE"

# Check if answer exists
if echo "$RESPONSE" | grep -q '"answer"'; then
  echo "✓ Answer field present"
else
  echo "✗ Answer field missing"
fi

# Check if citations exist
if echo "$RESPONSE" | grep -q '"citations"'; then
  echo "✓ Citations field present"
else
  echo "✗ Citations field missing"
fi

# Kill server
echo -e "\nShutting down server..."
kill $SERVER_PID 2>/dev/null

echo -e "\n=== Smoke Test Complete ==="
