---
created: 2026-04-05
tags:
  - "rag"
  - "enterprise"
  - "security"
  - "multimodal"
  - "encryption"
  - "nvidia-blueprint"
---

# Cyborg Enterprise RAG Blueprint

Connect AI applications to multimodal enterprise data with a scalable RAG pipeline built on NVIDIA NIM microservices, enhanced with enterprise-grade vector database security through CyborgDB's encryption-in-use capabilities.

## Key Benefits

- **15x faster** multimodal PDF data extraction
- **50% fewer** incorrect answers
- **Zero plaintext exposure** of vector data

## Key Features

### Data Ingestion
- Multimodal PDF data extraction (text, tables, charts, infographics)
- Audio file ingestion support
- Custom metadata support
- Multi-collection searchability

### Vision & Language
- Opt-in Vision Language Model (VLM) Support
- Image captioning with VLMs
- Document summarization

### Search & Retrieval
- Hybrid search with dense and sparse search
- GPU-accelerated index creation and search
- Reranking to improve accuracy

### Security (CyborgDB)
- Encryption-in-use for vector embeddings
- Customer-controlled key management (BYOK/HYOK)
- Zero plaintext exposure of vector data
- Multi-tenant isolation and workload segregation

### Additional Features
- Multi-turn conversations
- Multi-session support
- Telemetry and observability
- Reflection for accuracy improvement
- Guardrailing conversations
- OpenAI-compatible APIs
- Sample user interface

## NIM Microservices Used

### Embedding & Reranking
- NeMo Retriever Llama 3.2 embedding NIM
- NeMo Retriever Llama 3.2 reranking NIM

### Parsing & Extraction
- NeMo Retriever page elements NIM
- NeMo Retriever table structure NIM
- NeMo Retriever graphic elements NIM
- PaddleOCR NIM
- NeMo Retriever parse NIM (optional)

### Generation
- Llama 3.3 Nemotron Super 49B v1 NIM
- Mixtral 8x22B instruct 0.1 (optional)

### Safety (Optional)
- Llama 3.1 NemoGuard 8B content safety NIM
- Llama 3.1 NemoGuard 8B topic control NIM

### Vision (Optional)
- Llama 3.2 11B vision instruct NIM

## System Requirements

### Docker Deployment
| Component | Requirement |
|-----------|-------------|
| GPUs | 2× H100 or 3× A100 |
| RAM | 32GB+ (additional overhead for encryption) |

### Kubernetes Deployment
| Component | Requirement |
|-----------|-------------|
| GPUs | 8× H100-80GB or 9× A100-80GB |
| RAM | 64GB+ for production workloads |

- OS: Ubuntu 22.04

## Third-Party Software

- [LangChain](
- [CyborgDB]( (PostgreSQL with pgvector and transparent encryption proxy)
- [Redis](

## Related

- [[rag-concept]]
- [[rag-plus-reranker]]
- [[ai-observability-for-data-flywheel-by-weights-biases]]

---
*Source: [NVIDIA Build](
