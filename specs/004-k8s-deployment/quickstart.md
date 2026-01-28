# Quickstart Guide: Phase IV Kubernetes Deployment

## Prerequisites

1. **System Requirements**:
   - Docker Desktop with Docker AI Gordon enabled
   - Minikube (latest version)
   - kubectl
   - Helm 3+
   - kubectl-ai plugin
   - kagent plugin

2. **Environment Setup**:
   ```bash
   # Verify Docker installation and AI features
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
   kagent --help
   ```

## Starting the Local Kubernetes Cluster

1. **Start Minikube Cluster**:
   ```bash
   # Start Minikube with sufficient resources for all services
   minikube start --cpus=4 --memory=8192 --disk-size=20g

   # Verify cluster is running
   kubectl cluster-info
   minikube status
   ```

2. **Enable Required Minikube Addons**:
   ```bash
   # Enable ingress addon for external access
   minikube addons enable ingress

   # Verify addons are enabled
   minikube addons list
   ```

## Containerization Process

1. **Analyze Projects with Docker AI Gordon**:
   ```bash
   # Analyze the frontend project for containerization
   docker-ai analyze-project ./frontend

   # Analyze the backend project for containerization
   docker-ai analyze-project ./backend

   # Analyze the MCP server project for containerization
   docker-ai analyze-project ./mcp-server
   ```

2. **Generate Optimized Dockerfiles**:
   ```bash
   # Generate optimized Dockerfile for frontend using Docker AI Gordon
   cd frontend && docker-ai generate-dockerfile . && cd ..

   # Generate optimized Dockerfile for backend using Docker AI Gordon
   cd backend && docker-ai generate-dockerfile . && cd ..

   # Generate optimized Dockerfile for MCP server using Docker AI Gordon
   cd mcp-server && docker-ai generate-dockerfile . && cd ..
   ```

3. **Build Container Images**:
   ```bash
   # Build frontend image with AI-optimized Dockerfile
   docker build -t todo-frontend:latest -f ./frontend/Dockerfile .

   # Build backend image with AI-optimized Dockerfile
   docker build -t todo-backend:latest -f ./backend/Dockerfile .

   # Build MCP server image with AI-optimized Dockerfile
   docker build -t mcp-server:latest -f ./mcp-server/Dockerfile .

   # Verify images were created and optimized
   docker images | grep todo
   ```

4. **Load Images into Minikube**:
   ```bash
   # Load images into Minikube's container runtime
   minikube image load todo-frontend:latest
   minikube image load todo-backend:latest
   minikube image load mcp-server:latest

   # Verify images are in Minikube
   minikube ssh docker images | grep todo
   ```

## Helm Chart Generation

1. **Create Helm Chart Structure**:
   ```bash
   # Create Helm chart for frontend
   helm create todo-frontend

   # Create Helm chart for backend
   helm create todo-backend

   # Create Helm chart for MCP server
   helm create mcp-server
   ```

2. **Configure Helm Charts with Service-Specific Settings**:
   ```bash
   # Configure frontend chart with Next.js specific resource requests/limits
   # Edit values.yaml in todo-frontend/ to set:
   # resources:
   #   limits:
   #     cpu: 200m
   #     memory: 256Mi
   #   requests:
   #     cpu: 50m
   #     memory: 64Mi

   # Configure backend chart with FastAPI specific resource requests/limits
   # Edit values.yaml in todo-backend/ to set:
   # resources:
   #   limits:
   #     cpu: 500m
   #     memory: 512Mi
   #   requests:
   #     cpu: 100m
   #     memory: 128Mi

   # Configure MCP server chart with MCP-specific resource requests/limits
   # Edit values.yaml in mcp-server/ to set:
   # resources:
   #   limits:
   #     cpu: 300m
   #     memory: 256Mi
   #   requests:
   #     cpu: 50m
   #     memory: 64Mi
   ```

## Kubernetes Deployment

1. **Deploy MCP Server First** (Dependency):
   ```bash
   # Deploy MCP server chart first as it's a dependency for the backend AI functionality
   helm install mcp-server ./mcp-server \
       --set image.repository=mcp-server \
       --set image.tag=latest \
       --set service.type=ClusterIP \
       --set service.port=8080
   ```

2. **Deploy Backend** (Second):
   ```bash
   # Deploy backend chart with MCP server connection
   helm install todo-backend ./todo-backend \
       --set image.repository=todo-backend \
       --set image.tag=latest \
       --set service.type=ClusterIP \
       --set service.port=8000 \
       --set mcp.server.url=http://mcp-server:8080 \
       --set resources.requests.cpu=100m \
       --set resources.requests.memory=128Mi \
       --set resources.limits.cpu=500m \
       --set resources.limits.memory=512Mi
   ```

3. **Deploy Frontend** (Last):
   ```bash
   # Deploy frontend chart with backend connection
   helm install todo-frontend ./todo-frontend \
       --set image.repository=todo-frontend \
       --set image.tag=latest \
       --set service.type=NodePort \
       --set service.port=3000 \
       --set backend.apiUrl=http://todo-backend:8000 \
       --set resources.requests.cpu=50m \
       --set resources.requests.memory=64Mi \
       --set resources.limits.cpu=200m \
       --set resources.limits.memory=256Mi
   ```

## Configuration and Secrets

1. **Create Required Secrets**:
   ```bash
   # Create JWT secret for authentication (required by Constitution Section VI)
   kubectl create secret generic jwt-secret \
       --from-literal=BETTER_AUTH_SECRET="your-jwt-secret-key-here"

   # Create database credentials secret
   kubectl create secret generic db-credentials \
       --from-literal=POSTGRES_USER="postgres" \
       --from-literal=POSTGRES_PASSWORD="your-db-password" \
       --from-literal=POSTGRES_DB="tododb"
   ```

2. **Verify Configuration**:
   ```bash
   # Check if secrets were created
   kubectl get secrets

   # Check if ConfigMaps were created by Helm
   kubectl get configmaps

   # Use AI-assisted tool to verify configuration
   kubectl-ai show environment for pod todo-backend-*
   ```

## Verification and Testing

1. **Check Pod Status**:
   ```bash
   # Verify all pods are running
   kubectl get pods

   # Check detailed status of pods
   kubectl get pods -o wide

   # Use AI-assisted tool to diagnose any issues
   kubectl-ai show cluster status
   kubectl-ai show pods with issues
   ```

2. **Check Service Connectivity**:
   ```bash
   # Verify services are available
   kubectl get services

   # Test connectivity between services
   kubectl-ai validate service connectivity
   kubectl-ai test connectivity between services
   ```

3. **Validate Health Probes**:
   ```bash
   # Check that health checks are passing consistently
   kubectl get pods --watch

   # Use AI-assisted tool to check health status
   kubectl-ai diagnose deployment status
   ```

4. **Access the Application**:
   ```bash
   # Get the frontend service URL
   minikube service todo-frontend --url

   # Or use port forwarding for testing
   kubectl port-forward svc/todo-frontend 3000:3000
   ```

## Troubleshooting Common Issues

1. **Pods in CrashLoopBackOff**:
   ```bash
   # Use AI-assisted diagnostics
   kubectl-ai diagnose failing pods
   kubectl-ai why is pod crashing
   kubectl-ai show logs for pods with CrashLoopBackOff
   ```

2. **ImagePullBackOff Errors**:
   ```bash
   # Use AI-assisted tool to find problematic pods
   kubectl-ai find pods with ImagePullBackOff
   # Verify images are loaded in Minikube
   minikube ssh docker images
   # Reload images if necessary
   minikube image load <image-name>:<tag>
   ```

3. **Pending Pods**:
   ```bash
   # Use AI-assisted diagnostics
   kubectl-ai diagnose pending pods
   kubectl-ai explain why pods are pending
   # Check node resources
   kubectl-ai show node resource usage
   ```

4. **Resource Constraints**:
   ```bash
   # Check resource usage with AI-assisted tools
   kubectl-ai analyze resource pressure
   kubectl-ai show cluster resource usage
   # Use kagent for optimization suggestions
   kagent analyze pod-resource conflicts
   kagent optimize resource allocation
   ```

## Post-Deployment Validation

1. **Verify Constitutional Compliance**:
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

2. **Test Application Functionality**:
   ```bash
   # Test endpoint accessibility
   curl $(minikube service todo-frontend --url)/api/health

   # Verify JWT authentication works
   kubectl-ai test environment propagation
   ```

## Rollback Procedures

1. **Emergency Rollback**:
   ```bash
   # Rollback to previous release if issues occur
   helm rollback mcp-server
   helm rollback todo-backend
   helm rollback todo-frontend

   # Analyze rollback impact with AI
   kubectl-ai analyze rollback impact
   ```

2. **Check Deployment History**:
   ```bash
   # Check deployment history
   helm history mcp-server
   helm history todo-backend
   helm history todo-frontend
   ```

## Cleanup

1. **Uninstall Helm Releases**:
   ```bash
   # Uninstall in reverse order to respect dependencies
   helm uninstall todo-frontend
   helm uninstall todo-backend
   helm uninstall mcp-server
   ```

2. **Stop Minikube**:
   ```bash
   # Stop the Minikube cluster
   minikube stop

   # Optionally delete the cluster
   minikube delete
   ```

## Next Steps

1. **Customize Values**: Modify `values.yaml` files in each chart to customize your deployment
2. **Scale Services**: Use `helm upgrade` to adjust replica counts and resource allocations
3. **Configure Ingress**: Set up ingress rules to access services via domain names
4. **Monitor Performance**: Use AI-assisted tools like kubectl-ai and kagent to monitor resource usage and optimize performance
5. **Run Validation Tests**: Execute the validation steps from the implementation plan to ensure all constitutional requirements are met