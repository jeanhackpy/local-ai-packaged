---
created: 2026-04-05
updated: 2026-04-05
tags: [concept, data-flywheel, AI-observability, ML-pipeline]
sources: []
---

## Data Flywheel

Cycle où le système génère des données qui améliorent le modèle qui génère des données.

### Components

1. **Data Collection** : Logs, feedback, interactions
2. **Annotation/Labeling** : Human or automated
3. **Training** : Model improvement
4. **Inference** : Deployment
5. **Feedback** : Real-world signals → back to collection

### Stack NVIDIA

- **NeMo** : NVIDIA NIM microservices
- **MLRun (Iguazio)** : Serverless ML orchestration
- **W&B** : Observability + experiment tracking

### Patterns

- Continuous training
- A/B testing
- Canary deployments
- Shadow mode

### Sources

- [[sources/nvidia-omniverse-dsx-blueprint]]
- [[sources/ai-observability-data-flywheel-wandb]]
- [[sources/ai-orchestration-data-flywheel-iguazio]]

## Connexions

- [[concepts/agentic-ai]] (agentic → flywheel)
- [[concepts/AI-observability]]
