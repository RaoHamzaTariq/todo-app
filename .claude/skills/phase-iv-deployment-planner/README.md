# Phase IV Deployment Planner Skill

## Overview
The phase-iv-deployment-planner skill provides comprehensive guidance for reading Phase IV infrastructure specifications and producing multi-stage deployment plans for Kubernetes applications. The skill follows a systematic 5-stage process with safety rules and validation checkpoints.

## Components

### Core Skill
- **SKILL.md**: Main skill definition with 5-stage deployment process, safety rules, and validation checkpoints

### References
- **deployment-checklist.md**: Comprehensive checklist for deployment validation

### Scripts
- **validate-deployment-plan.sh**: Validates a Phase IV deployment plan before execution
- **generate-deployment-plan.sh**: Generates a comprehensive deployment plan from Phase IV spec

## Key Features

1. **Systematic 5-Stage Process**: Containerize → Chart → Deploy → Validate → Rollback
2. **Safety Rules**: Enforces local-only deployment constraints and AI-assisted tool usage
3. **Validation Checkpoints**: Service reachability, environment variables, MCP integration
4. **MCP Integration**: Special handling for Model Context Protocol server deployments
5. **Rollback Strategy**: Comprehensive rollback planning and validation

## Usage Scenarios

This skill is ideal for:
- Planning Kubernetes deployments from Phase IV infrastructure specifications
- Following the 5-stage deployment process with safety constraints
- Ensuring compliance with local-only deployment requirements (Minikube)
- Validating MCP server and chatbot tool integrations
- Creating comprehensive deployment plans with validation checkpoints

The skill ensures all deployments follow the required constraints while maintaining the ability to safely rollback if needed.