# Quickstart Guide: Phase V - Advanced Cloud Deployment of Todo Chatbot

## Overview
This guide provides a step-by-step approach to getting the Phase V Todo Chatbot with event-driven architecture running locally using Minikube. This includes setting up Kafka, Dapr, and the specialized event-driven services.

## Prerequisites

### System Requirements
- Docker Desktop with Kubernetes enabled OR Minikube
- kubectl (v1.28+)
- Helm (v3+)
- Dapr CLI
- Python 3.13+
- Node.js 18+

### Installation
```bash
# Install Dapr CLI
wget -q https://raw.githubusercontent.com/dapr/cli/master/install/install.sh -O - | /bin/bash

# Install kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x kubectl
sudo mv kubectl /usr/local/bin/

# Install Helm
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
```

## Local Setup with Minikube

### 1. Start Minikube and Install Dapr
```bash
# Start Minikube with sufficient resources
minikube start --cpus=4 --memory=8192 --disk-size=40g

# Install Dapr in the cluster
dapr init -k

# Verify Dapr installation
dapr status -k
```

### 2. Clone and Navigate to the Repository
```bash
git clone <repository-url>
cd todo-app

# Switch to the Phase V branch
git checkout 005-advanced-cloud-deployment
```

### 3. Deploy Kafka Cluster
```bash
# Create a namespace for Kafka
kubectl create namespace kafka

# Deploy Strimzi Kafka operator
kubectl create -f 'https://strimzi.io/install/latest?namespace=kafka' -n kafka

# Wait for the operator to be ready
kubectl wait --for=condition=ready pod -l name=strimzi-cluster-operator -n kafka --timeout=300s

# Deploy a Kafka cluster
cat <<EOF | kubectl apply -f -
apiVersion: kafka.strimzi.io/v1beta2
kind: Kafka
metadata:
  name: my-cluster
  namespace: kafka
spec:
  kafka:
    version: 3.6.0
    replicas: 1
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
      offsets.topic.replication.factor: 1
      transaction.state.log.replication.factor: 1
      transaction.state.log.min.isr: 1
      default.replication.factor: 1
      min.insync.replicas: 1
      inter.broker.protocol.version: "3.6"
    storage:
      type: jbod
      volumes:
      - id: 0
        type: persistent-claim
        size: 10Gi
        deleteClaim: false
  zookeeper:
    replicas: 1
    storage:
      type: persistent-claim
      size: 5Gi
      deleteClaim: false
  entityOperator:
    topicOperator: {}
    userOperator: {}
EOF

# Verify Kafka cluster is ready
kubectl wait --for=condition=Ready kafka/my-cluster -n kafka --timeout=300s
```

### 4. Configure Dapr Components
```bash
# Create Dapr components for Kafka pub/sub
cat <<EOF | kubectl apply -f -
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: kafka-pubsub
  namespace: default
spec:
  type: pubsub.kafka
  version: v1
  metadata:
  - name: brokers
    value: "my-cluster-kafka-bootstrap.kafka.svc.cluster.local:9092"
  - name: authRequired
    value: "false"
  - name: consumerGroup
    value: "dapr-consumer-group"
  - name: clientID
    value: "dapr-kafka-client"
  - name: maxMessageBytes
    value: "1048576"
  - name: consumeRetryInterval
    value: "200ms"
EOF

# Create Dapr state component for PostgreSQL
cat <<EOF | kubectl apply -f -
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: postgresql-state
  namespace: default
spec:
  type: state.postgresql
  version: v1
  metadata:
  - name: connectionString
    value: "host=neon-postgres.default.svc.cluster.local user=postgres password=yourpassword dbname=todoapp port=5432 sslmode=disable"
  - name: versionColumnType
    value: "dapr_version"
  - name: valueColumnName
    value: "dapr_value"
  - name: keyColumnName
    value: "dapr_key"
  - name: tableName
    value: "dapr_store"
EOF
```

### 5. Deploy PostgreSQL Database
```bash
# Deploy Neon PostgreSQL (or standard PostgreSQL for local dev)
kubectl apply -f - <<EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: neon-postgres
  namespace: default
spec:
  replicas: 1
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
      - name: postgres
        image: postgres:15
        ports:
        - containerPort: 5432
        env:
        - name: POSTGRES_DB
          value: "todoapp"
        - name: POSTGRES_USER
          value: "postgres"
        - name: POSTGRES_PASSWORD
          value: "yourpassword"
        volumeMounts:
        - name: postgres-storage
          mountPath: /var/lib/postgresql/data
      volumes:
      - name: postgres-storage
        emptyDir: {}
---
apiVersion: v1
kind: Service
metadata:
  name: neon-postgres
  namespace: default
spec:
  selector:
    app: postgres
  ports:
    - protocol: TCP
      port: 5432
      targetPort: 5432
EOF
```

### 6. Deploy the Application with Helm
```bash
# Add the required repositories
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update

# Create a values file for local development
cat > local-values.yaml <<EOF
global:
  daprEnabled: true
  kafkaEndpoint: "my-cluster-kafka-bootstrap.kafka.svc.cluster.local:9092"

backend:
  replicaCount: 1
  image:
    repository: todo-backend
    tag: latest
  service:
    type: ClusterIP
    port: 8000
  resources:
    limits:
      cpu: 500m
      memory: 512Mi
    requests:
      cpu: 100m
      memory: 128Mi
  daprEnabled: true
  daprAppPort: 8000
  daprAppProtocol: http

frontend:
  replicaCount: 1
  image:
    repository: todo-frontend
    tag: latest
  service:
    type: LoadBalancer
    port: 3000
  resources:
    limits:
      cpu: 200m
      memory: 256Mi
    requests:
      cpu: 50m
      memory: 64Mi
  daprEnabled: true
  daprAppPort: 3000
  daprAppProtocol: http

eventServices:
  reminderService:
    enabled: true
    replicaCount: 1
  recurringTaskService:
    enabled: true
    replicaCount: 1
  auditLogService:
    enabled: true
    replicaCount: 1
  notificationService:
    enabled: true
    replicaCount: 1

database:
  enabled: false  # We're using our own PostgreSQL deployment
EOF

# Install the application using Helm
helm install todo-app ./helm/todo-app -f local-values.yaml
```

### 7. Build and Deploy Container Images
```bash
# Build backend image
cd backend
docker build -t todo-backend:latest .
minikube image load todo-backend:latest

# Build frontend image
cd ../frontend
docker build -t todo-frontend:latest .
minikube image load todo-frontend:latest

# Restart deployments to pick up the new images
kubectl rollout restart deployment/todo-app-backend
kubectl rollout restart deployment/todo-app-frontend
```

### 8. Deploy Event-Driven Services
```bash
# Create deployments for event-driven services
kubectl apply -f - <<EOF
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: reminder-service
  labels:
    app: reminder-service
spec:
  replicas: 1
  selector:
    matchLabels:
      app: reminder-service
  template:
    metadata:
      labels:
        app: reminder-service
      annotations:
        dapr.io/enabled: "true"
        dapr.io/app-id: "reminder-service"
        dapr.io/app-port: "8001"
        dapr.io/config: "dapr-config"
    spec:
      containers:
      - name: reminder-service
        image: reminder-service:latest
        ports:
        - containerPort: 8001
        env:
        - name: KAFKA_BROKER
          value: "my-cluster-kafka-bootstrap.kafka.svc.cluster.local:9092"
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: url
        resources:
          limits:
            cpu: 300m
            memory: 256Mi
          requests:
            cpu: 50m
            memory: 64Mi

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: recurring-task-service
  labels:
    app: recurring-task-service
spec:
  replicas: 1
  selector:
    matchLabels:
      app: recurring-task-service
  template:
    metadata:
      labels:
        app: recurring-task-service
      annotations:
        dapr.io/enabled: "true"
        dapr.io/app-id: "recurring-task-service"
        dapr.io/app-port: "8002"
        dapr.io/config: "dapr-config"
    spec:
      containers:
      - name: recurring-task-service
        image: recurring-task-service:latest
        ports:
        - containerPort: 8002
        env:
        - name: KAFKA_BROKER
          value: "my-cluster-kafka-bootstrap.kafka.svc.cluster.local:9092"
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: url
        resources:
          limits:
            cpu: 300m
            memory: 256Mi
          requests:
            cpu: 50m
            memory: 64Mi
EOF
```

### 9. Verify the Deployment
```bash
# Check if all pods are running
kubectl get pods

# Check Dapr sidecars are injected
dapr status -k

# Check Kafka connection
kubectl -n kafka get pods

# Port forward to access the frontend
kubectl port-forward svc/todo-app-frontend 3000:80
```

## Accessing the Application

### Frontend
The frontend will be accessible at `http://localhost:3000` after running:
```bash
kubectl port-forward svc/todo-app-frontend 3000:80
```

### Dapr Dashboard
Monitor Dapr components and services:
```bash
dapr dashboard -k
```

### Kafka Topics
View Kafka topics to verify event processing:
```bash
kubectl -n kafka exec -it my-cluster-kafka-0 -- bin/kafka-topics.sh --bootstrap-server localhost:9092 --list
```

## Testing Advanced Features

### Creating a Recurring Task
1. Navigate to the frontend UI
2. Click on "Advanced Features" → "Recurring Tasks"
3. Create a recurring task with daily frequency
4. Verify in the database that recurring pattern is saved
5. Check that Kafka receives `recurring-task.created` events

### Setting Up a Reminder
1. Create a task with a due date
2. Set up a reminder 1 hour before the due date
3. Monitor the reminder service logs for processing
4. Verify that reminder events are published to Kafka

### Event Stream Monitoring
Monitor the event stream:
```bash
kubectl -n kafka exec -it my-cluster-kafka-0 -- bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic task-events --from-beginning
```

## Troubleshooting

### Common Issues
1. **Pods not starting**: Check resource availability in Minikube
2. **Dapr sidecar not injected**: Verify Dapr is properly installed
3. **Kafka connection issues**: Check Kafka bootstrap server address
4. **Database connection errors**: Verify PostgreSQL is running and accessible

### Useful Commands
```bash
# Check Dapr sidecar logs
kubectl logs <pod-name> daprd

# Check application logs
kubectl logs <pod-name>

# Describe a pod for detailed information
kubectl describe pod <pod-name>

# Check service endpoints
kubectl get endpoints

# Execute into a pod for debugging
kubectl exec -it <pod-name> -- /bin/sh
```

## Cleanup
To remove all resources:
```bash
helm uninstall todo-app
kubectl delete -f kafka-deployment.yaml
kubectl delete -f dapr-components.yaml
dapr uninstall -k
minikube delete
```