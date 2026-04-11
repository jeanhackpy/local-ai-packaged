---
title: "AI Observability for Data Flywheel Blueprint by Weights & Biases"
source: "https://build.nvidia.com/wandb/ai-observability-for-data-flywheel"
author:
published:
created: 2026-04-05
description: "Streamline evaluation, monitoring, and optimization of AI data flywheel with Weights & Biases."
tags:
  - "clippings"
---
j

![](https://build.nvidia.com/_next/image?url=https%3A%2F%2Fassets.ngc.nvidia.com%2Fproducts%2Fapi-catalog%2Fimages%2Fai-observability-for-data-flywheel.jpg&w=3840&q=75)

## AI Observability for Data Flywheel

Streamline evaluation, monitoring, and optimization of AI data flywheel with Weights & Biases.

This blueprint extends the [NVIDIA AI Blueprint for building data flywheels](https://build.nvidia.com/nvidia/build-an-enterprise-data-flywheel) to demonstrate how observability and experiment tracking can be added to agentic AI workflows.

[Weights & Biases](https://wandb.ai/site/weave/) enhances the NVIDIA AI Blueprint for building data flywheels by providing advanced traceability for continuous model optimization with real-world data and user feedback. While the blueprint orchestrates automated evaluation and selection of models for optimal latency, cost, and enterprise-grade accuracy, Weights & Biases layers in native traceability, robust experiment tracking, version management, and visualization. The framework enables monitoring, automated retraining, and rapid iteration cycles, accelerating the transition from experimentation to production.

W&B Weave helps customers evaluate, monitor, and iterate on their AI applications to accelerate the development and deployment process. Weave also enables continuous improvement in quality, latency, cost, and safety by running comprehensive evaluations, keeping pace with new models, debugging, and monitoring production performance - all while ensuring secure collaboration.

W&B Models help train, fine-tune, govern, and manage models from experimentation to production, accelerating time to market. It boosts experiment speed and team collaboration to bring models to production faster while ensuring performance, data reliability, and security.

## Architecture Diagram

[![](https://assets.ngc.nvidia.com/products/api-catalog/ai-observability-for-data-flywheel/diagram.jpg)](https://assets.ngc.nvidia.com/products/api-catalog/ai-observability-for-data-flywheel/diagram.jpg)

## Key Features

The Weights & Biases blueprint extension achieves the following:

- Showcases how Weights & Biases integrates into the workflow to provide seamless tracing, and evaluation capabilities accelerating generative AI iteration and providing robust monitoring when in production
- Demonstrates how to bring an AI application closer to production readiness by adding W&B Weave
- Accelerates model training, fine-tuning, and governance, enabling secure, rapid production at scale with W&B Models

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
- Celery (task processing)
- Python 3.11
- Docker Compose
- Docker Engine

## Software used in this blueprint

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

Please refer to [AI Virtual Assistant for Customer Service](https://build.nvidia.com/nvidia/ai-virtual-assistant-for-customer-service) for the details on the foundational blueprint.

**Weights & Biases Technology** W&B Weave W&B Models

**3rd-Party Technologies**

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