# Todo Chatbot Application - Deployment and User Guide

## Table of Contents
1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Prerequisites](#prerequisites)
4. [Deployment](#deployment)
5. [Configuration](#configuration)
6. [User Guide](#user-guide)
7. [Troubleshooting](#troubleshooting)
8. [Scaling and Monitoring](#scaling-and-monitoring)

## Overview

The Todo Chatbot is an advanced task management application featuring recurring tasks, due dates, reminders, priorities, tags, and event-driven architecture. Built with Python (FastAPI) for the backend, TypeScript (Next.js) for the frontend, and event-driven services using Kafka and Dapr, the application is designed for deployment on Oracle Kubernetes Engine (OKE) with horizontal pod autoscaling and comprehensive monitoring.

### Key Features
- **Advanced Task Management**: Create, update, and manage tasks with due dates, priorities, and tags
- **Recurring Tasks**: Set up tasks that automatically repeat on daily, weekly, monthly, or yearly schedules
- **Smart Reminders**: Receive timely notifications for upcoming deadlines
- **Event-Driven Architecture**: Scalable system using Kafka for messaging and Dapr for distributed runtime
- **Auto-Scaling**: Automatically adjusts resources based on demand
- **Comprehensive Monitoring**: Prometheus and Grafana for metrics and visualization

## Architecture

The application follows a microservices architecture with the following components:

### Core Services
- **Backend API**: FastAPI application handling business logic and data persistence
- **Frontend UI**: Next.js application providing the user interface
- **Event Services**:
  - Reminder Service: Processes and sends task reminders
  - Recurring Task Service: Manages recurring task generation
  - Audit Log Service: Maintains system audit trails
  - Notification Service: Handles user notifications

### Infrastructure Components
- **Kafka**: Message broker for event-driven communication
- **Dapr**: Distributed application runtime providing pub/sub, state management, and service invocation
- **PostgreSQL**: Persistent storage for tasks and user data
- **Redis**: Caching layer (if implemented)

### Deployment Architecture
- **Oracle Kubernetes Engine (OKE)**: Managed Kubernetes service
- **Helm Charts**: For consistent and reproducible deployments
- **Horizontal Pod Autoscaler (HPA)**: Automatic scaling based on CPU/memory metrics
- **Prometheus & Grafana**: Monitoring and visualization stack

## Prerequisites

Before deploying the application, ensure you have:

### Local Development
- Docker and Docker Compose
- Python 3.11+
- Node.js 18+
- Helm 3.x
- Kubernetes CLI (kubectl)

### Oracle Cloud Infrastructure (OCI)
- OCI account with appropriate permissions
- OKE cluster provisioned
- OCI CLI configured with access credentials
- Docker registry (OCIR) configured

### Required Tools
- Helm (v3.12+)
- kubectl (v1.28+)
- Git

## Deployment

### 1. Clone the Repository

```bash
git clone <repository-url>
cd todo-app
```

### 2. Configure OCI and Kubernetes Access

```bash
# Configure OCI CLI
oci setup config

# Get OKE cluster kubeconfig
oci ce cluster create-kubeconfig --cluster-id <cluster-id> --file $HOME/.kube/config --region <region>
```

### 3. Build and Push Docker Images

```bash
# Login to OCIR
docker login <region-code>.ocir.io -u '<tenancy-namespace>/<username>' -p '<auth-token>'

# Build and tag images
docker build -t <region-code>.ocir.io/<tenancy-namespace>/todo-backend:<tag> ./backend
docker build -t <region-code>.ocir.io/<tenancy-namespace>/todo-frontend:<tag> ./frontend
docker build -t <region-code>.ocir.io/<tenancy-namespace>/reminder-service:<tag> ./event-services/reminder-service
docker build -t <region-code>.ocir.io/<tenancy-namespace>/recurring-task-service:<tag> ./event-services/recurring-task-service
docker build -t <region-code>.ocir.io/<tenancy-namespace>/audit-log-service:<tag> ./event-services/audit-log-service
docker build -t <region-code>.ocir.io/<tenancy-namespace>/notification-service:<tag> ./event-services/notification-service

# Push images
docker push <region-code>.ocir.io/<tenancy-namespace>/todo-backend:<tag>
docker push <region-code>.ocir.io/<tenancy-namespace>/todo-frontend:<tag>
docker push <region-code>.ocir.io/<tenancy-namespace>/reminder-service:<tag>
docker push <region-code>.ocir.io/<tenancy-namespace>/recurring-task-service:<tag>
docker push <region-code>.ocir.io/<tenancy-namespace>/audit-log-service:<tag>
docker push <region-code>.ocir.io/<tenancy-namespace>/notification-service:<tag>
```

### 4. Deploy Infrastructure Components

#### Deploy Dapr

```bash
# Add Dapr Helm repo
helm repo add dapr https://dapr.github.io/helm-charts/
helm repo update

# Install Dapr
helm upgrade --install dapr dapr/dapr --namespace dapr-system --create-namespace --wait
```

#### Deploy Kafka (using Strimzi)

```bash
# Deploy Strimzi operator
kubectl create -f https://strimzi.io/install/latest?namespace=kafka
kubectl create namespace kafka
kubectl apply -f https://strimzi.io/examples/latest/kafka/kafka-ephemeral-single.yaml -n kafka
```

#### Deploy PostgreSQL

```bash
# Deploy PostgreSQL using your preferred method
# Example with Bitnami chart:
helm upgrade --install postgresql oci://registry-1.docker.io/bitnamicharts/postgresql --namespace postgresql --create-namespace --set auth.password=<password>
```

### 5. Configure Helm Values

Update the `helm/todo-app/values.yaml` file with your specific configurations:

```yaml
# Image tags - update with your pushed image tags
backend:
  image:
    repository: <region-code>.ocir.io/<tenancy-namespace>/todo-backend
    tag: <tag>

frontend:
  image:
    repository: <region-code>.ocir.io/<tenancy-namespace>/todo-frontend
    tag: <tag>

eventServices:
  reminder:
    image:
      repository: <region-code>.ocir.io/<tenancy-namespace>/reminder-service
      tag: <tag>
  recurringTask:
    image:
      repository: <region-code>.ocir.io/<tenancy-namespace>/recurring-task-service
      tag: <tag>
  auditLog:
    image:
      repository: <region-code>.ocir.io/<tenancy-namespace>/audit-log-service
      tag: <tag>
  notification:
    image:
      repository: <region-code>.ocir.io/<tenancy-namespace>/notification-service
      tag: <tag>

# Kafka configuration
kafka:
  broker: "kafka-kafka-brokers.kafka.svc.cluster.local:9092"

# PostgreSQL configuration
backend:
  config:
    databaseHost: "postgresql-postgresql.postgresql.svc.cluster.local"
    databasePort: "5432"
    databaseName: "tododb"
    databaseUser: "postgres"
```

### 6. Deploy the Application

```bash
# Deploy the application using Helm
helm upgrade --install todo-app ./helm/todo-app --namespace todo-app --create-namespace --wait --values helm/todo-app/values.yaml
```

### 7. Deploy Monitoring Stack

```bash
# Deploy Prometheus and Grafana
kubectl apply -f k8s/monitoring/
```

## Configuration

### Environment Variables

The application uses several environment variables for configuration:

#### Backend Service
- `DATABASE_URL`: Connection string for PostgreSQL database
- `DAPR_HTTP_ENDPOINT`: Dapr sidecar endpoint (usually `http://localhost:3500`)
- `KAFKA_BROKER`: Kafka broker address
- `ENVIRONMENT`: Current environment (development, staging, production)

#### Event Services
- `DAPR_HTTP_ENDPOINT`: Dapr sidecar endpoint
- `KAFKA_BROKER`: Kafka broker address
- `KAFKA_CONSUMER_GROUP`: Unique consumer group for the service

### Helm Configuration

The Helm chart allows configuration of:

- **Replica Counts**: For scaling different services
- **Resource Limits**: CPU and memory allocation
- **Autoscaling**: HPA configuration for automatic scaling
- **Service Types**: LoadBalancer, ClusterIP, or NodePort
- **Image Versions**: Container image tags

## User Guide

### Getting Started

1. **Access the Application**
   - After deployment, get the frontend service external IP:
     ```bash
     kubectl get svc todo-frontend -n todo-app
     ```
   - Access the application through the external IP or load balancer address

2. **Create an Account**
   - Navigate to the signup page
   - Enter your email and create a password
   - Verify your email if required

### Task Management

#### Creating Tasks
1. Click the "Create New Task" button
2. Enter the task title and description
3. Set due date if applicable
4. Choose priority level (low, medium, high)
5. Add tags for organization (comma-separated)
6. Save the task

#### Managing Existing Tasks
- **Edit**: Click on a task to modify its details
- **Complete**: Check the checkbox to mark as completed
- **Delete**: Use the delete option to remove tasks

#### Recurring Tasks
1. Navigate to the "Recurring Tasks" section
2. Click "Create Recurring Task"
3. Enter the task details
4. Select the frequency (daily, weekly, monthly, yearly)
5. Set the interval (every N days/weeks/months)
6. Optionally set an end date
7. Save the recurring pattern

### Reminders and Notifications

#### Setting Up Reminders
1. Open an existing task
2. Click on "Add Reminder"
3. Select the date and time for the reminder
4. Choose the notification channel (email, push, SMS)
5. Save the reminder

#### Reminder Settings
- Access reminder settings from the profile menu
- Configure default reminder times
- Set preferred notification channels
- Manage notification preferences

### Advanced Features

#### Task Organization
- **Tags**: Use tags to categorize tasks (e.g., work, personal, urgent)
- **Priorities**: Assign priority levels to tasks
- **Search**: Use the search bar to find tasks by title, description, or tags
- **Filter**: Filter tasks by priority, completion status, or due date

#### Dashboard
- **Statistics**: View completion rates and task distribution
- **Upcoming Reminders**: See soon-to-be-triggered reminders
- **Recurring Tasks**: Monitor active recurring patterns
- **Tag Distribution**: Visualize task categories

### Profile and Settings

#### User Preferences
- Update your profile information
- Change password
- Configure notification preferences
- Set timezone and date format preferences

## Troubleshooting

### Common Issues

#### Application Not Starting
1. Check pod status:
   ```bash
   kubectl get pods -n todo-app
   ```
2. Check logs for specific pods:
   ```bash
   kubectl logs <pod-name> -n todo-app
   ```
3. Verify service dependencies (Kafka, PostgreSQL, Dapr)

#### Kafka Connection Issues
1. Verify Kafka is running:
   ```bash
   kubectl get pods -n kafka
   ```
2. Check Kafka logs:
   ```bash
   kubectl logs -l strimzi.io/name=kafka-cluster -n kafka
   ```
3. Verify network connectivity between services

#### Dapr Sidecar Issues
1. Check Dapr system status:
   ```bash
   kubectl get pods -n dapr-system
   ```
2. Verify Dapr components:
   ```bash
   kubectl get components -A
   ```
3. Check Dapr logs:
   ```bash
   kubectl logs -l app=dapr-placement-server -n dapr-system
   ```

#### Scaling Problems
1. Check HPA status:
   ```bash
   kubectl get hpa -n todo-app
   kubectl describe hpa <hpa-name> -n todo-app
   ```
2. Verify resource metrics:
   ```bash
   kubectl top nodes
   kubectl top pods -n todo-app
   ```

### Monitoring and Logging

#### Accessing Metrics
- **Prometheus**: Available at `http://<prometheus-ip>:9090`
- **Grafana**: Available at `http://<grafana-ip>:3000`

#### Useful Queries
- Application request rate: `rate(http_requests_total[5m])`
- Average response time: `rate(http_request_duration_seconds_sum[5m]) / rate(http_request_duration_seconds_count[5m])`
- Pod resource usage: `container_cpu_usage_seconds_total` and `container_memory_usage_bytes`

### Health Checks

The application provides health check endpoints:
- Backend: `GET /health` and `GET /ready`
- Individual services have their own health endpoints

## Scaling and Monitoring

### Horizontal Pod Autoscaling (HPA)

The application is configured with HPA for automatic scaling:

- **Backend Service**: Scales based on CPU utilization (target: 80%)
- **Frontend Service**: Scales based on CPU utilization (target: 80%)
- **Event Services**: Scale based on CPU and custom metrics

To view HPA status:
```bash
kubectl get hpa -n todo-app
```

### Monitoring Stack

#### Prometheus
- Collects metrics from all services
- Pre-configured service discovery for application components
- Stores metrics for analysis and alerting

#### Grafana
- Pre-built dashboards for application metrics
- System resource monitoring
- Custom dashboard creation capability

#### Alerts
- Configure alerts in Prometheus Alertmanager
- Common alerts include:
  - High error rates
  - Slow response times
  - Service unavailability
  - Resource exhaustion

### Performance Tuning

#### Resource Optimization
- Monitor resource usage with `kubectl top`
- Adjust resource requests and limits in Helm values
- Fine-tune HPA parameters based on usage patterns

#### Database Performance
- Monitor database connection pools
- Optimize queries based on slow query logs
- Consider read replicas for heavy read loads

## Support

For support, please contact:
- **Documentation**: Refer to the project documentation
- **Issues**: Submit issues through the GitHub repository
- **Community**: Join our community forums or Slack channel

---

*This documentation was last updated on February 8, 2026 for the Todo Chatbot application.*