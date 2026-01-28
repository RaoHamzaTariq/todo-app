#!/bin/bash
# analyze-pod-failures.sh
# Script to analyze specific pod failures and provide detailed diagnostics

set -e

POD_NAME=${1:-""}
NAMESPACE=${2:-"default"}

if [ -z "$POD_NAME" ]; then
    echo "Usage: $0 <pod-name> [namespace]"
    echo "Analyzes a specific pod for failure causes"
    exit 1
fi

echo "🔍 Analyzing pod: $POD_NAME in namespace: $NAMESPACE"

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
fi

echo ""
echo "=== POD BASIC INFORMATION ==="

if [ "$KUBECTL_AI_AVAILABLE" = true ]; then
    kubectl-ai describe pod "$POD_NAME" -n "$NAMESPACE" 2>/dev/null || kubectl describe pod "$POD_NAME" -n "$NAMESPACE"
else
    kubectl describe pod "$POD_NAME" -n "$NAMESPACE"
fi

echo ""
echo "=== POD STATUS ANALYSIS ==="

# Get pod status
POD_STATUS=$(kubectl get pod "$POD_NAME" -n "$NAMESPACE" -o jsonpath='{.status.phase}')
echo "Pod Phase: $POD_STATUS"

# Check for specific error conditions
CONTAINER_STATUSES=$(kubectl get pod "$POD_NAME" -n "$NAMESPACE" -o jsonpath='{.status.containerStatuses[*].state}')

if [[ "$CONTAINER_STATUSES" == *"crashLoopBackOff"* ]]; then
    echo "🚨 DETECTED: CrashLoopBackOff"
elif [[ "$CONTAINER_STATUSES" == *"waiting"* ]]; then
    REASON=$(kubectl get pod "$POD_NAME" -n "$NAMESPACE" -o jsonpath='{.status.containerStatuses[].state.waiting.reason}')
    if [ "$REASON" = "ImagePullBackOff" ]; then
        echo "🚨 DETECTED: ImagePullBackOff"
    elif [ "$REASON" = "ErrImagePull" ]; then
        echo "🚨 DETECTED: ErrImagePull"
    else
        echo "⏳ Container waiting: $REASON"
    fi
fi

echo ""
echo "=== CONTAINER STATUS DETAILS ==="

kubectl get pod "$POD_NAME" -n "$NAMESPACE" -o jsonpath="{range .status.containerStatuses[*]}Container Name: {.name}{'\n'}Ready: {.ready}{'\n'}Restart Count: {.restartCount}{'\n'}State: {range .state}{@}{end}{'\n'}{'\n'}{end}"

echo ""
echo "=== LOG ANALYSIS ==="

if [ "$KUBECTL_AI_AVAILABLE" = true ]; then
    echo "📄 Container logs:"
    kubectl-ai show logs for pod "$POD_NAME" -n "$NAMESPACE" 2>/dev/null || {
        kubectl logs "$POD_NAME" -n "$NAMESPACE" --tail=50
        echo ""
        echo "🔄 Previous container logs (if restarted):"
        kubectl logs "$POD_NAME" -n "$NAMESPACE" --previous --tail=50 2>/dev/null || echo "No previous logs available"
    }
else
    kubectl logs "$POD_NAME" -n "$NAMESPACE" --tail=50
    echo ""
    echo "🔄 Previous container logs (if restarted):"
    kubectl logs "$POD_NAME" -n "$NAMESPACE" --previous --tail=50 2>/dev/null || echo "No previous logs available"
fi

echo ""
echo "=== RESOURCE CONFIGURATION ==="

if [ "$KUBECTL_AI_AVAILABLE" = true ]; then
    kubectl-ai check resource configuration for pod "$POD_NAME" -n "$NAMESPACE" 2>/dev/null || {
        echo "Requests and Limits:"
        kubectl get pod "$POD_NAME" -n "$NAMESPACE" -o jsonpath="{range .spec.containers[*]}Container: {.name}{'\n'}Requests: {range .resources.requests}{@}={.}{'\n'}{end}Limits: {range .resources.limits}{@}={.}{'\n'}{end}{'\n'}{end}"
    }
else
    echo "Requests and Limits:"
    kubectl get pod "$POD_NAME" -n "$NAMESPACE" -o jsonpath="{range .spec.containers[*]}Container: {.name}{'\n'}Requests: {range .resources.requests}{@}={.}{'\n'}{end}Limits: {range .resources.limits}{@}={.}{'\n'}{end}{'\n'}{end}"
fi

echo ""
echo "=== EVENTS FOR POD ==="

if [ "$KUBECTL_AI_AVAILABLE" = true ]; then
    kubectl-ai show events for pod "$POD_NAME" -n "$NAMESPACE" 2>/dev/null || kubectl get events -n "$NAMESPACE" --field-selector involvedObject.name="$POD_NAME" --sort-by='.lastTimestamp'
else
    kubectl get events -n "$NAMESPACE" --field-selector involvedObject.name="$POD_NAME" --sort-by='.lastTimestamp'
fi

echo ""
echo "=== NODE INFORMATION ==="

NODE_NAME=$(kubectl get pod "$POD_NAME" -n "$NAMESPACE" -o jsonpath='{.spec.nodeName}')
if [ -n "$NODE_NAME" ]; then
    echo "Node: $NODE_NAME"
    if [ "$KUBECTL_AI_AVAILABLE" = true ]; then
        kubectl-ai describe node "$NODE_NAME" 2>/dev/null || kubectl describe node "$NODE_NAME"
    else
        kubectl describe node "$NODE_NAME"
    fi
else
    echo "Pod not scheduled to any node yet"
fi

echo ""
echo "=== POTENTIAL ROOT CAUSES ==="

# Analyze potential causes based on gathered information
CAUSES=()

# Check for CrashLoopBackOff
if [[ "$CONTAINER_STATUSES" == *"crashLoopBackOff"* ]]; then
    CAUSES+=("Application startup failure")
    CAUSES+=("Configuration error")
    CAUSES+=("Missing dependencies")
    CAUSES+=("Insufficient resources")
    CAUSES+=("Permission issues")
fi

# Check for ImagePullBackOff
if [[ "$REASON" == "ImagePullBackOff" ]]; then
    CAUSES+=("Image doesn't exist in registry")
    CAUSES+=("Invalid image name/tag")
    CAUSES+=("Missing or invalid image pull secret")
    CAUSES+=("Registry authentication failure")
fi

# Check for resource issues
REQUESTS_CPU=$(kubectl get pod "$POD_NAME" -n "$NAMESPACE" -o jsonpath='{.spec.containers[0].resources.requests.cpu}')
LIMITS_MEM=$(kubectl get pod "$POD_NAME" -n "$NAMESPACE" -o jsonpath='{.spec.containers[0].resources.limits.memory}')

if [ -n "$LIMITS_MEM" ] && [ "$LIMITS_MEM" != "0" ]; then
    CAUSES+=("Memory limit too low causing OOM kills")
fi

if [ ${#CAUSES[@]} -eq 0 ]; then
    echo "No specific root causes identified. Check logs and events above for more details."
else
    for cause in "${CAUSES[@]}"; do
        echo "- $cause"
    done
fi

echo ""
echo "=== RECOMMENDATIONS ==="

if [[ "$CONTAINER_STATUSES" == *"crashLoopBackOff"* ]]; then
    echo "🔧 For CrashLoopBackOff:"
    echo "  - Check application logs for startup errors"
    echo "  - Verify environment variables and configuration"
    echo "  - Increase resource limits if insufficient"
    echo "  - Check container entrypoint and command"
elif [[ "$REASON" == "ImagePullBackOff" ]]; then
    echo "🔧 For ImagePullBackOff:"
    echo "  - Verify image name and tag are correct"
    echo "  - Check image pull secret configuration"
    echo "  - Confirm registry accessibility"
elif [ "$POD_STATUS" = "Pending" ]; then
    echo "🔧 For Pending pods:"
    echo "  - Check node availability and resources"
    echo "  - Verify node selectors and affinities"
    echo "  - Check resource quotas in namespace"
fi

echo ""
echo "✅ Pod analysis completed"