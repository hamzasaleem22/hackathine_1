#!/bin/bash

API_URL="https://backend-vert-zeta-89.vercel.app"

echo "🧪 Running Smoke Tests..."
echo "================================"
echo ""

# Test 1: Health Check
echo "Test 1: Health endpoint..."
RESPONSE=$(curl -s $API_URL/)
if echo "$RESPONSE" | grep -q '"status":"ok"'; then
    echo "✅ PASS: Health check successful"
    echo "   Response: $RESPONSE"
else
    echo "❌ FAIL: Health check failed"
    echo "   Response: $RESPONSE"
    exit 1
fi
echo ""

# Test 2: CORS Headers
echo "Test 2: CORS headers..."
HEADERS=$(curl -si -X OPTIONS $API_URL/ \
    -H "Origin: https://msaleemakhtar.github.io" \
    -H "Access-Control-Request-Method: POST" 2>&1 | head -n 20)

if echo "$HEADERS" | grep -q "access-control-allow-origin"; then
    echo "✅ PASS: CORS headers present"
    ORIGIN=$(echo "$HEADERS" | grep "access-control-allow-origin" | cut -d' ' -f2- | tr -d '\r')
    echo "   Origin: $ORIGIN"
else
    echo "❌ FAIL: CORS headers missing"
    echo "   Headers: $HEADERS"
    exit 1
fi
echo ""

# Test 3: Response Time
echo "Test 3: Response time..."
START=$(date +%s%N)
curl -s $API_URL/ > /dev/null
END=$(date +%s%N)
DURATION=$(( ($END - $START) / 1000000 ))

if [ $DURATION -lt 3000 ]; then
    echo "✅ PASS: Response time ${DURATION}ms (< 3000ms)"
else
    echo "⚠️  WARN: Response time ${DURATION}ms (>= 3000ms)"
    echo "   (Cold start may cause slower first request)"
fi
echo ""

# Test 4: JSON Response Structure
echo "Test 4: JSON response structure..."
JSON_RESPONSE=$(curl -s $API_URL/)
if echo "$JSON_RESPONSE" | python3 -m json.tool > /dev/null 2>&1; then
    echo "✅ PASS: Valid JSON response"
    if echo "$JSON_RESPONSE" | grep -q '"version"'; then
        VERSION=$(echo "$JSON_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['version'])" 2>/dev/null)
        echo "   Version: $VERSION"
    fi
else
    echo "❌ FAIL: Invalid JSON response"
    exit 1
fi
echo ""

echo "================================"
echo "✅ All smoke tests passed!"
echo "================================"
echo ""
echo "📊 Summary:"
echo "   • API URL: $API_URL"
echo "   • Status: Operational"
echo "   • CORS: Configured"
echo "   • Response Time: ${DURATION}ms"
