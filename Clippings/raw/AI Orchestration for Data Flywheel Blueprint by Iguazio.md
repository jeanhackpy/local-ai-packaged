---
title: "AI Orchestration for Data Flywheel Blueprint by Iguazio"
source: "https://build.nvidia.com/iguazio/ai-orchestration-for-data-flywheel"
author:
published:
created: 2026-04-05
description: "Orchestrate AI agents for data flywheel with MLRun and NVIDIA NeMo microservices."
tags:
  - "clippings"
---
j

![](https://build.nvidia.com/_next/image?url=https%3A%2F%2Fassets.ngc.nvidia.com%2Fproducts%2Fapi-catalog%2Fimages%2Fai-orchestration-for-data-flywheel.jpg&w=3840&q=75)

## AI Orchestration for Data Flywheel

Orchestrate AI agents for data flywheel with MLRun and NVIDIA NeMo microservices.

**Automate the End-to-End AIOps Lifecycle for Data Flywheels**

Continuous model optimization at scale requires constant tuning and resource management, but manual workflows struggle to keep up with shifting traffic patterns, latency targets, and infrastructure costs.

The AI Orchestration for Data Flywheel blueprint, built in collaboration with NVIDIA, extends on the [NVIDIA AI Blueprint for data flywheels](https://build.nvidia.com/nvidia/build-an-enterprise-data-flywheel). It tackles this scalability challenge by combining the Iguazio MLRun’s low-code orchestration engine with [NVIDIA NeMo microservices](https://docs.nvidia.com/nemo/microservices/latest/about/index.html). This enables a production-integrated [data flywheel](https://www.nvidia.com/en-us/glossary/data-flywheel/) that fully automates end-to-end orchestration of continuous agent optimization. It ingests real production data, evaluates performance, fine-tunes, and surfaces smaller effective models — all without heavy engineering lift.

At the core of this system is MLRun, an open-source AI orchestration framework built by Iguazio — an AI platform company acquired by QuantumBlack, AI by McKinsey, which acts as the orchestrator that glues everything together. It streamlines data collection, partitions traffic for training and evaluation, and dispatches fine-tuning or evaluation jobs using NeMo microservices - all while exposing intuitive APIs and minimizing boilerplate code.

Whether you're optimizing tool-calling accuracy or aligning domain-specific copilots, the modular architecture supports plug-and-play integration across any use cases.

## Architecture Diagram

[![](https://assets.ngc.nvidia.com/products/api-catalog/ai-orchestration-for-data-flywheel/diagram.jpg)](https://assets.ngc.nvidia.com/products/api-catalog/ai-orchestration-for-data-flywheel/diagram.jpg)

## Key Features

- Unified AIOps Orchestration: MLRun automates data flows, logging, job scheduling, finetuning and evaluation - simplifying CI/CD integration.
- Live, Low-Code Optimization: Continuously adapts models to production data with minimal effort to reduce latency, TCO, and manual tuning - while cutting boilerplate code up to 90%.
- Plug-and-Play Flexibility: Modular APIs and low-code setup integrate easily across cloud, hybrid, or on-prem stacks.
- Integrated Evaluation and Tuning: NeMo microservices exposed as simple-to-use APIs, orchestrated by MLRun, handle SFT-LoRA tuning and automated evaluations.

## Minimum System Requirements

#### Hardware Requirements

- With Self-hosted LLM Judge: 6× (NVIDIA H100 or A100 GPUs)
- With Remote LLM Judge: 2× (NVIDIA H100 or A100 GPUs)
- Minimum Memory: 1GB (512MB reserved for Elasticsearch)
- Storage: Varies based on log volume and model size
- Network: Ports 8000 (API), 9200 (Elasticsearch), 27017 (MongoDB), 6379 (Redis)

#### OS Requirements

- Ubuntu 22.04 OS

#### Software Dependencies

- Elasticsearch 8.12.2
- MongoDB 7.0
- Redis 7.2
- FastAPI (API server)
- Python 3.11
- Docker Compose
- Docker Engine

## Software Used in This Blueprint

**NVIDIA Technology**

- **NIM microservices:**
	- [llama-3.3-70b-instruct](https://build.nvidia.com/meta/llama-3_3-70b-instruct)
		- [llama-3.2-1b-instruct](https://build.nvidia.com/meta/llama-3.2-1b-instruct)
		- [llama-3.2-3b-instruct](https://build.nvidia.com/meta/llama-3.2-3b-instruct)
		- [llama-3.1-70b-instruct](https://build.nvidia.com/meta/llama-3_1-70b-instruct)
		- [llama-3.1-8b-instruct](https://build.nvidia.com/meta/llama-3_1-8b-instruct)
- **NVIDIA NeMo microservices:**
	- **NeMo Customizer**: Model finetuning
		- **NeMo Evaluator**: Model and workflow evaluation
		- **Datastore**: Stores datasets, evaluation results, fine-tuning artifacts
		- **Deployment Manager**: Deploys and experiments with candidate models
		- **Entity Store**: Unified data model and registry
		- **NIM Proxy**: Routes inference across multiple models

**Iguazio Technology** MLRun - open-source AI orchestration tool that automates and scales the end-to-end lifecycle of GenAI and ML applications across any environment.

**3rd Party Software**

- Elasticsearch
- MongoDB
- Redis
- FastAPI
- Celery

## Ethical Considerations

NVIDIA believes Trustworthy AI is a shared responsibility, and we have established policies and practices to enable development for a wide array of AI applications. When downloaded or used in accordance with our terms of service, developers should work with their supporting model team to ensure the models meet requirements for the relevant industry and use case and address unforeseen product misuse. For more detailed information on ethical considerations for the models, please see the Model Card++ Explainability, Bias, Safety & Security, and Privacy Subcards. Please report security vulnerabilities or NVIDIA AI concerns [here](https://www.nvidia.com/en-us/support/submit-security-vulnerability/).

## License

Use of the models in this blueprint is governed by the [NVIDIA AI Foundation Models Community License](https://docs.nvidia.com/ai-foundation-models-community-license.pdf).

## Terms of Use

GOVERNING TERMS: This service is governed by the [NVIDIA API Trial Terms of Service](https://assets.ngc.nvidia.com/products/api-catalog/legal/NVIDIA%20API%20Trial%20Terms%20of%20Service.pdf).