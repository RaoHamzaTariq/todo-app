# Kubernetes Deployment Guide

## Prerequisites
1. Docker Desktop running
2. Minikube installed and running with sufficient resources (4 CPU, 8GB RAM)
3. Helm installed
4. kubectl configured to point to your Minikube cluster

## Step 1: Verify Minikube Status
```bash
minikube status
kubectl cluster-info
```

If Minikube is not running or kubectl is misconfigured:
```bash
minikube start --cpus=4 --memory=8192 --driver=docker
minikube update-context
```

## Step 2: Build Docker Images
From the project root directory, build the three application images:

### Frontend Image:
```bash
docker build -t todo-frontend:v1.0.0 -f ./frontend/Dockerfile ./frontend
```

### Backend Image:
```bash
docker build -t todo-backend:v1.0.0 -f ./backend/Dockerfile .
```

### MCP Server Image:
```bash
docker build -t mcp-server:v1.0.0 -f ./mcp-server/Dockerfile .
```

## Step 3: Load Images into Minikube
```bash
minikube image load todo-frontend:v1.0.0
minikube image load todo-backend:v1.0.0
minikube image load mcp-server:v1.0.0
```

## Step 4: Deploy Using Helm
Navigate to the helm directory and install the charts:

```bash
cd helm
helm install todo-frontend ./todo-frontend --set image.tag=v1.0.0
helm install todo-backend ./todo-backend --set image.tag=v1.0.0
helm install mcp-server ./mcp-server --set image.tag=v1.0.0
```

## Step 5: Verify Deployment
Check that all pods are running:
```bash
kubectl get pods
kubectl get services
```

## Step 6: Access the Application
To access the frontend service:
```bash
minikube service todo-frontend-svc --url
```

## Troubleshooting Commands
- Check pod logs: `kubectl logs -f deployment/<deployment-name>`
- Describe pod: `kubectl describe pod <pod-name>`
- Check service endpoints: `kubectl get ep`
- Port forward for testing: `kubectl port-forward svc/<service-name> <local-port>:<service-port>`

## Additional Notes
- The database (Neon PostgreSQL) is external and accessed via environment variables
- All services should be accessible via their respective Kubernetes services
- Environment variables for the applications should be configured in the Helm values files