# Implementation Plan: Phase IV Kubernetes Deployment

**Branch**: `004-k8s-deployment` | **Date**: 2026-01-26 | **Spec**: [link to spec.md]
**Input**: Feature specification from `/specs/004-k8s-deployment/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Deploy the existing AI-powered Todo Chatbot application to a local Kubernetes cluster using Minikube, Helm Charts, and AI-assisted DevOps agents. This involves containerizing the frontend (Next.js), backend (FastAPI), and MCP server components using AI-assisted tools, creating parameterized Helm charts for each service, and deploying them to a local Minikube cluster following constitutional requirements for cloud-native deployment with AI-assisted operations. The plan follows a systematic 5-stage process: containerize, chart, deploy, validate, rollback.

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: Python 3.13+ (backend), TypeScript (frontend) + FastAPI, Next.js
**Primary Dependencies**: FastAPI, SQLModel, Neon PostgreSQL, OpenAI Agents SDK, Official MCP SDK, Better Auth, Kubernetes, Helm, Minikube, Docker AI Gordon, kubectl-ai, kagent
**Storage**: Neon Serverless PostgreSQL (managed via SQLModel ORM) with Kubernetes PersistentVolumes for local deployment
**Testing**: pytest (backend), Jest/React Testing Library (frontend), Helm tests (infrastructure), kubectl-ai validation tests
**Target Platform**: Local Kubernetes cluster (Minikube)
**Project Type**: Web (frontend + backend + MCP server)
**Performance Goals**: Sub-2 second response time in local environment, 99% uptime in local Minikube, under 10-minute deployment time
**Constraints**: Must run entirely on local Minikube (no cloud dependencies), use AI-assisted DevOps tools, follow constitutional requirements, respect resource limits (2 CPUs, 4GB RAM default Minikube)
**Scale/Scope**: Single-user local development environment with ability to scale to multi-user in future

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- ✅ **Section I (SDD)**: Following proper SDD workflow (spec -> plan -> tasks -> implement)
- ✅ **Section VI (Multi-User Security)**: Will implement JWT authentication with Kubernetes Secrets for BETTER_AUTH_SECRET
- ✅ **Section VII (Authentication)**: Will maintain Better Auth for frontend and JWT verification in backend
- ✅ **Section IX (Persistence)**: Will use Neon PostgreSQL with Kubernetes PersistentVolumes
- ✅ **Section XVIII (Kubernetes Deployment)**: Deploying using Helm Charts to Minikube only
- ✅ **Section XIX (AI-Assisted DevOps)**: Using Docker AI Gordon, kubectl-ai, and kagent as required
- ✅ **Section XXI (Infrastructure as Code)**: Using Helm Charts with version-controlled templates
- ✅ **Section XXII (Local-Only Deployment)**: Targeting Minikube exclusively per requirements

## Stage 1 — Environment Preparation

### Validate Minikube Setup
**Skill to Use**: `devops-scenario-evaluator` - Section: Initial Assessment
- Execute: `minikube version` to verify installation
- Execute: `minikube status` to confirm cluster readiness
- Verify: Minikube cluster is running and accessible
- Use context7: Fetch latest Minikube best practices and resource allocation recommendations

### Validate Docker Desktop with Docker AI Agent Enabled
**Skill to Use**: `devops-scenario-evaluator` - Section: Initial Assessment
- Execute: `docker --version` to verify Docker installation
- Execute: `docker info` to confirm AI Agent features are enabled
- Verify: Docker daemon is running and connected to Minikube context
- Use context7: Fetch latest Docker AI Gordon capabilities and usage patterns

### Validate Kubernetes Tools
**Skill to Use**: `devops-scenario-evaluator` - Section: Initial Assessment
- Execute: `kubectl version --client` to verify kubectl installation
- Execute: `helm version` to verify Helm installation
- Execute: `kubectl-ai --help` to verify kubectl-ai plugin
- Execute: `kagent --help` to verify kagent installation
- Use context7: Fetch latest kubectl-ai and kagent documentation

### Precondition Checks
**Skill to Use**: `devops-scenario-evaluator` - Section: Initial Assessment
- Verify: Minimum 4GB free RAM allocated to Minikube (recommended 8GB)
- Verify: At least 20GB free disk space
- Verify: No conflicting Docker containers running
- Verify: Network connectivity for pulling images
- Use context7: Fetch Minikube resource requirement best practices

## Stage 2 — Containerization

### Containerize Frontend Application
**Skill to Use**: `k8s-deployment-orchestrator` - Section: Step 1: Analyze Service Architecture
**Sub-skill**: `phase-iv-deployment-planner` - Section: Stage 1: Containerize Apps
- Use Docker AI Gordon to analyze Next.js project: `docker-ai analyze-project ./frontend`
- Generate optimized Dockerfile: `docker-ai generate-dockerfile ./frontend`
- Build container image with appropriate base image: `docker build -t todo-frontend:latest -f ./frontend/Dockerfile .`
- Optimize image for size and security following Next.js specific configurations
- Expected artifact: `todo-frontend:latest` image
- Use context7: Fetch latest Docker best practices for Next.js applications

### Containerize Backend Application
**Skill to Use**: `k8s-deployment-orchestrator` - Section: Step 1: Analyze Service Architecture
**Sub-skill**: `phase-iv-deployment-planner` - Section: Stage 1: Containerize Apps
- Use Docker AI Gordon to analyze FastAPI project: `docker-ai analyze-project ./backend`
- Generate optimized Dockerfile: `docker-ai generate-dockerfile ./backend`
- Build container image using official Python 3.13+ base image: `docker build -t todo-backend:latest -f ./backend/Dockerfile .`
- Optimize image for size and security following FastAPI specific configurations
- Expected artifact: `todo-backend:latest` image
- Use context7: Fetch latest Docker best practices for Python/FastAPI applications

### Containerize MCP Server
**Skill to Use**: `k8s-deployment-orchestrator` - Section: Step 1: Analyze Service Architecture
**Sub-skill**: `phase-iv-deployment-planner` - Section: Stage 1: Containerize Apps
- Use Docker AI Gordon to analyze MCP server project: `docker-ai analyze-project ./mcp-server`
- Generate Dockerfile for MCP server (Python or Node.js based on implementation)
- Install MCP SDK dependencies
- Configure appropriate startup command
- Expected artifact: `mcp-server:latest` image
- Use context7: Fetch latest Docker best practices for MCP server applications

### Image Validation
**Skill to Use**: `devops-scenario-evaluator` - Section: Validation Steps After Remediation
- Confirm: All images are appropriately sized (under 500MB for simple apps)
- Confirm: All dependencies are properly included
- Confirm: Dockerfiles follow security best practices
- Use kubectl-ai to verify image integrity: `kubectl-ai verify image integrity`

## Stage 3 — Helm Chart Generation

### Generate Frontend Helm Chart
**Skill to Use**: `k8s-deployment-orchestrator` - Section: Step 4: Create Helm Chart Structure
**Sub-skill**: `phase-iv-deployment-planner` - Section: Stage 2: Generate Helm Charts
- Create Helm chart structure: `helm create todo-frontend`
- Define Deployment with Next.js specific resource requests/limits:
  ```yaml
  resources:
    limits:
      cpu: 200m
      memory: 256Mi
    requests:
      cpu: 50m
      memory: 64Mi
  ```
- Define Service with ClusterIP type
- Define Ingress with appropriate host/path routing
- Add health checks specific to Next.js application
- Use context7: Fetch latest Kubernetes API schemas for Deployment and Service objects

### Generate Backend Helm Chart
**Skill to Use**: `k8s-deployment-orchestrator` - Section: Step 4: Create Helm Chart Structure
**Sub-skill**: `phase-iv-deployment-planner` - Section: Stage 2: Generate Helm Charts
- Create Helm chart structure: `helm create todo-backend`
- Define Deployment with environment variable mappings and FastAPI specific configurations:
  ```yaml
  resources:
    limits:
      cpu: 500m
      memory: 512Mi
    requests:
      cpu: 100m
      memory: 128Mi
  ```
- Define Service with ClusterIP type
- Configure liveness/readiness probes for FastAPI health endpoints
- Add security contexts as per constitutional requirements
- Use context7: Fetch latest Kubernetes API schemas for health probe configurations

### Generate MCP Server Helm Chart
**Skill to Use**: `k8s-deployment-orchestrator` - Section: Step 4: Create Helm Chart Structure
**Sub-skill**: `phase-iv-deployment-planner` - Section: Stage 2: Generate Helm Charts
- Create Helm chart structure: `helm create mcp-server`
- Define Deployment with MCP-specific configurations:
  ```yaml
  resources:
    limits:
      cpu: 300m
      memory: 256Mi
    requests:
      cpu: 50m
      memory: 64Mi
  ```
- Define Service with ClusterIP type
- Configure security contexts as per Constitution
- Add MCP-specific environment variables
- Use context7: Fetch latest Kubernetes security context best practices

### Values Override Configuration
**Skill to Use**: `k8s-deployment-orchestrator` - Section: Step 5: Define Values.yaml with Best Practices
**Sub-skill**: `phase-iv-deployment-planner` - Section: Stage 2: Generate Helm Charts
- Map environment variables from Constitution:
  - Database connection strings
  - JWT secret keys
  - API endpoints
  - External service URLs
- Configure replica counts per service (1 for Minikube environment)
- Set resource limits based on expected load and Minikube constraints
- Implement proper resource requests/limits based on actual usage
- Use context7: Fetch latest Helm best practices for values management

## Stage 4 — Kubernetes Deployment

### Apply Helm Charts to Minikube
**Skill to Use**: `phase-iv-deployment-planner` - Section: Stage 3: Deploy to Minikube
**Sub-skill**: `k8s-deployment-orchestrator` - Section: When to Use This Skill
- Execute: `minikube start --cpus=4 --memory=8192 --disk-size=20g` to start cluster with sufficient resources
- Load images into Minikube: `minikube image load todo-frontend:latest`, etc.
- Execute: `helm install mcp-server ./charts/mcp-server/` (first due to dependency)
- Execute: `helm install todo-backend ./charts/todo-backend/` (second due to dependency)
- Execute: `helm install todo-frontend ./charts/todo-frontend/` (last)
- Monitor deployment progress using `kubectl-ai diagnose deployment status`
- Use context7: Fetch latest Kubernetes API details for deployment operations

### Configure Service Dependencies
**Skill to Use**: `phase-iv-deployment-planner` - Section: Stage 3: Deploy to Minikube
**Sub-skill**: `k8s-deployment-orchestrator` - Section: Service-Specific Configurations
- Configure backend to connect to MCP server via internal DNS
- Configure frontend to connect to backend via internal DNS
- Set up proper service account and RBAC if required
- Verify service-to-service communication
- Use context7: Fetch latest Kubernetes service discovery patterns

### Configure Health Probes and Resource Limits
**Skill to Use**: `k8s-deployment-orchestrator` - Section: Best Practices - Health Checks
**Sub-skill**: `phase-iv-deployment-planner` - Section: Stage 3: Deploy to Minikube
- Configure liveness probes with 30s initial delay, 10s interval
- Configure readiness probes with 5s initial delay, 5s interval
- Set CPU requests/limits: 100m/500m for frontend, 200m/1000m for backend, 50m/300m for MCP
- Set memory requests/limits: 256Mi/512Mi for frontend, 512Mi/1Gi for backend, 64Mi/256Mi for MCP
- Use context7: Fetch latest Kubernetes resource management best practices

## Stage 5 — Operational Verification

### Pod Health Checks
**Skill to Use**: `devops-scenario-evaluator` - Section: 1. CrashLoopBackOff Diagnosis
- Verify: All pods are Running status with no restarts
- Use: `kubectl-ai show cluster status` and `kubectl-ai show pods with issues`
- Verify: No CrashLoopBackOff, ImagePullBackOff, or Pending states
- Check: Resource utilization within expected ranges
- Check: Logs for any error messages
- Use context7: Fetch latest kubectl-ai diagnostic commands

### Connectivity Tests
**Skill to Use**: `devops-scenario-evaluator` - Section: Step-by-Step Diagnostic Process
**Sub-skill**: `phase-iv-deployment-planner` - Section: Stage 4: Validate Health and Functionality
- Test: Frontend can reach backend via internal service
- Test: Backend can reach MCP server via internal service
- Test: Database connections are established
- Use kubectl exec to perform connectivity tests from within pods
- Use: `kubectl-ai validate service connectivity`
- Use context7: Fetch latest Kubernetes connectivity testing patterns

### JWT Authentication Validation
**Skill to Use**: `devops-scenario-evaluator` - Section: Expected Resolution Steps by Issue Type
**Sub-skill**: `phase-iv-deployment-planner` - Section: Stage 4: Validate Health and Functionality
- Test: JWT token generation and validation flow
- Test: Protected endpoints require valid tokens
- Test: Token expiration is properly handled
- Validate: No hardcoded credentials in configuration
- Use: `kubectl-ai show environment for pod <pod-name>` to verify JWT_SECRET
- Use context7: Fetch latest JWT validation best practices in Kubernetes

### Chatbot Tool Invocation Tests
**Skill to Use**: `devops-scenario-evaluator` - Section: Expected Resolution Steps by Issue Type
**Sub-skill**: `phase-iv-deployment-planner` - Section: Stage 4: Validate Health and Functionality
- Test: Chatbot can successfully invoke MCP tools
- Test: Tool responses are properly formatted
- Test: Error handling for failed tool calls
- Validate: End-to-end chat functionality
- Use: `kubectl-ai verify mcp tool access`
- Use context7: Fetch latest MCP tool invocation patterns

## Stage 6 — Post-Deployment Validation

### Acceptance Criteria Verification
**Skill to Use**: `phase-iv-deployment-planner` - Section: Post-Deployment Validation
- Confirm: All Phase IV Constitution invariants are maintained
- Confirm: Application responds to HTTP requests
- Confirm: Data persistence works correctly
- Confirm: Authentication flow operates as expected
- Use: `kubectl-ai test environment propagation`
- Use context7: Fetch latest acceptance testing methodologies for Kubernetes

### Endpoint Testing
**Skill to Use**: `devops-scenario-evaluator` - Section: Guidance for Log Inspection
**Sub-skill**: `phase-iv-deployment-planner` - Section: Post-Deployment Validation
- Test: Frontend health endpoint
- Test: Backend API endpoints
- Test: MCP server registration endpoints
- Test: Authentication endpoints
- Use curl or kubectl port-forward to access endpoints
- Use: `kubectl-ai show logs for pods with issues` if problems arise
- Use context7: Fetch latest endpoint testing tools for Kubernetes

### Security and Configuration Validation
**Skill to Use**: `k8s-deployment-orchestrator` - Section: Best Practices - Security
**Sub-skill**: `devops-scenario-evaluator` - Section: Expected Resolution Steps by Issue Type
- Verify: No privileged containers running
- Verify: Proper resource quotas enforced
- Verify: Network policies applied if configured
- Verify: Secrets are properly managed and not exposed
- Use: `kubectl-ai check image pull secrets` for secret validation
- Use context7: Fetch latest Kubernetes security validation tools

## Stage 7 — Rollback and Recovery

### Rollback Triggers
**Skill to Use**: `phase-iv-deployment-planner` - Section: Stage 5: Rollback Strategy
**Sub-skill**: `devops-scenario-evaluator` - Section: Expected Resolution Steps by Issue Type
- Application fails to reach healthy state after 10 minutes
- Critical security vulnerabilities detected
- Data corruption issues identified
- Performance below acceptable thresholds
- Persistent CrashLoopBackOff or ImagePullBackOff errors
- Use context7: Fetch latest rollback best practices for Helm deployments

### Rollback Procedure
**Skill to Use**: `phase-iv-deployment-planner` - Section: Stage 5: Rollback Strategy
- Execute: `helm rollback <release-name> <revision>` for failed deployments
- Use: `kubectl-ai analyze rollback impact` for impact analysis
- Verify: All resources removed from cluster during full uninstall
- Check: `helm history <release-name>` for deployment history
- Document reasons for rollback in deployment logs
- Use context7: Fetch latest Helm rollback procedures

### Recovery Using AI Skills
**Skill to Use**: Combination of `devops-scenario-evaluator`, `k8s-deployment-orchestrator`, and `phase-iv-deployment-planner`
- Analyze failure logs using `devops-scenario-evaluator` diagnostic tools
- Use kubectl-ai to identify root causes: `kubectl-ai diagnose failing pods`
- Generate remediation suggestions using kagent: `kagent analyze pod-resource conflicts`
- Re-attempt deployment with fixes
- Use context7: Fetch latest Kubernetes troubleshooting best practices

### Constitution Invariant Checks
**Skill to Use**: `devops-scenario-evaluator` - Section: Validation Steps After Remediation
**Sub-skill**: `phase-iv-deployment-planner` - Section: Final Validation Checklist
- Before any deployment: Verify Constitution invariants
- During rollback: Ensure no violation of core principles
- After recovery: Re-validate all constitutional requirements
- Use: `kubectl-ai validate service connectivity` for connectivity validation
- Use context7: Fetch latest constitutional compliance validation tools

## Project Structure

### Documentation (this feature)

```text
specs/004-k8s-deployment/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
│   └── api-contracts.yaml
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/
│   ├── services/
│   └── api/
└── tests/

frontend/
├── src/
│   ├── components/
│   ├── pages/
│   └── services/
└── tests/

mcp-server/
├── src/
│   └── tools/
└── tests/

helm/
├── todo-frontend/
│   ├── Chart.yaml
│   ├── values.yaml
│   └── templates/
│       ├── deployment.yaml
│       ├── service.yaml
│       ├── ingress.yaml
│       ├── configmap.yaml
│       └── secret.yaml
├── todo-backend/
│   ├── Chart.yaml
│   ├── values.yaml
│   └── templates/
│       ├── deployment.yaml
│       ├── service.yaml
│       ├── configmap.yaml
│       └── secret.yaml
└── mcp-server/
    ├── Chart.yaml
    ├── values.yaml
    └── templates/
        ├── deployment.yaml
        ├── service.yaml
        ├── configmap.yaml
        └── secret.yaml
```

**Structure Decision**: Web application with three main services (frontend, backend, MCP server) following the constitutional requirements for separation of concerns. Infrastructure as code is managed through Helm charts in the helm/ directory with proper resource management, health checks, and configuration management as specified in the k8s-deployment-orchestrator skill.

## Complexity Tracking

No constitutional violations identified. All implementation approaches comply with the Cloud-Native Todo Chatbot Constitution requirements. The plan incorporates AI-assisted DevOps tools as mandated by Section XIX and targets Minikube exclusively as required by Section XXII.
