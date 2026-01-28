# Kubernetes Deployment Guide: Cloud-Native Todo Chatbot

## Prerequisites

Before deploying the Todo Chatbot application to Kubernetes, ensure your system meets the following requirements:

### System Requirements
- **Operating System**: Windows, macOS, or Linux
- **Memory**: Minimum 8GB RAM (16GB recommended)
- **CPU**: Minimum 4 cores (8 cores recommended)
- **Disk Space**: Minimum 20GB free space
- **Architecture**: AMD64/x86_64

### Required Tools
1. **Docker Desktop** with Docker AI Gordon (Windows/macOS) or **Docker Engine** (Linux)
2. **Minikube** (latest version)
3. **kubectl** (latest version)
4. **Helm 3+** (latest version)
5. **kubectl-ai plugin** (for AI-assisted operations)
6. **kagent plugin** (for resource optimization)

### Installation Commands

#### Install Minikube
```bash
# Windows (using Chocolatey)
choco install minikube kubernetes-cli helm

# macOS (using Homebrew)
brew install minikube kubectl helm

# Linux (Ubuntu/Debian)
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube

# Install kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
```

#### Install kubectl-ai and kagent plugins
```bash
# Install kubectl-ai
curl -sSL https://raw.githubusercontent.com/sozercan/kubectl-ai/main/install.sh | bash

# Install kagent (if available)
# Follow instructions from the kagent documentation
```

## Environment Setup

### 1. Verify Prerequisites
```bash
# Verify Docker installation
docker --version
docker info

# Verify Minikube installation
minikube version

# Verify kubectl installation
kubectl version --client

# Verify Helm installation
helm version

# Verify AI-assisted tools
kubectl-ai --help
```

### 2. Start Minikube Cluster
```bash
# Start Minikube with sufficient resources for all services
minikube start --cpus=4 --memory=8192 --disk-size=20g

# Verify cluster is running
kubectl cluster-info
minikube status

# Enable required addons
minikube addons enable ingress
minikube addons enable metrics-server
```

## Building Container Images

### 1. Navigate to Project Directory
```bash
cd /path/to/todo-app
```

### 2. Build Container Images
```bash
# Build frontend image
docker build -t todo-frontend:latest -f frontend/Dockerfile .

# Build backend image
docker build -t todo-backend:latest -f backend/Dockerfile .

# Build MCP server image
docker build -t mcp-server:latest -f mcp-server/Dockerfile .
```

### 3. Load Images into Minikube
```bash
# Load images into Minikube's container runtime
minikube image load todo-frontend:latest
minikube image load todo-backend:latest
minikube image load mcp-server:latest

# Verify images are loaded
minikube ssh docker images | grep todo
```

## Deploying to Kubernetes

### 1. Deploy MCP Server (Dependency First)
```bash
# Deploy MCP server chart first as it's a dependency for the backend AI functionality
helm install mcp-server ./mcp-server \
    --set image.repository=mcp-server \
    --set image.tag=latest \
    --set service.type=ClusterIP \
    --set service.port=8080 \
    --set resources.requests.cpu=50m \
    --set resources.requests.memory=64Mi \
    --set resources.limits.cpu=300m \
    --set resources.limits.memory=256Mi
```

### 2. Deploy Backend Service
```bash
# Deploy backend chart with MCP server connection
helm install todo-backend ./todo-backend \
    --set image.repository=todo-backend \
    --set image.tag=latest \
    --set service.type=ClusterIP \
    --set service.port=8000 \
    --set config.mcpServerUrl=http://mcp-server:8080 \
    --set resources.requests.cpu=100m \
    --set resources.requests.memory=128Mi \
    --set resources.limits.cpu=500m \
    --set resources.limits.memory=512Mi
```

### 3. Deploy Frontend Service
```bash
# Deploy frontend chart with backend connection
helm install todo-frontend ./todo-frontend \
    --set image.repository=todo-frontend \
    --set image.tag=latest \
    --set service.type=NodePort \
    --set service.port=3000 \
    --set config.apiBaseUrl=http://todo-backend:8000 \
    --set resources.requests.cpu=50m \
    --set resources.requests.memory=64Mi \
    --set resources.limits.cpu=200m \
    --set resources.limits.memory=256Mi
```

## Configuration and Secrets

### Create Required Secrets
```bash
# Create JWT secret for authentication (required by Constitution Section VI)
kubectl create secret generic jwt-secret \
    --from-literal=BETTER_AUTH_SECRET=$(openssl rand -base64 32) \
    --dry-run=client -o yaml | kubectl apply -f -

# Create database credentials secret
kubectl create secret generic db-credentials \
    --from-literal=POSTGRES_USER=postgres \
    --from-literal=POSTGRES_PASSWORD=$(openssl rand -base64 16) \
    --from-literal=POSTGRES_DB=tododb \
    --dry-run=client -o yaml | kubectl apply -f -
```

## Verification and Testing

### 1. Check Pod Status
```bash
# Verify all pods are running
kubectl get pods

# Check detailed status of pods
kubectl get pods -o wide

# Use AI-assisted tool to diagnose any issues
kubectl-ai show cluster status
kubectl-ai show pods with issues
```

### 2. Check Service Connectivity
```bash
# Verify services are available
kubectl get services

# Test connectivity between services
kubectl-ai validate service connectivity
kubectl-ai test connectivity between services
```

### 3. Validate Health Probes
```bash
# Check that health checks are passing consistently
kubectl get pods --watch

# Use AI-assisted tool to check health status
kubectl-ai diagnose deployment status
```

### 4. Access the Application
```bash
# Get the frontend service URL
minikube service todo-frontend --url

# Or use port forwarding for testing
kubectl port-forward svc/todo-frontend 3000:3000
```

## Troubleshooting Common Issues

### Pods in CrashLoopBackOff
```bash
# Use AI-assisted diagnostics
kubectl-ai diagnose failing pods
kubectl-ai why is pod crashing
kubectl-ai show logs for pods with CrashLoopBackOff
```

### ImagePullBackOff Errors
```bash
# Use AI-assisted tool to find problematic pods
kubectl-ai find pods with ImagePullBackOff
# Verify images are loaded in Minikube
minikube ssh docker images
# Reload images if necessary
minikube image load <image-name>:<tag>
```

### Pending Pods
```bash
# Use AI-assisted diagnostics
kubectl-ai diagnose pending pods
kubectl-ai explain why pods are pending
# Check node resources
kubectl-ai show node resource usage
```

### Resource Constraints
```bash
# Check resource usage with AI-assisted tools
kubectl-ai analyze resource pressure
kubectl-ai show cluster resource usage
# Use kagent for optimization suggestions
kagent analyze pod-resource conflicts
kagent optimize resource allocation
```

## Post-Deployment Validation

### Verify Constitutional Compliance
```bash
# Verify all pods are running without restarts
kubectl get pods

# Verify services are accessible and responsive
kubectl get svc

# Verify environment variables are correctly set
kubectl-ai show environment for pod todo-backend-*

# Verify MCP tools are registered and accessible
kubectl-ai verify mcp tool access
```

### Test Application Functionality
```bash
# Test endpoint accessibility
curl $(minikube service todo-frontend --url)/api/health

# Verify JWT authentication works
kubectl-ai test environment propagation
```

## Rollback Procedures

### Emergency Rollback
```bash
# Rollback to previous release if issues occur
helm rollback mcp-server
helm rollback todo-backend
helm rollback todo-frontend

# Analyze rollback impact with AI
kubectl-ai analyze rollback impact
```

### Check Deployment History
```bash
# Check deployment history
helm history mcp-server
helm history todo-backend
helm history todo-frontend
```

## Cleanup

### Uninstall Helm Releases
```bash
# Uninstall in reverse order to respect dependencies
helm uninstall todo-frontend
helm uninstall todo-backend
helm uninstall mcp-server
```

### Stop Minikube
```bash
# Stop the Minikube cluster
minikube stop

# Optionally delete the cluster
minikube delete
```

## Advanced Configuration

### Customizing Values
Modify `values.yaml` files in each chart to customize your deployment:
- Adjust replica counts for scaling
- Modify resource requests and limits
- Configure ingress rules for external access
- Set up persistent volumes for data persistence

### Monitoring and Optimization
- Use AI-assisted tools like kubectl-ai and kagent to monitor resource usage
- Implement custom metrics and monitoring dashboards
- Set up alerts for critical failures
- Regularly audit security configurations

## Success Criteria Validation

After deployment, verify the following success criteria are met:

1. **SC-001**: All services deploy successfully with 99% uptime in local Minikube environment
2. **SC-004**: Deployment process completes in under 10 minutes from clean slate
3. **SC-005**: All AI-assisted DevOps tools respond to natural language commands with 95% accuracy
4. **SC-006**: Resource utilization stays within Minikube's default limits (2 CPUs, 4GB RAM)
5. **SC-007**: All existing application features function identically post-deployment
6. **SC-010**: Security scan of generated containers shows zero critical vulnerabilities

## Next Steps

1. Customize values in Helm charts for your specific requirements
2. Implement persistent storage for database persistence
3. Set up monitoring and alerting
4. Configure SSL/TLS certificates for secure communication
5. Implement backup and disaster recovery procedures
6. Scale the deployment based on your user requirements