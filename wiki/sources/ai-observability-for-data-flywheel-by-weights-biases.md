---
created: 2026-04-05
tags:
  - "rag"
  - "ai-observability"
  - "data-flywheel"
  - "nvidia-blueprint"
  - "weights-biases"
---

# AI Observability for Data Flywheel Blueprint

Streamline evaluation, monitoring, and optimization of AI data flywheel with Weights & Biases.

This blueprint extends the [NVIDIA AI Blueprint for building data flywheels]( to demonstrate how observability and experiment tracking can be added to agentic AI workflows.

## Overview

[W&B Weave]( enhances the NVIDIA AI Blueprint for building data flywheels by providing advanced traceability for continuous model optimization with real-world data and user feedback. While the blueprint orchestrates automated evaluation and selection of models for optimal latency, cost, and enterprise-grade accuracy, Weights & Biases layers in native traceability, robust experiment tracking, version management, and visualization.

## Key Components

### W&B Weave
- Evaluate, monitor, and iterate on AI applications
- Continuous improvement in quality, latency, cost, and safety
- Comprehensive evaluations with new models
- Debugging and production monitoring
- Secure collaboration

### W&B Models
- Train, fine-tune, govern, and manage models
- Experiment speed and team collaboration
- Performance, data reliability, and security

## NVIDIA NeMo Microservices Used

- **NeMo Customizer**: Model finetuning
- **NeMo Evaluator**: Model and workflow evaluation
- **Datastore**: Stores datasets, evaluation results, fine-tuning artifacts
- **Deployment Manager**: Deploys and experiments with candidate models
- **Entity Store**: Unified data model and registry
- **NIM Proxy**: Routes inference across multiple models

## NIM Models

- llama-3.3-70b-instruct
- llama-3.2-1b-instruct
- llama-3.2-3b-instruct
- llama-3.1-70b-instruct
- llama-3.1-8b-instruct

## System Requirements

| Component | Requirement |
|-----------|-------------|
| Hardware (Self-hosted LLM Judge) | 6× NVIDIA H100 or A100 GPUs |
| Hardware (Remote LLM Judge) | 2× NVIDIA H100 or A100 GPUs |
| Memory | 1GB minimum (512MB for Elasticsearch) |
| OS | Ubuntu 22.04 |
| Ports | 8000 (API), 9200 (Elasticsearch), 27017 (MongoDB), 6379 (Redis) |

## Software Stack

- Elasticsearch 8.12.2
- MongoDB 7.0
- Redis 7.2
- FastAPI
- Celery
- Python 3.11
- Docker Compose

## Related

- [[ai-orchestration-for-data-flywheel-by-iguazio]]
- [[rag-concept]]
- [[cyborg-enterprise-rag-blueprint]]

---
*Source: [NVIDIA Build](
