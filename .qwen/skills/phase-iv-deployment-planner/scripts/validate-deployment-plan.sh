#!/bin/bash
# validate-deployment-plan.sh
# Script to validate a Phase IV deployment plan before execution

set -e

SPEC_FILE=${1:-"specs/004-k8s-deployment/spec.md"}

echo "🔍 Validating Phase IV deployment plan..."
echo "📋 Using spec file: $SPEC_FILE"

# Check if required tools are available
MISSING_TOOLS=()
REQUIRED_TOOLS=("minikube" "kubectl" "helm")

if command -v docker-ai &> /dev/null; then
    REQUIRED_TOOLS+=("docker-ai")
else
    echo "⚠️  docker-ai not found - will use standard docker commands"
fi

if command -v kubectl-ai &> /dev/null; then
    REQUIRED_TOOLS+=("kubectl-ai")
else
    echo "⚠️  kubectl-ai not found - will use standard kubectl commands"
fi

for tool in "${REQUIRED_TOOLS[@]}"; do
    if ! command -v "$tool" &> /dev/null; then
        MISSING_TOOLS+=("$tool")
    fi
done

if [ ${#MISSING_TOOLS[@]} -gt 0 ]; then
    echo "❌ Missing required tools: ${MISSING_TOOLS[*]}"
    echo "Please install the missing tools before proceeding"
    exit 1
fi

echo "✅ All required tools are available"

# Validate spec file exists
if [ ! -f "$SPEC_FILE" ]; then
    echo "❌ Spec file not found: $SPEC_FILE"
    exit 1
fi

echo "✅ Spec file found: $SPEC_FILE"

# Check for safety rules compliance
echo ""
echo "🛡️  Checking safety rules compliance..."

# Check for cloud provider calls
if grep -E -i "aws|gcp|azure|cloud|provider" "$SPEC_FILE" | grep -v "local\|minikube\|on-premise" > /dev/null; then
    echo "⚠️  Potential cloud provider references found in spec - verify local-only deployment"
else
    echo "✅ No cloud provider references detected"
fi

# Check for manual code changes
if grep -E -i "manual|hand-written|written by hand|custom code" "$SPEC_FILE" | grep -v "configuration\|manifest\|yaml" > /dev/null; then
    echo "⚠️  Potential manual code change references found - verify AI-assisted approach"
else
    echo "✅ No manual code change references detected"
fi

# Identify services to be deployed
echo ""
echo "📦 Identifying services to be deployed..."

SERVICES=()
if grep -E -i "frontend|next.js|react|ui" "$SPEC_FILE" > /dev/null; then
    SERVICES+=("frontend")
    echo "  - Frontend service identified"
fi

if grep -E -i "backend|fastapi|api|server" "$SPEC_FILE" > /dev/null; then
    SERVICES+=("backend")
    echo "  - Backend service identified"
fi

if grep -E -i "mcp|mcp server|model context protocol" "$SPEC_FILE" > /dev/null; then
    SERVICES+=("mcp-server")
    echo "  - MCP server identified"
fi

if [ ${#SERVICES[@]} -eq 0 ]; then
    echo "⚠️  No services identified in spec - please verify spec content"
else
    echo "  Found ${#SERVICES[@]} services to deploy: ${SERVICES[*]}"
fi

# Check for MCP integration requirements
echo ""
echo "🤖 Checking MCP integration requirements..."

if grep -E -i "mcp|tool|openai agents|model context protocol" "$SPEC_FILE" > /dev/null; then
    echo "  ✅ MCP integration required - validating tool access"
    echo "  - Verify MCP server deployment"
    echo "  - Confirm tool registration"
    echo "  - Test chatbot integration"
else
    echo "  ℹ️  MCP integration not explicitly required"
fi

# Validate resource requirements
echo ""
echo "💾 Checking resource requirements..."

MEMORY_REQ=$(grep -E -i "memory|resource" "$SPEC_FILE" | grep -oE "[0-9]+[MG]" | head -1)
CPU_REQ=$(grep -E -i "cpu|cores" "$SPEC_FILE" | grep -oE "[0-9]+(m|core|cores)" | head -1)

if [ -n "$MEMORY_REQ" ]; then
    echo "  - Memory requirement detected: $MEMORY_REQ"
else
    echo "  - No specific memory requirements found"
fi

if [ -n "$CPU_REQ" ]; then
    echo "  - CPU requirement detected: $CPU_REQ"
else
    echo "  - No specific CPU requirements found"
fi

# Check Minikube requirements
echo ""
echo "☸️  Validating Minikube setup..."

MINIKUBE_STATUS=$(minikube status 2>/dev/null || echo "inactive")
if [[ "$MINIKUBE_STATUS" == *"Running"* ]]; then
    echo "✅ Minikube is running"
else
    echo "⚠️  Minikube is not running - will need to start cluster"
fi

MINIKUBE_CPUS=$(minikube ssh 'nproc' 2>/dev/null || echo "unknown")
MINIKUBE_MEMORY=$(minikube ssh 'free -m | grep Mem | awk "{print \$7}"' 2>/dev/null || echo "unknown")

echo "  - Available CPUs: $MINIKUBE_CPUS"
echo "  - Available memory: $MINIKUBE_MEMORY MB"

# Validate Helm chart requirements
echo ""
echo "🚢 Checking Helm chart requirements..."

HELM_VERSION=$(helm version --short 2>/dev/null || echo "not available")
echo "  - Helm version: $HELM_VERSION"

# Check for existing chart templates
if [ -d "helm-templates" ] || [ -d "charts" ]; then
    echo "  ✅ Helm chart templates found"
else
    echo "  ℹ️  No existing Helm chart templates found - will need to create"
fi

# Check for deployment invariants
echo ""
echo "🔒 Validating deployment invariants..."

# Check for local-only constraint
if grep -E -i "local|minikube|localhost|127.0.0.1" "$SPEC_FILE" > /dev/null; then
    echo "  ✅ Local-only deployment constraint confirmed"
else
    echo "  ⚠️  Local-only constraint not explicitly stated - verify spec"
fi

# Check for cloud-agnostic requirements
if grep -E -i "cloud-agnostic|platform-agnostic|vendor-neutral" "$SPEC_FILE" > /dev/null; then
    echo "  ✅ Cloud-agnostic requirement found"
fi

# Summary
echo ""
echo "📋 Deployment Plan Validation Summary:"
echo "  - Spec file: $SPEC_FILE"
echo "  - Services to deploy: ${#SERVICES[@]} (${SERVICES[*]})"
echo "  - Safety rules: Checked"
echo "  - Required tools: Available"
echo "  - MCP integration: $(if grep -E -i "mcp|tool|openai agents" "$SPEC_FILE" > /dev/null; then echo "Required"; else echo "Not required"; fi)"
echo "  - Minikube status: $([ minikube status 2>/dev/null | grep -q "Running" ] && echo "Running" || echo "Not running")"
echo ""
echo "✅ Phase IV deployment plan validation completed successfully!"

echo ""
echo "🚀 Next steps:"
echo "  1. Start Minikube cluster if not running: minikube start"
echo "  2. Containerize applications using Docker AI"
echo "  3. Generate Helm charts for identified services"
echo "  4. Deploy to Minikube following the 5-stage process"
echo "  5. Validate functionality and MCP integration"
echo "  6. Prepare rollback strategy"

exit 0