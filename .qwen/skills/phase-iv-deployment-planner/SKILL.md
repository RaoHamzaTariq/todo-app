---
name: phase-iv-deployment-planner
description: Read Phase IV infrastructure specs and produce multi-stage deployment plans including containerization, Helm chart generation, Minikube deployment, health validation, and rollback strategies. Includes test checkpoints and safety rules. Use when planning Kubernetes deployments following the 5-stage process: containerize, chart, deploy, validate, rollback.
---

# Phase IV Deployment Planner

## Overview

This skill teaches Claude how to read Phase IV infrastructure specifications and produce a comprehensive multi-stage deployment plan for Kubernetes applications. The skill follows a systematic 5-stage process with safety rules and validation checkpoints.

## When to Use This Skill

Use this skill when:
- Planning Kubernetes deployments from Phase IV infrastructure specifications
- Following the 5-stage deployment process (containerize → chart → deploy → validate → rollback)
- Ensuring compliance with local-only deployment constraints (Minikube)
- Validating deployment invariants and safety rules
- Planning MCP server and chatbot tool integrations

## Safety Rules

### Critical Constraints
1. **No Cloud Provider Calls**: All deployments must be local using Minikube only
2. **No Manual Code Changes**: Only use AI-assisted tools (Docker AI, kubectl-ai, kagent)
3. **Respect Deployment Invariants**: Follow the spec-defined constraints
4. **Local-Only Environment**: No external dependencies or cloud services

### Validation Requirements
- Verify all images are containerized locally
- Confirm all configurations use Kubernetes-native resources
- Ensure no hardcoded secrets in manifests
- Validate all services are deployed to Minikube

## Multi-Stage Deployment Plan

### Stage 1: Containerize Apps (Use Docker AI)

**Objective**: Package applications into optimized container images using AI assistance

**Process**:
1. Analyze application codebase and dependencies
2. Generate Dockerfiles using Docker AI Gordon
3. Build container images with appropriate base images
4. Optimize images for size and security

**Commands**:
- `docker-ai analyze-project` - Analyze project for containerization
- `docker-ai generate-dockerfile` - Generate optimized Dockerfile
- `docker build -t <image-name> .` - Build the container

**Validation**:
- Dockerfile follows security best practices
- Images are appropriately sized (under 500MB for simple apps)
- All dependencies are properly included

### Stage 2: Generate Helm Charts

**Objective**: Create parameterized Helm charts for each service

**Process**:
1. Create Helm chart structure for each service
2. Parameterize configurations using values.yaml
3. Implement proper resource requests/limits
4. Add health checks and service discovery

**Chart Structure**:
```
chart-name/
├── Chart.yaml
├── values.yaml
├── templates/
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── serviceaccount.yaml
│   ├── configmap.yaml
│   └── secret.yaml
└── charts/
```

**Validation**:
- All configurations are parameterized
- Resource requests/limits are appropriate
- Security contexts are properly configured
- Values can be overridden per environment

### Stage 3: Deploy to Minikube

**Objective**: Deploy services to local Minikube cluster

**Process**:
1. Start and configure Minikube cluster
2. Install Helm charts with appropriate values
3. Monitor deployment progress
4. Verify service connectivity

**Commands**:
- `minikube start` - Start local cluster
- `helm install <release-name> <chart-path> -f values.yaml` - Deploy chart
- `kubectl get pods,services` - Verify deployments
- `kubectl-ai diagnose deployment status` - AI-assisted diagnosis

**Validation**:
- All pods are running (not pending/crashing)
- Services are accessible within cluster
- Environment variables are properly propagated

### Stage 4: Validate Health and Functionality

**Objective**: Verify deployment functionality and health

**Test Checkpoints**:

#### A. Service Reachability
- **Check**: Services are accessible via ClusterIP/NodePort
- **Method**:
  - `kubectl get svc` - Verify service endpoints
  - `kubectl port-forward` - Test external access
  - `curl` internal service endpoints
- **Success Criteria**: All services respond with expected HTTP codes

#### B. Correct Environment Variable Propagation
- **Check**: Environment variables are correctly set in pods
- **Method**:
  - `kubectl-ai show environment for pod <pod-name>`
  - `kubectl exec -it <pod> -- env` - Verify env vars
- **Success Criteria**: All required environment variables are present and correct

#### C. Chatbot Tool Invocation Through MCP
- **Check**: MCP server tools are accessible and functional
- **Method**:
  - Verify MCP server is running and accessible
  - Test MCP tool registration and invocation
  - Confirm chatbot can access MCP tools
- **Success Criteria**: MCP tools can be invoked and return expected results

**Validation Commands**:
- `kubectl-ai validate service connectivity`
- `kubectl-ai test environment propagation`
- `kubectl-ai verify mcp tool access`

### Stage 5: Rollback Strategy

**Objective**: Prepare and document rollback procedures

**Rollback Plan**:
1. **Immediate Rollback**: Use Helm rollback for failed deployments
2. **Data Preservation**: Ensure persistent data is not lost
3. **Configuration Backup**: Maintain previous configuration states
4. **Monitoring**: Track rollback success

**Commands**:
- `helm rollback <release-name> <revision>` - Rollback to previous version
- `kubectl-ai analyze rollback impact` - AI-assisted impact analysis
- `helm history <release-name>` - Check deployment history

## Sample Plan Breakdown

### Example: Todo Chatbot Deployment

**Stage 1 - Containerize**:
```
Services to containerize:
- frontend: Next.js application
- backend: FastAPI with JWT + OpenAI Agents SDK
- mcp-server: Model Context Protocol server

Process:
1. docker-ai analyze-project for each service
2. Generate optimized Dockerfiles
3. Build images: todo-frontend:v1.0, todo-backend:v1.0, mcp-server:v1.0
```

**Stage 2 - Helm Charts**:
```
Create charts:
- todo-frontend/
- todo-backend/
- mcp-server/

Parameterize:
- Image tags
- Resource limits
- Environment variables
- Service configurations
```

**Stage 3 - Deploy**:
```
Deployment sequence:
1. Start Minikube cluster
2. Install MCP server chart first
3. Install backend chart
4. Install frontend chart
5. Verify inter-service connectivity
```

**Stage 4 - Validate**:
```
Test sequence:
1. Service reachability: Confirm all services are running
2. Env var propagation: Verify JWT_SECRET, API keys are set
3. MCP integration: Test chatbot tool invocations
```

**Stage 5 - Rollback**:
```
Prepare rollback:
- Document current state
- Verify backup procedures
- Test rollback commands
- Plan for data persistence
```

## State Transitions

### Deployment States
```
Initial State: Codebase on disk
    ↓ [Containerize]
Ready State: Container images built and tagged
    ↓ [Helm Chart]
Packaged State: Helm charts created with configurations
    ↓ [Deploy]
Deploying State: Services being deployed to Minikube
    ↓ [Validate]
Active State: Services running and validated
    ↓ [Monitor]
Stable State: Services operating normally
    ↓ [Issues Detected]
Degraded State: Problems requiring attention
    ↓ [Rollback Decision]
Rollback State: Rolling back to previous stable version
    ↓ [Re-validate]
Previous Stable: Back to known working state
```

### Transition Validation Points
- **Ready → Packaged**: Verify images exist and are accessible
- **Packaged → Deploying**: Validate Helm chart syntax and values
- **Deploying → Active**: Confirm all pods are running
- **Active → Stable**: Validate all functionality tests pass
- **Stable → Degraded**: Monitor for failures and alerts
- **Degraded → Rollback**: Verify rollback procedures work
- **Rollback → Previous Stable**: Confirm successful restoration

## Common Validation Steps

### Pre-Deployment Validation
- [ ] Phase IV spec is fully understood and validated
- [ ] All services identified and dependencies mapped
- [ ] Resource requirements estimated
- [ ] Security requirements defined
- [ ] MCP integration points identified

### Post-Deployment Validation
- [ ] All pods running without restarts
- [ ] Services accessible and responsive
- [ ] Environment variables correctly set
- [ ] MCP tools registered and accessible
- [ ] Resource usage within expected bounds
- [ ] Health checks passing consistently

## Error Handling

### Common Issues and Solutions
- **ImagePullBackOff**: Verify container images were built successfully
- **CrashLoopBackOff**: Check resource limits and application configuration
- **Pending Pods**: Verify Minikube resources and node availability
- **Service Unreachable**: Confirm service configurations and network policies
- **MCP Tools Not Available**: Verify MCP server deployment and registration

## Integration with AI Tools

### Docker AI Gordon
- Use for Dockerfile generation and optimization
- Leverage for dependency analysis
- Apply for security scanning

### kubectl-ai
- Perform AI-assisted diagnostics
- Execute natural language commands
- Analyze deployment issues

### kagent
- Intelligent resource management
- Automated optimization suggestions
- Predictive scaling decisions

## Final Validation Checklist

Before marking deployment complete:
- [ ] All 5 stages completed successfully
- [ ] All safety rules validated
- [ ] All test checkpoints passed
- [ ] Rollback strategy tested and documented
- [ ] Monitoring and alerting configured
- [ ] Performance benchmarks met
- [ ] Security scans passed