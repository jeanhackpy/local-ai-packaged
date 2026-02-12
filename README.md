# Open Source Agentic System

An advanced, self-hosted foundation for creating autonomous agentic systems. This package combines state-of-the-art AI modules, robust databases, and powerful orchestration tools into a single, easy-to-deploy stack.

## 🚀 Core Tech Stack

- **AI & Models**:
  - **Ollama**: Local LLM inference engine.
  - **OpenClaw**: Advanced AI agent gateway with MCP (Model Context Protocol) support.
  - **Open WebUI**: User-friendly interface for interacting with models and agents.
- **Orchestration**:
  - **n8n**: Low-code workflow automation with over 400 integrations.
  - **LLM Router**: Intelligent routing between local and cloud models based on query difficulty.
- **Data & Extraction**:
  - **Crawl4ai**: Automated, NLP-powered data extraction from any website.
  - **SearXNG**: Privacy-respecting metasearch engine.
- **Databases**:
  - **Supabase (PostgreSQL)**: Main relational database and authentication.
  - **Qdrant**: High-performance vector store for RAG (Retrieval-Augmented Generation).
  - **Neo4j**: Graph database for complex relationship mapping.

## ✨ Key Features

- 🔒 **Private & Secure**: Run everything locally on your own hardware or VPS.
- 🛠️ **MCP Support**: Use the Model Context Protocol to give your agents standard access to tools and data.
- 🏪 **Skills Marketplace**: Personalize your bot using the OpenClaw skills marketplace.
- 🔌 **Plug & Play Connectivity**: Easily integrate with Telegram, Discord, WhatsApp, and more.
- 🧠 **Intelligent Routing**: Automatically switch between local models (for simple tasks/privacy) and cloud models (for complex reasoning).

## 🛠️ Installation

### Prerequisites

- **Python 3.10+**
- **Docker & Docker Desktop** (with WSL2 if on Windows)
- **Git**

### Quick Start

1. **Clone the repository**:
   ```bash
   git clone [your-repo-url]
   cd local-ai-packaged
   ```

2. **Set up environment variables**:
   Copy `.env.example` to `.env` and fill in the required secrets.
   ```bash
   cp .env.example .env
   ```

3. **Start the services**:
   Run the included startup script which handles database initialization and service orchestration.
   ```bash
   python start_services.py --profile gpu-nvidia  # Or --profile cpu
   ```

## 🤖 Using the LLM Router

The project includes a custom `router_pipe.py` for Open WebUI. This allows you to:
- **Save Costs**: Use local models (via Ollama) for simple requests and only call expensive APIs for complex ones.
- **Privacy Mode**: Toggle a switch to ensure no data ever leaves your local environment.
- **Difficulty Evaluation**: A small, fast local model (like Granite or Qwen) evaluates every query before routing.

## 🕸️ Crawl4ai Integration

Automated data extraction is handled by Crawl4ai. You can use it as a standalone service or integrate it into your n8n workflows and OpenClaw skills for real-time web intelligence.

## 📚 Documentation

For more detailed guides, check the `docs/` folder:
- **[OpenClaw & Caddy Guide](docs/OPENCLAW_CADDY_GUIDE.md)**
- **[VPS Maintenance](docs/VPS_MAINTENANCE.md)**
- **[Git Workflow](docs/GIT_WORKFLOW.md)**

## 📜 License

This project is licensed under the Apache License 2.0.
