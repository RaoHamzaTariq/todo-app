#!/bin/bash
# diagnose-cluster-health.sh
# Script to perform comprehensive Kubernetes cluster health diagnostics

set -e

echo "🔍 Starting Kubernetes cluster health diagnostics..."

# Check if kubectl is available
if ! command -v kubectl &> /dev/null; then
    echo "❌ Error: kubectl is not installed or not in PATH"
    exit 1
fi

# Optional: Check if kubectl-ai is available
KUBECTL_AI_AVAILABLE=false
if command -v kubectl-ai &> /dev/null; then
    KUBECTL_AI_AVAILABLE=true
    echo "✅ kubectl-ai is available"
else
    echo "⚠️  kubectl-ai is not available - will use standard kubectl commands"
fi

# Get current context
echo "📋 Current context: $(kubectl config current-context 2>/dev/null || echo 'No context set')"
echo "📋 Current namespace: $(kubectl config view --minify -o jsonpath='{..namespace}' 2>/dev/null || echo 'default')"

echo ""
echo "=== CLUSTER STATUS ==="

if [ "$KUBECTL_AI_AVAILABLE" = true ]; then
    echo "📊 Cluster status:"
    kubectl-ai show cluster status 2>/dev/null || kubectl cluster-info
else
    kubectl cluster-info
fi

echo ""
echo "=== NODE HEALTH ==="

if [ "$KUBECTL_AI_AVAILABLE" = true ]; then
    echo "🖥️  Node status:"
    kubectl-ai show node status 2>/dev/null || kubectl get nodes -o wide
else
    kubectl get nodes -o wide
fi

echo ""
echo "=== RESOURCE USAGE ==="

if [ "$KUBECTL_AI_AVAILABLE" = true ]; then
    echo "📈 Resource usage:"
    kubectl-ai show resource usage 2>/dev/null || {
        echo "Nodes resource usage:"
        kubectl top nodes 2>/dev/null || echo "Node metrics not available"
        echo ""
        echo "Pods resource usage:"
        kubectl top pods --all-namespaces 2>/dev/null || echo "Pod metrics not available"
    }
else
    echo "Nodes resource usage:"
    kubectl top nodes 2>/dev/null || echo "Node metrics not available"
    echo ""
    echo "Pods resource usage:"
    kubectl top pods --all-namespaces 2>/dev/null || echo "Pod metrics not available"
fi

echo ""
echo "=== PROBLEMATIC PODS ==="

# Find pods in problematic states
echo "🔍 Looking for pods in problematic states..."

PROBLEM_STATES="CrashLoopBackOff|ImagePullBackOff|Pending|Unknown|Failed|Evicted|Error"

if [ "$KUBECTL_AI_AVAILABLE" = true ]; then
    echo "🚨 Problematic pods:"
    kubectl-ai find pods with issues 2>/dev/null || {
        kubectl get pods --all-namespaces -o wide | grep -E "$PROBLEM_STATES" || echo "No problematic pods found"
    }
else
    kubectl get pods --all-namespaces -o wide | grep -E "$PROBLEM_STATES" || echo "No problematic pods found"
fi

echo ""
echo "=== DETAILED ANALYSIS ==="

# For each problematic pod found, perform deeper analysis
if [ "$KUBECTL_AI_AVAILABLE" = true ]; then
    echo "🔍 Analyzing failing pods..."
    kubectl-ai diagnose failing pods 2>/dev/null || echo "No failing pods to analyze"

    echo ""
    echo "🔍 Analyzing resource pressure..."
    kubectl-ai analyze resource pressure 2>/dev/null || echo "Resource pressure analysis not available"

    echo ""
    echo "🔍 Checking common issues..."
    kubectl-ai show common issues 2>/dev/null || echo "Common issues check not available"
else
    # Standard kubectl analysis
    echo "🔍 Checking for pods in CrashLoopBackOff..."
    kubectl get pods --all-namespaces -o yaml | grep -A 10 -B 10 "CrashLoopBackOff" || echo "No CrashLoopBackOff pods found"

    echo ""
    echo "🔍 Checking for pods in ImagePullBackOff..."
    kubectl get pods --all-namespaces -o yaml | grep -A 10 -B 10 "ImagePullBackOff" || echo "No ImagePullBackOff pods found"

    echo ""
    echo "🔍 Checking for pods in Pending state..."
    kubectl get pods --all-namespaces -o yaml | grep -A 10 -B 10 "Pending" | grep -v "ContainerCreating" || echo "No Pending pods found"
fi

echo ""
echo "=== EVENTS SUMMARY ==="

if [ "$KUBECTL_AI_AVAILABLE" = true ]; then
    echo "🔔 Recent cluster events:"
    kubectl-ai show recent events 2>/dev/null || kubectl get events --all-namespaces --sort-by='.lastTimestamp' | tail -20
else
    kubectl get events --all-namespaces --sort-by='.lastTimestamp' | tail -20
fi

echo ""
echo "✅ Cluster health diagnostics completed"
echo ""
echo "💡 Next steps:"
echo "   - Review any problematic pods identified above"
echo "   - Check detailed logs for failing containers"
echo "   - Verify resource requests/limits if resource issues detected"
echo "   - Consult the troubleshooting checklist in references/"

exit 0