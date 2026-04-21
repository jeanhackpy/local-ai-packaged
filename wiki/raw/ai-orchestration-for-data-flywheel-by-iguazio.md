---
created: 2026-04-05
tags:
  - "rag"
  - "ai-orchestration"
  - "data-flywheel"
  - "mlrun"
  - "nvidia-blueprint"
---

# AI Orchestration for Data Flywheel Blueprint

Orchestrate AI agents for data flywheel with MLRun and NVIDIA NeMo microservices.

**Automate the End-to-End AIOps Lifecycle for Data Flywheels**

## Overview

Continuous model optimization at scale requires constant tuning and resource management, but manual workflows struggle to keep up with shifting traffic patterns, latency targets, and infrastructure costs.

The AI Orchestration for Data Flywheel blueprint combines [Iguazio MLRun's]( low-code orchestration engine with [NVIDIA NeMo microservices]( This enables a production-integrated data flywheel that fully automates end-to-end orchestration of continuous agent optimization.

## MLRun: The Orchestrator

[MLRun]( is an open-source AI orchestration framework built by Iguazio — acquired by QuantumBlack, AI by McKinsey. It acts as the orchestrator that:
- Streamlines data collection
- Partitions traffic for training and evaluation
- Dispatches fine-tuning or evaluation jobs using NeMo microservices
- Exposes intuitive APIs and minimizes boilerplate code

## Key Features

1. **Unified AIOps Orchestration**: MLRun automates data flows, logging, job scheduling, finetuning and evaluation - simplifying CI/CD integration.

2. **Live, Low-Code Optimization**: Continuously adapts models to production data with minimal effort to reduce latency, TCO, and manual tuning — while cutting boilerplate code up to 90%.

3. **Plug-and-Play Flexibility**: Modular APIs and low-code setup integrate easily across cloud, hybrid, or on-prem stacks.

4. **Integrated Evaluation and Tuning**: NeMo microservices exposed as simple-to-use APIs, orchestrated by MLRun, handle SFT-LoRA tuning and automated evaluations.

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
- Python 3.11
- Docker Compose

## Related

- [[ai-observability-for-data-flywheel-by-weights-biases]]
- [[rag-concept]]
- [[cyborg-enterprise-rag-blueprint]]

---
*Source: [NVIDIA Build](
