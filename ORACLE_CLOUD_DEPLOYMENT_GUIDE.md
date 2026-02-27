# Oracle Cloud Deployment Guide for Todo Chatbot Application

## Overview

This guide provides instructions for deploying the Todo Chatbot application on Oracle Cloud Infrastructure (OCI) using Oracle Kubernetes Engine (OKE) with Dapr, Kafka, and Supabase integration.

## Prerequisites

1. **Oracle Cloud Account** with appropriate permissions
2. **OCI CLI** installed and configured
3. **kubectl** installed
4. **Helm 3** installed
5. **Dapr CLI** installed
6. **PostgreSQL Database** (either Oracle Autonomous Database or self-managed)

## Architecture Overview

The application will be deployed with the following architecture on Oracle Cloud:

- **Oracle Kubernetes Engine (OKE)**: Managed Kubernetes cluster
- **Dapr**: Distributed Application Runtime for service-to-service invocation, state management, and pub/sub
- **Apache Kafka**: Event streaming platform (can be self-hosted on OKE or use a managed service)
- **PostgreSQL**: Database service (either Oracle Autonomous Database or self-managed PostgreSQL)
- **Application Components**:
  - Frontend: Next.js application
  - Backend: FastAPI application with MCP integration
  - Event Services: Reminder, Recurring Task, Audit Log, Notification services

## Step 1: Set up Oracle Cloud Infrastructure

### 1.1 Create an OKE Cluster

```bash
# Create a new compartment (optional but recommended)
oci iam compartment create --compartment-id <your_tenancy_ocid> \
  --name "todo-app-compartment" \
  --description "Compartment for Todo App resources"

# Create a VCN for the cluster
oci network vcn create --compartment-id <compartment_ocid> \
  --display-name todo-app-vcn \
  --cidr-block 10.0.0.0/16

# Create the OKE cluster
oci ce cluster create --name todo-app-cluster \
  --kubernetes-version v1.28.2 \
  --vcn-id <vcn_ocid> \
  --service-lb-subnet-ids <subnet_id_1>,<subnet_id_2> \
  --compartment-id <compartment_ocid>
```

### 1.2 Get Cluster Credentials

```bash
# Get the cluster's OCID from the list
oci ce cluster list --compartment-id <compartment_ocid>

# Generate kubeconfig
oci ce cluster create-kubeconfig --cluster-id <cluster_ocid> \
  --file ~/.kube/config \
  --region <region> \
  --token-version 2.0.0

# Verify connection
kubectl get nodes
```

## Step 2: Install Dapr on OKE

```bash
# Verify Dapr CLI is installed
dapr --version

# Install Dapr on the cluster
dapr init -k

# Verify Dapr is running
dapr status -k
```

## Step 3: Set up Kafka on OKE

For production, you can either use a managed Kafka service or deploy Kafka on OKE:

### Option A: Self-Hosted Kafka (using Strimzi)

```bash
# Add Strimzi Helm repository
helm repo add strimzi https://strimzi.io/charts/
helm repo update

# Install Strimzi operator
helm install strimzi strimzi/strimzi-kafka-operator \
  --namespace kafka \
  --create-namespace

# Create a Kafka cluster
kubectl apply -f - <<EOF
apiVersion: kafka.strimzi.io/v1beta2
kind: Kafka
metadata:
  name: todo-kafka
  namespace: kafka
spec:
  kafka:
    version: 3.7.0
    replicas: 3
    listeners:
      - name: plain
        port: 9092
        type: internal
        tls: false
      - name: tls
        port: 9093
        type: internal
        tls: true
    config:
      offsets.topic.replication.factor: 3
      transaction.state.log.replication.factor: 3
      transaction.state.log.min.isr: 2
      default.replication.factor: 3
      min.insync.replicas: 2
      inter.broker.protocol.version: "3.7"
    storage:
      type: jbod
      volumes:
      - id: 0
        type: persistent-claim
        size: 10Gi
        deleteClaim: false
  zookeeper:
    replicas: 3
    storage:
      type: persistent-claim
      size: 5Gi
      deleteClaim: false
  entityOperator:
    topicOperator: {}
    userOperator: {}
EOF
```

### Option B: Managed Kafka Service

If using a managed service like Oracle Streaming Service or a third-party service, note the connection details for later configuration.

## Step 4: Configure PostgreSQL Database

You have two options for PostgreSQL on Oracle Cloud:

**Option A: Oracle Autonomous Database (Recommended)**
1. Create an Autonomous Transaction Processing (ATP) instance in the Oracle Cloud Console
2. Download the wallet file and connection string
3. Get your connection string from the Database Connection Strings section

**Option B: Self-managed PostgreSQL on OKE**
Deploy PostgreSQL using Helm:
```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
helm install postgresql bitnami/postgresql \
  --set auth.postgresPassword=your_secure_password \
  --set primary.persistence.enabled=false \
  --namespace todo-app \
  --create-namespace
```

4. Store the connection details in a Kubernetes secret:

```bash
kubectl create secret generic postgres-secret \
  --from-literal=database-url="postgresql://postgres:your_secure_password@<your-db-host>:5432/todo_db"
```

## Step 5: Prepare Application Images

### 5.1 Build and Push Images to OCIR (Oracle Cloud Infrastructure Registry)

```bash
# Tag and push images to OCIR
docker build -t <region-code>.ocir.io/<tenant-namespace>/todo-backend:v1.0.0 -f backend/Dockerfile .
docker build -t <region-code>.ocir.io/<tenant-namespace>/todo-frontend:v1.0.0 -f frontend/Dockerfile .
docker build -t <region-code>.ocir.io/<tenant-namespace>/reminder-service:v1.0.0 -f event-services/reminder-service/Dockerfile .
docker build -t <region-code>.ocir.io/<tenant-namespace>/recurring-task-service:v1.0.0 -f event-services/recurring-task-service/Dockerfile .
docker build -t <region-code>.ocir.io/<tenant-namespace>/audit-log-service:v1.0.0 -f event-services/audit-log-service/Dockerfile .
docker build -t <region-code>.ocir.io/<tenant-namespace>/notification-service:v1.0.0 -f event-services/notification-service/Dockerfile .

# Login to OCIR
docker login <region-code>.ocir.io

# Push images
docker push <region-code>.ocir.io/<tenant-namespace>/todo-backend:v1.0.0
docker push <region-code>.ocir.io/<tenant-namespace>/todo-frontend:v1.0.0
docker push <region-code>.ocir.io/<tenant-namespace>/reminder-service:v1.0.0
docker push <region-code>.ocir.io/<tenant-namespace>/recurring-task-service:v1.0.0
docker push <region-code>.ocir.io/<tenant-namespace>/audit-log-service:v1.0.0
docker push <region-code>.ocir.io/<tenant-namespace>/notification-service:v1.0.0
```

## Step 6: Update Helm Values for Oracle Cloud

Create a `values-oracle-cloud.yaml` file with Oracle Cloud specific configurations:

```yaml
# values-oracle-cloud.yaml
global:
  postgres:
    enabled: true
    databaseUrl: "postgresql://[user]:[password]@[host]:[port]/[database]"
  
  auth:
    enabled: true
    secret: "[your-super-secret-key-min-32-chars]"

# Backend configuration
backend:
  replicaCount: 2
  image:
    repository: "<region-code>.ocir.io/<tenant-namespace>/todo-backend"
    pullPolicy: Always
    tag: "v1.0.0"
  service:
    type: ClusterIP
    port: 80
  resources:
    limits:
      cpu: 500m
      memory: 512Mi
    requests:
      cpu: 250m
      memory: 256Mi
  env:
    DATABASE_URL: "postgresql://[user]:[password]@[host]:[port]/[database]"
    MCP_SERVER_URL: "http://mcp-server:8001"
    KAFKA_BROKER: "todo-kafka-kafka-brokers.kafka.svc.cluster.local:9092"
    DAPR_HTTP_ENDPOINT: "http://localhost:3500"
    DAPR_GRPC_ENDPOINT: "grpc://localhost:50001"
    BETTER_AUTH_SECRET: "[your-super-secret-key-min-32-chars]"
    JWT_ALGORITHM: "HS256"
    ENVIRONMENT: "production"

# Frontend configuration
frontend:
  replicaCount: 2
  image:
    repository: "<region-code>.ocir.io/<tenant-namespace>/todo-frontend"
    pullPolicy: Always
    tag: "v1.0.0"
  service:
    type: LoadBalancer
    port: 80
  resources:
    limits:
      cpu: 200m
      memory: 256Mi
    requests:
      cpu: 100m
      memory: 128Mi
  env:
    NEXT_PUBLIC_API_URL: "http://backend:80"
    NEXT_PUBLIC_MCP_SERVER_URL: "http://mcp-server:80"
    NEXT_PUBLIC_DAPR_HTTP_ENDPOINT: "http://localhost:3500"
    NEXT_PUBLIC_KAFKA_BROKER: "todo-kafka-kafka-brokers.kafka.svc.cluster.local:9092"
    BETTER_AUTH_SECRET: "[your-super-secret-key-min-32-chars]"

# MCP Server configuration
mcpServer:
  replicaCount: 1
  image:
    repository: "<region-code>.ocir.io/<tenant-namespace>/todo-backend"
    pullPolicy: Always
    tag: "v1.0.0"
  service:
    type: ClusterIP
    port: 80
  resources:
    limits:
      cpu: 300m
      memory: 256Mi
    requests:
      cpu: 150m
      memory: 128Mi
  env:
    DATABASE_URL: "postgresql://[user]:[password]@[host]:[port]/[database]"
    KAFKA_BROKER: "todo-kafka-kafka-brokers.kafka.svc.cluster.local:9092"
    DAPR_HTTP_ENDPOINT: "http://localhost:3500"
    DAPR_GRPC_ENDPOINT: "grpc://localhost:50001"
    BETTER_AUTH_SECRET: "[your-super-secret-key-min-32-chars]"
    JWT_ALGORITHM: "HS256"
    ENVIRONMENT: "production"

# Event services configurations
eventServices:
  reminderService:
    enabled: true
    replicaCount: 1
    image:
      repository: "<region-code>.ocir.io/<tenant-namespace>/reminder-service"
      pullPolicy: Always
      tag: "v1.0.0"
    service:
      type: ClusterIP
      port: 80
    resources:
      limits:
        cpu: 200m
        memory: 128Mi
      requests:
        cpu: 100m
        memory: 64Mi
    env:
      DATABASE_URL: "postgresql://[user]:[password]@[host]:[port]/[database]"
      KAFKA_BROKER: "todo-kafka-kafka-brokers.kafka.svc.cluster.local:9092"
      DAPR_HTTP_ENDPOINT: "http://localhost:3500"
      DAPR_GRPC_ENDPOINT: "grpc://localhost:50001"
      ENVIRONMENT: "production"

  recurringTaskService:
    enabled: true
    replicaCount: 1
    image:
      repository: "<region-code>.ocir.io/<tenant-namespace>/recurring-task-service"
      pullPolicy: Always
      tag: "v1.0.0"
    service:
      type: ClusterIP
      port: 80
    resources:
      limits:
        cpu: 200m
        memory: 128Mi
      requests:
        cpu: 100m
        memory: 64Mi
    env:
      DATABASE_URL: "postgresql://[user]:[password]@[host]:[port]/[database]"
      KAFKA_BROKER: "todo-kafka-kafka-brokers.kafka.svc.cluster.local:9092"
      DAPR_HTTP_ENDPOINT: "http://localhost:3500"
      DAPR_GRPC_ENDPOINT: "grpc://localhost:50001"
      ENVIRONMENT: "production"

  auditLogService:
    enabled: true
    replicaCount: 1
    image:
      repository: "<region-code>.ocir.io/<tenant-namespace>/audit-log-service"
      pullPolicy: Always
      tag: "v1.0.0"
    service:
      type: ClusterIP
      port: 80
    resources:
      limits:
        cpu: 200m
        memory: 128Mi
      requests:
        cpu: 100m
        memory: 64Mi
    env:
      DATABASE_URL: "postgresql://[user]:[password]@[host]:[port]/[database]"
      KAFKA_BROKER: "todo-kafka-kafka-brokers.kafka.svc.cluster.local:9092"
      DAPR_HTTP_ENDPOINT: "http://localhost:3500"
      DAPR_GRPC_ENDPOINT: "grpc://localhost:50001"
      ENVIRONMENT: "production"

  notificationService:
    enabled: true
    replicaCount: 1
    image:
      repository: "<region-code>.ocir.io/<tenant-namespace>/notification-service"
      pullPolicy: Always
      tag: "v1.0.0"
    service:
      type: ClusterIP
      port: 80
    resources:
      limits:
        cpu: 200m
        memory: 128Mi
      requests:
        cpu: 100m
        memory: 64Mi
    env:
      DATABASE_URL: "postgresql://[user]:[password]@[host]:[port]/[database]"
      KAFKA_BROKER: "todo-kafka-kafka-brokers.kafka.svc.cluster.local:9092"
      DAPR_HTTP_ENDPOINT: "http://localhost:3500"
      DAPR_GRPC_ENDPOINT: "grpc://localhost:50001"
      ENVIRONMENT: "production"

# Dapr component configurations
daprComponents:
  kafkaPubSub:
    enabled: true
    brokers: "todo-kafka-kafka-brokers.kafka.svc.cluster.local:9092"
    consumerGroup: "dapr-consumer-group"
    clientID: "dapr-kafka-client"
    authRequired: false

  postgresStateStore:
    enabled: true
    connectionString: "postgresql://[user]:[password]@[host]:[port]/[database]?sslmode=disable"
    actorStateStore: true

  cronBinding:
    enabled: true
    schedule: "@every 30s"

  kubernetesSecretStore:
    enabled: true
```

## Step 7: Deploy the Application

### 7.1 Create a namespace for the application

```bash
kubectl create namespace todo-app
kubectl config set-context --current --namespace=todo-app
```

### 7.2 Install the application using Helm

```bash
# Add the Dapr and Kafka repositories if not already added
helm repo add dapr https://dapr.github.io/helm-charts
helm repo add strimzi https://strimzi.io/charts/
helm repo update

# Install the application
helm install todo-app ./helm/todo-app \
  --namespace todo-app \
  --values values-oracle-cloud.yaml \
  --set backend.image.repository="<region-code>.ocir.io/<tenant-namespace>/todo-backend" \
  --set frontend.image.repository="<region-code>.ocir.io/<tenant-namespace>/todo-frontend" \
  --set eventServices.reminderService.image.repository="<region-code>.ocir.io/<tenant-namespace>/reminder-service" \
  --set eventServices.recurringTaskService.image.repository="<region-code>.ocir.io/<tenant-namespace>/recurring-task-service" \
  --set eventServices.auditLogService.image.repository="<region-code>.ocir.io/<tenant-namespace>/audit-log-service" \
  --set eventServices.notificationService.image.repository="<region-code>.ocir.io/<tenant-namespace>/notification-service"
```

## Step 8: Verify the Deployment

```bash
# Check if all pods are running
kubectl get pods -n todo-app

# Check services
kubectl get svc -n todo-app

# Check Dapr status
dapr status -k

# Check if Kafka is running (if using self-hosted)
kubectl get pods -n kafka
```

## Step 9: Configure Load Balancer and DNS

### 9.1 Get the LoadBalancer IP for the frontend

```bash
kubectl get svc frontend -n todo-app
```

### 9.2 Configure DNS (optional)

If you have a domain name, create a DNS record pointing to the LoadBalancer IP.

## Step 10: Set up Monitoring and Logging

### 10.1 Install monitoring stack (Prometheus and Grafana)

```bash
# Add Prometheus community Helm repository
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

# Install Prometheus and Grafana
helm install monitoring prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --create-namespace
```

### 10.2 Set up Dapr monitoring

```bash
# Port forward to access Grafana
kubectl port-forward -n monitoring svc/monitoring-grafana 3000:80

# Access Grafana at http://localhost:3000
# Default credentials: admin/admin
```

## Step 11: Set up Auto-Scaling

### 11.1 Configure Horizontal Pod Autoscaler (HPA)

```bash
# Create HPA for backend
kubectl autoscale deployment backend \
  --cpu-percent=70 \
  --min=2 \
  --max=10 \
  --namespace todo-app

# Create HPA for frontend
kubectl autoscale deployment frontend \
  --cpu-percent=70 \
  --min=2 \
  --max=5 \
  --namespace todo-app
```

## Step 12: Set up CI/CD Pipeline

Create a GitHub Actions workflow for automated deployments:

```yaml
# .github/workflows/deploy-oracle-oke.yaml
name: Deploy to Oracle OKE

on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]

env:
  ORACLE_REGION: us-ashburn-1
  TENANT_NAMESPACE: your-tenant-namespace
  COMPARTMENT_OCID: your-compartment-ocid
  REGION_CODE: iad

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v4

    - name: Setup OCI CLI
      uses: oracle-actions/setup-oci-cli@v1
      with:
        tenancy-id: ${{ secrets.OCI_TENANCY }}
        user-id: ${{ secrets.OCI_USER }}
        region: ${{ env.ORACLE_REGION }}
        private-key: ${{ secrets.OCI_PRIVATE_KEY }}

    - name: Configure kubectl for OKE
      run: |
        oci ce cluster create-kubeconfig --cluster-id ${{ secrets.OKE_CLUSTER_ID }} --file $HOME/.kube/config --region ${{ env.ORACLE_REGION }}

    - name: Build and push Docker images
      run: |
        # Login to OCIR
        echo ${{ secrets.OCI_AUTH_TOKEN }} | docker login ${REGION_CODE}.ocir.io -u '${{ secrets.OCI_TENANCY }}/oracleidentitycloudservice/${{ secrets.OCI_USER }}'

        # Build and push images
        docker build -t ${REGION_CODE}.ocir.io/${TENANT_NAMESPACE}/todo-backend:${{ github.sha }} -f backend/Dockerfile .
        docker push ${REGION_CODE}.ocir.io/${TENANT_NAMESPACE}/todo-backend:${{ github.sha }}

        docker build -t ${REGION_CODE}.ocir.io/${TENANT_NAMESPACE}/todo-frontend:${{ github.sha }} -f frontend/Dockerfile .
        docker push ${REGION_CODE}.ocir.io/${TENANT_NAMESPACE}/todo-frontend:${{ github.sha }}

        docker build -t ${REGION_CODE}.ocir.io/${TENANT_NAMESPACE}/reminder-service:${{ github.sha }} -f event-services/reminder-service/Dockerfile .
        docker push ${REGION_CODE}.ocir.io/${TENANT_NAMESPACE}/reminder-service:${{ github.sha }}

        docker build -t ${REGION_CODE}.ocir.io/${TENANT_NAMESPACE}/recurring-task-service:${{ github.sha }} -f event-services/recurring-task-service/Dockerfile .
        docker push ${REGION_CODE}.ocir.io/${TENANT_NAMESPACE}/recurring-task-service:${{ github.sha }}

        docker build -t ${REGION_CODE}.ocir.io/${TENANT_NAMESPACE}/audit-log-service:${{ github.sha }} -f event-services/audit-log-service/Dockerfile .
        docker push ${REGION_CODE}.ocir.io/${TENANT_NAMESPACE}/audit-log-service:${{ github.sha }}

        docker build -t ${REGION_CODE}.ocir.io/${TENANT_NAMESPACE}/notification-service:${{ github.sha }} -f event-services/notification-service/Dockerfile .
        docker push ${REGION_CODE}.ocir.io/${TENANT_NAMESPACE}/notification-service:${{ github.sha }}

    - name: Update Helm release
      run: |
        helm upgrade --install todo-app ./helm/todo-app \
          --namespace todo-app \
          --create-namespace \
          --values values-oracle-cloud.yaml \
          --set backend.image.tag=${{ github.sha }} \
          --set frontend.image.tag=${{ github.sha }} \
          --set eventServices.reminderService.image.tag=${{ github.sha }} \
          --set eventServices.recurringTaskService.image.tag=${{ github.sha }} \
          --set eventServices.auditLogService.image.tag=${{ github.sha }} \
          --set eventServices.notificationService.image.tag=${{ github.sha }}