#!/bin/bash
# generate-deployment-plan.sh
# Script to generate a comprehensive deployment plan from Phase IV spec

set -e

SPEC_FILE=${1:-"specs/004-k8s-deployment/spec.md"}
OUTPUT_DIR=${2:-"./deployment-plan"}

echo "🏗️  Generating Phase IV deployment plan..."
echo "📋 Source spec: $SPEC_FILE"
echo "📁 Output directory: $OUTPUT_DIR"

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Extract services from spec
echo "📦 Identifying services..."

SERVICES=()
FRONTEND_FOUND=false
BACKEND_FOUND=false
MCP_SERVER_FOUND=false

if grep -E -i "frontend|next.js|react|ui" "$SPEC_FILE" > /dev/null; then
    SERVICES+=("frontend")
    FRONTEND_FOUND=true
    echo "  - Frontend service detected"
fi

if grep -E -i "backend|fastapi|api|server" "$SPEC_FILE" > /dev/null; then
    SERVICES+=("backend")
    BACKEND_FOUND=true
    echo "  - Backend service detected"
fi

if grep -E -i "mcp|mcp server|model context protocol|openai agents" "$SPEC_FILE" > /dev/null; then
    SERVICES+=("mcp-server")
    MCP_SERVER_FOUND=true
    echo "  - MCP server detected"
fi

if [ ${#SERVICES[@]} -eq 0 ]; then
    echo "⚠️  No services detected in spec - please verify spec content"
    exit 1
fi

echo "  Identified ${#SERVICES[@]} services: ${SERVICES[*]}"

# Create plan structure
mkdir -p "$OUTPUT_DIR/stage-1-containerize"
mkdir -p "$OUTPUT_DIR/stage-2-helm-charts"
mkdir -p "$OUTPUT_DIR/stage-3-deploy"
mkdir -p "$OUTPUT_DIR/stage-4-validate"
mkdir -p "$OUTPUT_DIR/stage-5-rollback"

# Generate Stage 1: Containerize Plan
echo ""
echo "📦 Creating containerization plan..."

cat > "$OUTPUT_DIR/stage-1-containerize/README.md" << EOF
# Stage 1: Containerize Applications

## Services to Containerize

EOF

for service in "${SERVICES[@]}"; do
    cat >> "$OUTPUT_DIR/stage-1-containerize/README.md" << EOF
- **$service**:
  - Use Docker AI Gordon to analyze and generate Dockerfile
  - Build image with tag: \$(PROJECT_NAME)-$service:\$(VERSION)
  - Optimize for size and security

EOF
done

cat >> "$OUTPUT_DIR/stage-1-containerize/README.md" << EOF

## Commands to Execute

\`\`\`bash
# Analyze each service
EOF

for service in "${SERVICES[@]}"; do
    cat >> "$OUTPUT_DIR/stage-1-containerize/README.md" << EOF
docker-ai analyze-project --path ./services/$service
docker-ai generate-dockerfile --path ./services/$service
docker build -t \$(PROJECT_NAME)-$service:\$(VERSION) ./services/$service
EOF
done

cat >> "$OUTPUT_DIR/stage-1-containerize/README.md" << EOF
\`\`\`

## Validation Checklist

- [ ] Dockerfiles generated for all services
- [ ] Images build successfully
- [ ] Images are optimized (size < 500MB)
- [ ] Security scans pass
- [ ] Images pushed to local registry
EOF

# Generate Stage 2: Helm Charts Plan
echo "🚢 Creating Helm chart plan..."

cat > "$OUTPUT_DIR/stage-2-helm-charts/README.md" << EOF
# Stage 2: Generate Helm Charts

## Charts to Create

EOF

for service in "${SERVICES[@]}"; do
    cat >> "$OUTPUT_DIR/stage-2-helm-charts/README.md" << EOF
### $service

- Chart name: $service
- Parameters to include:
  - image.repository
  - image.tag
  - image.pullPolicy
  - service.type
  - service.port
  - resources.limits/cpu
  - resources.limits/memory
  - resources.requests/cpu
  - resources.requests/memory
  - env variables

EOF
done

cat >> "$OUTPUT_DIR/stage-2-helm-charts/README.md" << EOF

## Commands to Execute

\`\`\`bash
EOF

for service in "${SERVICES[@]}"; do
    cat >> "$OUTPUT_DIR/stage-2-helm-charts/README.md" << EOF
helm create $service-chart
# Customize templates for $service
EOF
done

cat >> "$OUTPUT_DIR/stage-2-helm-charts/README.md" << EOF
\`\`\`

## Validation Checklist

- [ ] Helm charts created for all services
- [ ] All parameters are configurable via values.yaml
- [ ] Resource requests/limits are appropriate
- [ ] Security contexts are properly configured
- [ ] Dependencies between charts defined
EOF

# Generate Stage 3: Deploy Plan
echo "🚀 Creating deployment plan..."

cat > "$OUTPUT_DIR/stage-3-deploy/README.md" << EOF
# Stage 3: Deploy to Minikube

## Deployment Order

1. MCP Server (if exists)
2. Backend services
3. Frontend services

## Commands to Execute

\`\`\`bash
# Start Minikube cluster
minikube start --cpus=4 --memory=8192

# Install charts in order
EOF

if [ "$MCP_SERVER_FOUND" = true ]; then
    cat >> "$OUTPUT_DIR/stage-3-deploy/README.md" << EOF
helm install mcp-server ./mcp-server-chart --wait
EOF
fi

if [ "$BACKEND_FOUND" = true ]; then
    cat >> "$OUTPUT_DIR/stage-3-deploy/README.md" << EOF
helm install backend ./backend-chart --wait
EOF
fi

if [ "$FRONTEND_FOUND" = true ]; then
    cat >> "$OUTPUT_DIR/stage-3-deploy/README.md" << EOF
helm install frontend ./frontend-chart --wait
EOF
fi

cat >> "$OUTPUT_DIR/stage-3-deploy/README.md" << EOF

# Verify deployments
kubectl get pods,services,ingress
\`\`\`

## Validation Checklist

- [ ] Minikube cluster started successfully
- [ ] All charts installed without errors
- [ ] All pods are running (not pending/crashing)
- [ ] Services are accessible within cluster
- [ ] Inter-service communication works
EOF

# Generate Stage 4: Validation Plan
echo "✅ Creating validation plan..."

cat > "$OUTPUT_DIR/stage-4-validate/README.md" << EOF
# Stage 4: Validate Health and Functionality

## Test Checkpoints

### A. Service Reachability
EOF

for service in "${SERVICES[@]}"; do
    cat >> "$OUTPUT_DIR/stage-4-validate/README.md" << EOF
- **$service**:
  - Check: Service is accessible via ClusterIP
  - Method: kubectl get svc $service-service
  - Success: Service responds with expected HTTP codes

EOF
done

cat >> "$OUTPUT_DIR/stage-4-validate/README.md" << EOF

### B. Environment Variable Propagation
EOF

for service in "${SERVICES[@]}"; do
    cat >> "$OUTPUT_DIR/stage-4-validate/README.md" << EOF
- **$service**:
  - Check: Environment variables are correctly set
  - Method: kubectl exec -it <pod> -- env | grep <var>
  - Success: All required environment variables are present

EOF
done

cat >> "$OUTPUT_DIR/stage-4-validate/README.md" << EOF

### C. MCP Tool Integration (if MCP server exists)
EOF

if [ "$MCP_SERVER_FOUND" = true ]; then
    cat >> "$OUTPUT_DIR/stage-4-validate/README.md" << EOF
- Check: MCP server tools are accessible
- Method: Test MCP tool registration and invocation
- Success: Chatbot can discover and use MCP tools

EOF
fi

cat >> "$OUTPUT_DIR/stage-4-validate/README.md" << EOF

## Commands to Execute

\`\`\`bash
# Check service reachability
kubectl get svc

# Test environment variables
kubectl get pods
EOF

for service in "${SERVICES[@]}"; do
    cat >> "$OUTPUT_DIR/stage-4-validate/README.md" << EOF
kubectl exec -it \$(kubectl get pods -l app=$service -o jsonpath='{.items[0].metadata.name}') -- env
EOF
done

if [ "$MCP_SERVER_FOUND" = true ]; then
    cat >> "$OUTPUT_DIR/stage-4-validate/README.md" << EOF

# Test MCP integration
# (Specific tests will depend on your MCP tools)
kubectl logs -l app=mcp-server
EOF
fi

cat >> "$OUTPUT_DIR/stage-4-validate/README.md" << EOF

# Run health checks
kubectl get pods -o wide
kubectl-ai diagnose deployment status
\`\`\`

## Validation Checklist

- [ ] All services respond to requests
- [ ] Environment variables are correctly set
- [ ] MCP tools are accessible (if applicable)
- [ ] Health checks pass consistently
- [ ] Performance meets requirements
EOF

# Generate Stage 5: Rollback Plan
echo "🔙 Creating rollback plan..."

cat > "$OUTPUT_DIR/stage-5-rollback/README.md" << EOF
# Stage 5: Rollback Strategy

## Rollback Plan

### Immediate Rollback Actions
EOF

for service in "${SERVICES[@]}"; do
    cat >> "$OUTPUT_DIR/stage-5-rollback/README.md" << EOF
- **$service**:
  - Command: helm rollback $service \$(PREVIOUS_VERSION)
  - Impact: Service downtime until rollback complete
  - Verification: Check service status and functionality

EOF
done

cat >> "$OUTPUT_DIR/stage-5-rollback/README.md" << EOF

### Data Preservation Strategy
- Persistent volumes: Data preserved during rollback
- ConfigMaps/Secrets: Usually preserved
- Custom resources: May need manual cleanup

### Commands to Execute

\`\`\`bash
# Check deployment history
EOF

for service in "${SERVICES[@]}"; do
    cat >> "$OUTPUT_DIR/stage-5-rollback/README.md" << EOF
helm history $service
EOF
done

cat >> "$OUTPUT_DIR/stage-5-rollback/README.md" << EOF

# Perform rollback (example)
helm rollback backend 1  # Rollback to revision 1
helm rollback frontend 1
\`\`\`

## Validation Checklist

- [ ] Rollback commands tested successfully
- [ ] Data preservation verified
- [ ] Service functionality restored after rollback
- [ ] No dependency issues after rollback
- [ ] Monitoring confirms stable state
EOF

# Create master plan overview
echo "📋 Creating master deployment plan..."

cat > "$OUTPUT_DIR/DEPLOYMENT_PLAN.md" << EOF
# Phase IV Deployment Plan

## Executive Summary

This plan outlines the 5-stage deployment process for the services identified in the Phase IV specification:

- Services to deploy: ${SERVICES[*]}
- Target platform: Minikube (local Kubernetes)
- Tools: Docker AI, Helm, kubectl-ai
- Timeline: Approximately 2-4 hours depending on complexity

## Safety Rules

1. **No Cloud Provider Calls**: All deployments local to Minikube
2. **No Manual Code Changes**: Only AI-assisted tools (Docker AI, kubectl-ai, kagent)
3. **Respect Deployment Invariants**: Follow spec-defined constraints
4. **Local-Only Environment**: No external dependencies

## Stage Overview

| Stage | Description | Estimated Time | Success Criteria |
|-------|-------------|----------------|------------------|
| 1. Containerize | Package applications into container images | 30-60 min | All services containerized successfully |
| 2. Helm Charts | Create parameterized Helm charts | 45-90 min | All charts created and validated |
| 3. Deploy | Deploy to Minikube cluster | 30-60 min | All services running in cluster |
| 4. Validate | Verify functionality and health | 30-60 min | All tests pass successfully |
| 5. Rollback | Prepare and document rollback strategy | 15-30 min | Rollback procedures tested |

## Prerequisites

- Minikube installed and running
- Docker daemon running
- kubectl and Helm installed
- Docker AI Gordon (recommended)
- kubectl-ai (recommended)

## Risk Mitigation

- Backup configurations before deployment
- Test rollback procedures beforehand
- Monitor resource usage during deployment
- Validate inter-service dependencies

## Success Criteria

- All services deployed and running
- All validation tests pass
- MCP integration functional (if applicable)
- Rollback strategy documented and tested
- Performance benchmarks met
EOF

echo ""
echo "✅ Deployment plan generated successfully!"
echo "📁 Plan location: $OUTPUT_DIR/"
echo ""
echo "📋 Plan structure:"
tree "$OUTPUT_DIR" 2>/dev/null || find "$OUTPUT_DIR" -type f | sort

echo ""
echo "🚀 To execute the plan:"
echo "1. Review each stage in the generated documentation"
echo "2. Ensure all prerequisites are met"
echo "3. Execute each stage in sequence"
echo "4. Validate success criteria before proceeding to next stage"