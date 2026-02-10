#!/bin/bash
# Test script to verify OpenClaw and all services are working

echo "=========================================="
echo "Testing OpenClaw and Service Stack"
echo "=========================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to test a service
test_service() {
    local name=$1
    local url=$2
    
    echo -n "Testing $name... "
    
    if curl -s --max-time 5 "$url" > /dev/null 2>&1; then
        echo -e "${GREEN}✓ OK${NC}"
        return 0
    else
        echo -e "${RED}✗ Failed${NC}"
        return 1
    fi
}

echo "1. Testing OpenClaw Services:"
echo "   ---------------------------"
test_service "OpenClaw Gateway" "http://localhost:18789/healthz"
test_service "OpenClaw Control UI" "http://localhost:18790"

echo ""
echo "2. Testing AI Services:"
echo "   -------------------"
test_service "Open WebUI" "http://localhost:8080"
test_service "n8n" "http://localhost:5678"
test_service "Ollama" "http://localhost:11434"

echo ""
echo "3. Testing Databases:"
echo "   -----------------"
test_service "Qdrant" "http://localhost:6333"
test_service "Neo4j HTTP" "http://localhost:7474"
test_service "Supabase Kong" "http://localhost:8000"

echo ""
echo "4. Testing Utilities:"
echo "   -----------------"
test_service "Caddy" "http://localhost"
test_service "Crawl4AI" "http://localhost:11235"

echo ""
echo "=========================================="
echo "Service Status Summary"
echo "=========================================="
docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}' | grep -E "openclaw|n8n|qdrant|neo4j|open-webui|caddy|crawl4ai"

echo ""
echo "=========================================="
echo "Testing OpenClaw Configuration"
echo "=========================================="
echo ""

# Test OpenClaw configuration
echo "Checking OpenClaw config files..."
if [ -f "openclaw/openclaw.json" ]; then
    echo -e "${GREEN}✓${NC} openclaw.json exists"
else
    echo -e "${RED}✗${NC} openclaw.json missing"
fi

if [ -f "openclaw/routing-config.json" ]; then
    echo -e "${GREEN}✓${NC} routing-config.json exists"
else
    echo -e "${RED}✗${NC} routing-config.json missing"
fi

if [ -f "openclaw/Dockerfile" ]; then
    echo -e "${GREEN}✓${NC} Dockerfile exists"
else
    echo -e "${RED}✗${NC} Dockerfile missing"
fi

echo ""
echo "Checking OpenClaw environment variables in container..."
docker exec openclaw printenv | grep -E "SUPABASE_URL|QDRANT_URL|NEO4J_URL|N8N_URL|CRAWL4AI_URL" | while read line; do
    var=$(echo $line | cut -d= -f1)
    val=$(echo $line | cut -d= -f2)
    if [ -n "$val" ]; then
        echo -e "${GREEN}✓${NC} $var is set"
    else
        echo -e "${YELLOW}!${NC} $var is empty"
    fi
done

echo ""
echo "=========================================="
echo "Testing Service Connectivity from OpenClaw"
echo "=========================================="
echo ""

# Test connections from OpenClaw container
echo "Testing Qdrant connection..."
if docker exec openclaw curl -s http://qdrant:6333 > /dev/null 2>&1; then
    echo -e "${GREEN}✓${NC} Qdrant accessible from OpenClaw"
else
    echo -e "${RED}✗${NC} Qdrant not accessible"
fi

echo "Testing Neo4j connection..."
if docker exec openclaw curl -s http://neo4j:7474 > /dev/null 2>&1; then
    echo -e "${GREEN}✓${NC} Neo4j accessible from OpenClaw"
else
    echo -e "${RED}✗${NC} Neo4j not accessible"
fi

echo "Testing n8n connection..."
if docker exec openclaw curl -s http://n8n:5678/healthz > /dev/null 2>&1; then
    echo -e "${GREEN}✓${NC} n8n accessible from OpenClaw"
else
    echo -e "${RED}✗${NC} n8n not accessible"
fi

echo "Testing Crawl4AI connection..."
if docker exec openclaw curl -s http://crawl4ai:11235 > /dev/null 2>&1; then
    echo -e "${GREEN}✓${NC} Crawl4AI accessible from OpenClaw"
else
    echo -e "${YELLOW}!${NC} Crawl4AI may not be accessible (check manually)"
fi

echo ""
echo "=========================================="
echo "Test Complete!"
echo "=========================================="
