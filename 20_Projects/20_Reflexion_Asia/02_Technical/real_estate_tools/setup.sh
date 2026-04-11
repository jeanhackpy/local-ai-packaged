#!/bin/bash

# Real Estate Tools - Setup Script
# Automates environment setup and validation

set -e

echo "🚀 Real Estate Tools - Setup"
echo "===================================================="
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 1. Check Python
echo -e "${BLUE}1. Checking Python...${NC}"
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found"
    exit 1
fi
PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
echo -e "${GREEN}✅ Python ${PYTHON_VERSION}${NC}"

# 2. Check SSH
echo ""
echo -e "${BLUE}2. Checking SSH...${NC}"
if ! command -v ssh &> /dev/null; then
    echo "❌ SSH not found"
    exit 1
fi
echo -e "${GREEN}✅ SSH available${NC}"

# 3. Install dependencies
echo ""
echo -e "${BLUE}3. Installing Python dependencies...${NC}"
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    echo -e "${GREEN}✅ Dependencies installed${NC}"
else
    echo "❌ requirements.txt not found"
    exit 1
fi

# 4. Create .env file if not exists
echo ""
echo -e "${BLUE}4. Checking environment configuration...${NC}"
if [ ! -f ".env" ] && [ -f ".env.example" ]; then
    cp .env.example .env
    echo -e "${YELLOW}⚠️  .env created from template - please configure${NC}"
elif [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚠️  No .env file found - create one with database credentials${NC}"
else
    echo -e "${GREEN}✅ .env file exists${NC}"
fi

# 5. Verify Supabase connection
echo ""
echo -e "${BLUE}5. Connection test (manual)...${NC}"
echo -e "${YELLOW}To test SSH tunnel:${NC}"
echo "  ssh -L 3000:127.0.0.1:8000 phil@31.97.67.145 \"sleep 600\" &"
echo ""
echo -e "${YELLOW}To verify tunnel:${NC}"
echo "  lsof -i :3000"
echo ""

# 6. Display next steps
echo -e "${GREEN}===================================================${NC}"
echo -e "${GREEN}✅ Setup complete!${NC}"
echo -e "${GREEN}===================================================${NC}"
echo ""
echo "📝 Next steps:"
echo ""
echo "1. Configure .env with your database credentials:"
echo "   nano .env"
echo ""
echo "2. Start SSH tunnel:"
echo "   ssh -L 3000:127.0.0.1:8000 phil@31.97.67.145 \"sleep 600\" &"
echo ""
echo "3. View your listings:"
echo "   open viewers/listings_with_photos.html"
echo ""
echo "4. Extract image tags (optional):"
echo "   python3 scripts/image_tagging_pipeline.py"
echo ""
echo "5. Search API:"
echo "   python3 scripts/search_api.py"
echo ""
echo "📚 For more info, see: README.md"
echo ""
