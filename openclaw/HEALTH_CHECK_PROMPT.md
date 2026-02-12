# OpenClaw Environment Health Check

Hey OpenClaw! 👋

I need you to perform a comprehensive health check of your environment and report back on everything you have access to. Please verify and report on the following:

## 1. 🔧 Core Configuration Check

Please verify these configuration files exist and are valid:
- `~/.openclaw/openclaw.json` - Main configuration
- `~/.openclaw/routing-config.json` - Routing configuration
- `~/.openclaw/Dockerfile` - Container configuration

Report any JSON syntax errors or missing fields.

## 2. 🤖 Model Providers & Access

Test connectivity to all configured AI providers:

**Cloud Providers:**
- ✅ NVIDIA (https://integrate.api.nvidia.com/v1) - Kimi K2.5
- ✅ OpenRouter (https://openrouter.ai/api/v1) - Free models
- ✅ Ollama Cloud (https://api.ollama.com/v1) - Cloud models

**Local Providers:**
- ✅ Ollama Local (http://ollama:11434/v1) - nomic-embed-text only

For each provider, test:
1. API connectivity (can you reach the endpoint?)
2. Authentication (are credentials valid?)
3. List available models
4. Test a simple completion/embeddings call

## 3. 🗄️ Database Connections

Test connectivity to all databases:

- ✅ **Supabase** (PostgreSQL) at `http://kong:8000`
  - Test REST API with service key
  - Test direct PostgreSQL connection on port 5432
  
- ✅ **Qdrant** (Vector DB) at `http://qdrant:6333`
  - List collections
  - Test vector search
  
- ✅ **Neo4j** (Graph DB) at `bolt://neo4j:7687`
  - Test Bolt protocol connection
  - Run a simple Cypher query

Report connection status and any authentication errors.

## 4. 🛠️ Service Integrations

Test connectivity to integrated services:

- ✅ **n8n** (Workflows) at `http://n8n:5678`
  - Check health endpoint
  - List available workflows if possible
  
- ✅ **Crawl4AI** (Web Crawling) at `http://crawl4ai:11235`
  - Test API connectivity
  - Verify crawling capability

- ✅ **Open WebUI** at `http://open-webui:8080`
  - Check if accessible

## 5. 🎯 Skills Check

Verify all enabled skills are working:

**Currently Enabled:**
- clawhub
- obsidian
- skill-creator
- coding-agent
- ddg-search
- blogwatcher
- notion
- bird
- summarize
- session-logs
- model-usage
- oracle
- gog
- gifgrep
- github
- tmux
- sag
- sherpa-onnx-tts
- gemini
- nano-pdf
- mcporter
- healthcheck
- crawl4ai
- supabase-client
- qdrant-client
- neo4j-client
- n8n-client

For each skill:
1. Check if skill files exist
2. Verify dependencies are available
3. Test basic functionality

## 6. 🔐 Environment Variables

Check these critical environment variables are set:

**API Keys:**
- OPENROUTER_API_KEY
- NVIDIA_API_KEY
- OLLAMA_API_KEY
- OPENCLAW_GATEWAY_TOKEN
- SERPER_API_KEY
- TELEGRAM_BOT_TOKEN

**Service URLs:**
- SUPABASE_URL
- SUPABASE_KEY
- QDRANT_URL
- NEO4J_URL
- NEO4J_AUTH
- N8N_URL
- CRAWL4AI_URL
- POSTGRES_HOST/PORT/USER/PASSWORD

**Ollama:**
- OLLAMA_HOST
- OLLAMA_CLOUD_URL

Report any missing or empty variables.

## 7. 🌐 Gateway Status

Verify your gateway is operational:
- Port 18789 (Gateway) - should respond to requests
- Port 18790 (Control UI) - should serve web interface
- Health check endpoint

## 8. 📊 Resource Usage

Check system resources:
- Memory usage
- Disk space
- Network connectivity
- Docker container status

## 📋 Report Format

Please provide a detailed report with:

```
✅ WORKING - [Service/Feature] - Brief description
⚠️  WARNING - [Service/Feature] - Issue description + recommendation
❌ ERROR - [Service/Feature] - Error details + fix needed
🔧 MISSING - [Service/Feature] - What's missing
```

## 🎯 Priority Fixes

After your check, identify:
1. **Critical errors** that prevent functionality
2. **Warnings** that should be addressed
3. **Missing configurations** needed for full operation
4. **Optimization opportunities**

Please run this comprehensive check and give me the full report so we can fix any remaining issues! 🔍
