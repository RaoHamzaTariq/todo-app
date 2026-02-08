# CI/CD Pipeline Examples Reference

## Overview
This document provides detailed configuration examples for CI/CD pipelines used in the Todo Chatbot application. Each pipeline follows best practices for automated deployment from Minikube to Oracle OKE environments.

## GitHub Actions Workflow Templates

### Complete CI/CD Pipeline with Multiple Environments
```yaml
# .github/workflows/todo-chatbot-cicd.yml
name: Todo Chatbot CI/CD Pipeline

on:
  push:
    branches: [ main, develop, feature/** ]
  pull_request:
    branches: [ main ]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME_FRONTEND: ${{ github.repository }}/todo-frontend
  IMAGE_NAME_BACKEND: ${{ github.repository }}/todo-backend
  IMAGE_NAME_MCP: ${{ github.repository }}/mcp-server

jobs:
  # Static analysis and linting
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.13'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install flake8 black mypy

      - name: Lint Python code
        run: |
          flake8 backend/
          black --check backend/
          mypy backend/

      - name: Lint Frontend
        run: |
          cd frontend
          npm ci
          npx eslint . --ext .ts,.tsx
          npx tsc --noEmit

  # Unit tests
  test:
    needs: lint
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.13'

      - name: Cache dependencies
        uses: actions/cache@v3
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
          restore-keys: |
            ${{ runner.os }}-pip-

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r backend/requirements.txt
          pip install pytest pytest-cov

      - name: Run unit tests
        run: |
          pytest backend/tests/ --cov=backend --cov-report=xml

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml

  # Security scanning
  security-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run Trivy vulnerability scanner
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          scan-ref: '.'
          format: 'sarif'
          output: 'trivy-results.sarif'

      - name: Upload Trivy scan results to GitHub Security tab
        uses: github/codeql-action/upload-sarif@v2
        if: always()
        with:
          sarif_file: 'trivy-results.sarif'

  # Build and push container images
  build-and-push:
    needs: [test, security-scan]
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main' || github.ref == 'refs/heads/develop'
    strategy:
      matrix:
        service: [frontend, backend, mcp-server]
    permissions:
      contents: read
      packages: write
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Log in to the Container registry
        uses: docker/login-action@v2
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata (tags, labels) for Docker
        id: meta
        uses: docker/metadata-action@v4
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME_${{ matrix.service }} }}
          tags: |
            type=raw,value=${{ github.sha }}
            type=raw,value=${{ github.ref_name }}
            type=raw,value=latest,enable={{is_default_branch}}

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2

      - name: Build and push Docker image
        uses: docker/build-push-action@v4
        with:
          context: ${{ matrix.service == 'frontend' && './frontend' || '.' }}
          file: ${{ matrix.service == 'frontend' && './frontend/Dockerfile' || format('./{0}/Dockerfile', matrix.service) }}
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

  # Deploy to Development Environment
  deploy-dev:
    needs: build-and-push
    runs-on: ubuntu-latest
    environment: development
    if: github.ref == 'refs/heads/develop'
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Kubectl
        uses: azure/setup-kubectl@v3
        with:
          version: 'latest'

      - name: Setup Helm
        uses: azure/setup-helm@v3
        with:
          version: 'latest'

      - name: Configure KUBECONFIG
        run: |
          echo "${{ secrets.KUBECONFIG_DEV }}" | base64 -d > kubeconfig
          export KUBECONFIG=$PWD/kubeconfig

      - name: Deploy Frontend
        run: |
          helm upgrade --install todo-frontend ./helm/todo-frontend \
            --set image.repository=${{ env.REGISTRY }}/${{ env.IMAGE_NAME_FRONTEND }} \
            --set image.tag=${{ github.sha }} \
            --set service.type=ClusterIP \
            --set replicaCount=1 \
            --namespace todo-dev --create-namespace \
            --atomic \
            --timeout 10m

      - name: Deploy Backend
        run: |
          helm upgrade --install todo-backend ./helm/todo-backend \
            --set image.repository=${{ env.REGISTRY }}/${{ env.IMAGE_NAME_BACKEND }} \
            --set image.tag=${{ github.sha }} \
            --set service.type=ClusterIP \
            --set replicaCount=1 \
            --set database.url="${{ secrets.DEV_DATABASE_URL }}" \
            --set auth.secret="${{ secrets.DEV_AUTH_SECRET }}" \
            --namespace todo-dev \
            --atomic \
            --timeout 10m

      - name: Deploy MCP Server
        run: |
          helm upgrade --install mcp-server ./helm/mcp-server \
            --set image.repository=${{ env.REGISTRY }}/${{ env.IMAGE_NAME_MCP }} \
            --set image.tag=${{ github.sha }} \
            --set service.type=ClusterIP \
            --set replicaCount=1 \
            --namespace todo-dev \
            --atomic \
            --timeout 10m

      - name: Verify deployment
        run: |
          kubectl rollout status deployment/todo-frontend -n todo-dev --timeout=5m
          kubectl rollout status deployment/todo-backend -n todo-dev --timeout=5m
          kubectl rollout status deployment/mcp-server -n todo-dev --timeout=5m

  # Deploy to Staging Environment (with manual approval)
  deploy-staging:
    needs: deploy-dev
    runs-on: ubuntu-latest
    environment: staging
    if: github.ref == 'refs/heads/main'
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Kubectl
        uses: azure/setup-kubectl@v3
        with:
          version: 'latest'

      - name: Setup Helm
        uses: azure/setup-helm@v3
        with:
          version: 'latest'

      - name: Configure KUBECONFIG
        run: |
          echo "${{ secrets.KUBECONFIG_STAGING }}" | base64 -d > kubeconfig
          export KUBECONFIG=$PWD/kubeconfig

      - name: Deploy with Blue-Green Strategy
        run: |
          # Create new release with blue/green labels
          TIMESTAMP=$(date +%s)

          helm upgrade --install todo-frontend-${TIMESTAMP} ./helm/todo-frontend \
            --set image.repository=${{ env.REGISTRY }}/${{ env.IMAGE_NAME_FRONTEND }} \
            --set image.tag=${{ github.sha }} \
            --set service.type=ClusterIP \
            --set replicaCount=2 \
            --set deploymentLabels.deploymentId=${TIMESTAMP} \
            --namespace todo-staging --create-namespace \
            --atomic \
            --timeout 10m

          # Wait for new deployment to be ready
          kubectl rollout status deployment/todo-frontend-${TIMESTAMP} -n todo-staging --timeout=5m

          # Update service to point to new deployment
          kubectl patch service todo-frontend-svc -n todo-staging -p '{"spec":{"selector":{"deploymentId":"'${TIMESTAMP}'"}}}'

          # Clean up old deployment (keeping last 2)
          OLD_DEPLOYMENTS=$(kubectl get deployments -n todo-staging -l app=todo-frontend --sort-by=.metadata.creationTimestamp -o jsonpath='{.items[*].metadata.name}' | tr ' ' '\n' | head -n -2)
          for deployment in $OLD_DEPLOYMENTS; do
            helm uninstall $deployment -n todo-staging
          done

      - name: Run smoke tests
        run: |
          # Get the service IP/URL
          SERVICE_URL=$(kubectl get service todo-frontend-svc -n todo-staging -o jsonpath='{.spec.clusterIP}')

          # Simple health check
          for i in {1..30}; do
            if curl -f http://$SERVICE_URL:3000/health; then
              echo "Health check passed"
              break
            fi
            sleep 10
          done

  # Deploy to Production Environment (with manual approval and canary release)
  deploy-production:
    needs: deploy-staging
    runs-on: ubuntu-latest
    environment: production
    if: github.ref == 'refs/heads/main' && contains(github.event.head_commit.message, '[deploy]')
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Kubectl
        uses: azure/setup-kubectl@v3
        with:
          version: 'latest'

      - name: Setup Helm
        uses: azure/setup-helm@v3
        with:
          version: 'latest'

      - name: Configure KUBECONFIG
        run: |
          echo "${{ secrets.KUBECONFIG_PROD }}" | base64 -d > kubeconfig
          export KUBECONFIG=$PWD/kubeconfig

      - name: Canary deployment
        run: |
          # Deploy 10% of traffic to new version initially
          helm upgrade --install todo-frontend-canary ./helm/todo-frontend \
            --set image.repository=${{ env.REGISTRY }}/${{ env.IMAGE_NAME_FRONTEND }} \
            --set image.tag=${{ github.sha }} \
            --set service.type=LoadBalancer \
            --set replicaCount=1 \
            --set deploymentLabels.version=canary \
            --namespace todo-prod --create-namespace \
            --atomic \
            --timeout 10m

          # Wait for canary to be ready
          kubectl rollout status deployment/todo-frontend-canary -n todo-prod --timeout=5m

          # Run canary tests
          CANARY_SERVICE_IP=$(kubectl get service todo-frontend-canary-svc -n todo-prod -o jsonpath='{.status.loadBalancer.ingress[0].ip}')

          # Run tests against canary deployment
          for i in {1..10}; do
            if curl -f http://$CANARY_SERVICE_IP:3000/health; then
              echo "Canary health check passed"
            else
              echo "Canary health check failed"
              exit 1
            fi
            sleep 30
          done

          # If canary tests pass, promote to full deployment
          helm upgrade --install todo-frontend ./helm/todo-frontend \
            --set image.repository=${{ env.REGISTRY }}/${{ env.IMAGE_NAME_FRONTEND }} \
            --set image.tag=${{ github.sha }} \
            --set service.type=LoadBalancer \
            --set replicaCount=3 \
            --namespace todo-prod \
            --atomic \
            --timeout 10m

          # Wait for full deployment
          kubectl rollout status deployment/todo-frontend -n todo-prod --timeout=10m

          # Clean up canary deployment
          helm uninstall todo-frontend-canary -n todo-prod

  # Post-deployment validation
  post-deploy-validation:
    needs: [deploy-dev, deploy-staging, deploy-production]
    runs-on: ubuntu-latest
    strategy:
      matrix:
        environment: [dev, staging, prod]
    steps:
      - name: Validate deployment
        run: |
          # Add validation steps specific to each environment
          echo "Validating deployment in ${{ matrix.environment }} environment"

          # Example: check if services are responding
          # Example: verify expected number of pods are running
          # Example: run integration tests
```

## Monitoring and Observability Configuration

### Prometheus Configuration for Kubernetes
```yaml
# prometheus-k8s-config.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: prometheus-config
  namespace: monitoring
data:
  prometheus.yml: |
    global:
      scrape_interval: 15s
      evaluation_interval: 15s

    rule_files:
      - "alert_rules.yml"

    scrape_configs:
      - job_name: 'kubernetes-apiservers'
        kubernetes_sd_configs:
        - role: endpoints
        scheme: https
        tls_config:
          ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
        bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token
        relabel_configs:
        - source_labels: [__meta_kubernetes_namespace, __meta_kubernetes_service_name, __meta_kubernetes_endpoint_port_name]
          action: keep
          regex: default;kubernetes;https

      - job_name: 'kubernetes-nodes'
        kubernetes_sd_configs:
        - role: node
        scheme: https
        tls_config:
          ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
        bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token
        relabel_configs:
        - action: labelmap
          regex: __meta_kubernetes_node_label_(.+)
        - target_label: __address__
          replacement: kubernetes.default.svc:443
        - source_labels: [__meta_kubernetes_node_name]
          regex: (.+)
          target_label: __metrics_path__
          replacement: /api/v1/nodes/${1}/proxy/metrics

      - job_name: 'todo-frontend'
        kubernetes_sd_configs:
        - role: pod
        relabel_configs:
        - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
          action: keep
          regex: true
        - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
          action: replace
          target_label: __metrics_path__
          regex: (.+)
        - source_labels: [__address__, __meta_kubernetes_pod_annotation_prometheus_io_port]
          action: replace
          regex: ([^:]+)(?::\d+)?;(\d+)
          replacement: $1:$2
          target_label: __address__
        - action: labelmap
          regex: __meta_kubernetes_pod_label_(.+)
        - source_labels: [__meta_kubernetes_namespace]
          action: replace
          target_label: kubernetes_namespace
        - source_labels: [__meta_kubernetes_pod_name]
          action: replace
          target_label: kubernetes_pod_name
```

### Alert Rules Configuration
```yaml
# alert_rules.yml
groups:
  - name: todo-app-alerts
    rules:
      - alert: TodoFrontendDown
        expr: up{job="todo-frontend"} == 0
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "Todo Frontend is down"
          description: "Todo Frontend has been down for more than 2 minutes."

      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5..", job="todo-backend"}[5m]) > 0.1
        for: 2m
        labels:
          severity: warning
        annotations:
          summary: "High error rate in Todo Backend"
          description: "More than 10% of requests are resulting in 5xx errors over the last 5 minutes."

      - alert: HighCPUUsage
        expr: 100 - (avg by(instance) (irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100) > 80
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High CPU usage"
          description: "CPU usage is above 80% for more than 5 minutes."

      - alert: PodRestartingFrequently
        expr: increase(kube_pod_container_status_restarts_total[15m]) > 5
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Pod restarting frequently"
          description: "Pod has restarted more than 5 times in the last 15 minutes."
```

## Helm Chart Enhancement for Observability

### ServiceMonitor for Prometheus (for use in Helm charts)
```yaml
# helm/todo-frontend/templates/servicemonitor.yaml
{{- if .Values.prometheus.enabled }}
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: {{ include "todo-frontend.fullname" . }}
  labels:
    {{- include "todo-frontend.labels" . | nindent 4 }}
spec:
  selector:
    matchLabels:
      {{- include "todo-frontend.selectorLabels" . | nindent 6 }}
  endpoints:
  - port: http
    interval: 30s
    path: /metrics
{{- end }}
```

### Values for observability
```yaml
# helm/todo-frontend/values.yaml
prometheus:
  enabled: true
  serviceMonitor:
    interval: 30s
    path: /metrics

grafana:
  dashboard:
    enabled: true
    annotations:
      grafana_folder: "Todo App Dashboards"

# Other values...
```

## GitHub Actions Secrets Management

### Recommended Secrets Structure
```
# Development Environment
DEV_DATABASE_URL
DEV_AUTH_SECRET
KUBECONFIG_DEV

# Staging Environment
STAGING_DATABASE_URL
STAGING_AUTH_SECRET
KUBECONFIG_STAGING

# Production Environment
PROD_DATABASE_URL
PROD_AUTH_SECRET
KUBECONFIG_PROD

# Container Registry
DOCKER_USERNAME
DOCKER_PASSWORD

# External Services
OPENAI_API_KEY
NEON_DB_URL
```

## Pipeline Validation Script

### Validate Pipeline Configuration
```bash
#!/bin/bash
# validate_pipeline.sh

echo "Validating GitHub Actions pipeline..."

# Check if required files exist
REQUIRED_FILES=(
  ".github/workflows/ci-cd-pipeline.yml"
  "backend/requirements.txt"
  "frontend/package.json"
  "helm/todo-frontend/Chart.yaml"
  "helm/todo-backend/Chart.yaml"
  "helm/mcp-server/Chart.yaml"
)

for file in "${REQUIRED_FILES[@]}"; do
  if [ ! -f "$file" ]; then
    echo "❌ Missing required file: $file"
    exit 1
  else
    echo "✅ Found required file: $file"
  fi
done

# Validate Helm charts
echo "Validating Helm charts..."
for chart in "todo-frontend" "todo-backend" "mcp-server"; do
  if helm lint "helm/$chart" >/dev/null 2>&1; then
    echo "✅ Helm chart valid: $chart"
  else
    echo "❌ Helm chart invalid: $chart"
    helm lint "helm/$chart"
    exit 1
  fi
done

# Validate Dockerfiles
echo "Validating Dockerfiles..."
for dockerfile in "backend/Dockerfile" "frontend/Dockerfile" "mcp-server/Dockerfile"; do
  if [ -f "$dockerfile" ]; then
    echo "✅ Found Dockerfile: $dockerfile"
  else
    echo "❌ Missing Dockerfile: $dockerfile"
    exit 1
  fi
done

echo "Pipeline validation completed successfully!"
```

## Oracle OKE Specific Configuration

### OKE Deployment Configuration
```yaml
# oke-values.yaml
# Oracle OKE specific values
global:
  oke:
    enabled: true
    region: us-ashburn-1
    compartmentId: ocid1.compartment.oc1...
    clusterId: ocid1.cluster.oc1...

image:
  registry: ocir.io
  repository: ashburn/mytenancy/todo-app

service:
  type: LoadBalancer
  annotations:
    service.beta.kubernetes.io/oci-load-balancer-internal: "false"
    service.beta.kubernetes.io/oci-load-balancer-shape: "flexible"
    service.beta.kubernetes.io/oci-load-balancer-minimum-weight: "10"
    service.beta.kubernetes.io/oci-load-balancer-maximum-weight: "100"

resources:
  limits:
    cpu: 1000m
    memory: 2Gi
  requests:
    cpu: 500m
    memory: 1Gi

autoscaling:
  enabled: true
  minReplicas: 3
  maxReplicas: 10
  targetCPUUtilizationPercentage: 70
  targetMemoryUtilizationPercentage: 80

nodeSelector:
  node_pool: production-pool

tolerations:
- key: "dedicated"
  operator: "Equal"
  value: "production"
  effect: "NoSchedule"
```