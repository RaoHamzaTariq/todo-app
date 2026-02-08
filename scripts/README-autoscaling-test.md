# Auto-scaling Test for Todo App

This script simulates load on the backend service to test the Horizontal Pod Autoscaler (HPA) functionality.

## Prerequisites

- Kubernetes cluster with the Todo App deployed
- `kubectl` configured to connect to the cluster
- `curl` installed on the machine running the test

## Running the Test

1. Make the script executable:
   ```bash
   chmod +x scripts/autoscaling-test.sh
   ```

2. Run the test with default parameters:
   ```bash
   ./scripts/autoscaling-test.sh
   ```

3. Or run with custom parameters:
   ```bash
   BACKEND_SERVICE_URL="http://your-backend-service:8000" \
   TEST_DURATION=600 \
   CONCURRENT_REQUESTS=20 \
   ./scripts/autoscaling-test.sh
   ```

## Parameters

- `BACKEND_SERVICE_URL`: The URL of the backend service (default: `http://localhost:8000`)
- `TEST_DURATION`: Duration of the test in seconds (default: `300` for 5 minutes)
- `CONCURRENT_REQUESTS`: Number of concurrent requests to send (default: `10`)

## What the Test Does

1. Sends continuous requests to the backend service to increase CPU usage
2. Monitors the pod count during the test to see if HPA triggers scaling
3. Reports the final status of pods and HPA configuration

## Expected Results

During the test, you should see:
- Increased CPU usage on the backend pods
- HPA triggering scaling events when CPU threshold is exceeded
- Increase in the number of backend pods up to the maximum configured

After the test, the pods should eventually scale back down based on the configured cooldown period.