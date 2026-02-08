#!/bin/bash

# Auto-scaling test script for Todo App
# This script simulates load on the backend service to test HPA functionality

set -e

echo "Starting auto-scaling test..."

# Define variables
BACKEND_SERVICE_URL=${BACKEND_SERVICE_URL:-"http://localhost:8000"}
TEST_DURATION=${TEST_DURATION:-300}  # 5 minutes
CONCURRENT_REQUESTS=${CONCURRENT_REQUESTS:-10}

echo "Test parameters:"
echo "  Backend Service URL: $BACKEND_SERVICE_URL"
echo "  Test Duration: $TEST_DURATION seconds"
echo "  Concurrent Requests: $CONCURRENT_REQUESTS"

# Function to send requests to the backend
send_requests() {
    local duration=$1
    local concurrency=$2
    local end_time=$(($(date +%s) + $duration))
    
    echo "Sending load to $BACKEND_SERVICE_URL for $duration seconds with $concurrency concurrent requests..."
    
    while [ $(date +%s) -lt $end_time ]; do
        # Send concurrent requests in the background
        for i in $(seq 1 $concurrency); do
            # Send a request to the health endpoint to simulate load
            curl -s "$BACKEND_SERVICE_URL/health" > /dev/null 2>&1 &
            
            # Also send a request to the tasks endpoint to generate more realistic load
            curl -s "$BACKEND_SERVICE_URL/api/test_user/tasks" > /dev/null 2>&1 &
        done
        
        # Wait a bit before sending the next batch
        sleep 0.5
    done
}

# Function to monitor pods during the test
monitor_pods() {
    local namespace=${1:-"todo-app"}
    local deployment_name=${2:-"todo-backend"}
    
    echo "Monitoring pods in namespace: $namespace, deployment: $deployment"
    
    # Print initial state
    echo "Initial pod count:"
    kubectl get pods -n $namespace | grep $deployment | wc -l
    
    # Monitor every 30 seconds during the test
    local test_end_time=$(($(date +%s) + $TEST_DURATION + 30))  # Add 30s buffer
    while [ $(date +%s) -lt $test_end_time ]; do
        local current_time=$(date '+%Y-%m-%d %H:%M:%S')
        local pod_count=$(kubectl get pods -n $namespace | grep $deployment | grep -c -E "(Running|ContainerCreating)")
        local total_pods=$(kubectl get pods -n $namespace | grep $deployment | wc -l)
        
        echo "[$current_time] Pod count for $deployment: $pod_count/$total_pods"
        
        # Also get HPA status
        if kubectl get hpa -n $namespace | grep -q $deployment; then
            kubectl get hpa $deployment -n $namespace
        fi
        
        sleep 30
    done
}

# Start monitoring in the background
monitor_pods "todo-app" "todo-backend" &
MONITOR_PID=$!

# Start sending requests
send_requests $TEST_DURATION $CONCURRENT_REQUESTS

# Wait for monitoring to complete
wait $MONITOR_PID

echo "Auto-scaling test completed."

# Final status check
echo "Final pod status:"
kubectl get pods -n todo-app

echo "Final HPA status:"
kubectl get hpa -n todo-app

echo "Auto-scaling test finished. Check the pod count to verify if scaling occurred."