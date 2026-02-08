# Dapr Runtime Skill

This skill provides guidance and tools for designing and enforcing Dapr runtime usage in the Todo Chatbot application.

## Purpose
Design and enforce Dapr runtime usage, including:
- Configuring Pub/Sub, Jobs API, State, Secrets, and Service Invocation
- Ensuring Dapr sidecars are injected correctly in all services
- Validating multi-environment operation (Minikube → Oracle OKE)
- Collaborating with context-verifier-agent for latest Dapr practices

## Key Features
- Dapr component configuration templates
- Sidecar injection guidance
- Multi-environment validation
- Configuration validation tools
- Service communication enforcement

## Files Included
- `SKILL.md` - Main skill documentation
- `references/dapr-components.md` - Detailed configuration examples
- `scripts/validate_dapr_config.py` - Configuration validation tool
- `assets/dapr-sidecar-template.yaml` - Sidecar configuration template

## Usage
Use this skill when implementing or managing Dapr runtime configurations for the Todo Chatbot, particularly for ensuring proper service communication through Dapr APIs and validating multi-environment deployments.