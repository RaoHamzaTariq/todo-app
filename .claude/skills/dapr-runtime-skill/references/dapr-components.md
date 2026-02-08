# Dapr Components Reference

## Overview
This document provides detailed configuration examples for various Dapr components used in the Todo Chatbot application. Each component follows the Dapr component specification and is designed to work across both Minikube and Oracle OKE environments.

## Component Configuration Templates

### 1. Kafka Pub/Sub Component

#### Basic Kafka Configuration
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: kafka-pubsub
spec:
  type: pubsub.kafka
  version: v1
  metadata:
  - name: brokers
    value: "kafka:9092"  # Adjust for environment
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
  - name: disableTls
    value: "true"
  - name: version
    value: "1.0.0"
```

#### Secure Kafka Configuration (for production)
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: kafka-pubsub-secure
spec:
  type: pubsub.kafka
  version: v1
  metadata:
  - name: brokers
    value: "kafka.oracle-oke.internal:9093"  # Secure port
  - name: authRequired
    value: "true"
  - name: saslUsername
    secretKeyRef:
      name: kafka-credentials
      key: username
  - name: saslPassword
    secretKeyRef:
      name: kafka-credentials
      key: password
  - name: saslMechanism
    value: "PLAIN"
  - name: consumerGroup
    value: "dapr-consumer-group"
  - name: clientID
    value: "dapr-kafka-client"
  - name: maxMessageBytes
    value: "1048576"
  - name: consumeRetryInterval
    value: "200ms"
  - name: disableTls
    value: "false"
  - name: caCert
    secretKeyRef:
      name: kafka-certificates
      key: ca.crt
  - name: clientCert
    secretKeyRef:
      name: kafka-certificates
      key: client.crt
  - name: clientKey
    secretKeyRef:
      name: kafka-certificates
      key: client.key
```

### 2. Redis State Store Component

#### Basic Redis Configuration
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: statestore
spec:
  type: state.redis
  version: v1
  metadata:
  - name: redisHost
    value: "redis-master:6379"
  - name: redisPassword
    secretKeyRef:
      name: redis-password
      key: redis-password
  - name: actorStateStore
    value: "true"
  - name: concurrency
    value: "first-write"
  - name: ttlInSeconds
    value: "0"  # 0 means no expiration
```

#### Redis Cluster Configuration (for production)
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: statestore-cluster
spec:
  type: state.redis
  version: v1
  metadata:
  - name: redisHost
    value: "redis-cluster.oracle-oke.svc.cluster.local:6379"
  - name: redisPassword
    secretKeyRef:
      name: redis-cluster-credentials
      key: password
  - name: enableCluster
    value: "true"
  - name: actorStateStore
    value: "true"
  - name: concurrency
    value: "first-write"
  - name: maxRetries
    value: "3"
  - name: maxRetryBackoff
    value: "4s"
  - name: dialTimeout
    value: "5s"
  - name: readTimeout
    value: "3s"
  - name: writeTimeout
    value: "3s"
  - name: poolSize
    value: "16"
```

### 3. Kubernetes Secrets Component

#### Basic Kubernetes Secrets Configuration
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: kubernetes-secrets-store
spec:
  type: secretstores.kubernetes
  version: v1
  metadata: []
```

#### With Specific Permissions
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: restricted-kubernetes-secrets
spec:
  type: secretstores.kubernetes
  version: v1
  metadata:
  - name: namespace
    value: "todo-app"
  - name: allowedSecrets
    value: "db-password,jwt-secret,api-keys"
```

### 4. Service Discovery Configuration

#### Dapr Configuration for Service Discovery
```yaml
apiVersion: dapr.io/v1alpha1
kind: Configuration
metadata:
  name: dapr-config
spec:
  tracing:
    samplingRate: "1"
    zipkin:
      endpointAddress: "http://zipkin.default.svc.cluster.local:9411/api/v2/spans"
  metric:
    enabled: true
  httpPipeline:
    handlers: []
  grpcPipeline:
    handlers: []
  accessControl:
    defaultAction: allow
    trustDomain: "pubsub-example-1"
    policies:
    - appId: "todo-frontend"
      defaultAction: allow
      trustDomain: "pubsub-example-1"
      namespace: "default"
      rules:
      - name: frontend-to-backend
        verb: "POST,PUT,GET,DELETE"
        protocol: "http"
        port: "8000"
        action: "allow"
```

## Dapr Sidecar Injection Examples

### Deployment with Dapr Annotations
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: todo-backend
  labels:
    app: todo-backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: todo-backend
  template:
    metadata:
      labels:
        app: todo-backend
      annotations:
        dapr.io/enabled: "true"
        dapr.io/app-id: "todo-backend"
        dapr.io/app-port: "8000"
        dapr.io/config: "dapr-config"
        dapr.io/log-level: "info"
        dapr.io/sidecar-cpu-limit: "0.5"
        dapr.io/sidecar-cpu-request: "0.2"
        dapr.io/sidecar-memory-limit: "512Mi"
        dapr.io/sidecar-memory-request: "256Mi"
        dapr.io/enable-api-logging: "true"
    spec:
      containers:
      - name: backend
        image: todo-backend:v1.0.0
        ports:
        - containerPort: 8000
        env:
        - name: DAPR_HOST
          value: "localhost"
        - name: DAPR_HTTP_PORT
          value: "3500"
        - name: DAPR_GRPC_PORT
          value: "50001"
```

### Service Definition
```yaml
apiVersion: v1
kind: Service
metadata:
  name: todo-backend
  labels:
    app: todo-backend
spec:
  type: ClusterIP
  selector:
    app: todo-backend
  ports:
  - name: http
    port: 8000
    targetPort: 8000
  - name: dapr-http
    port: 3500
    targetPort: 3500
  - name: dapr-grpc
    port: 50001
    targetPort: 50001
```

## Dapr API Usage Examples

### Publishing to a Topic
```python
import dapr.clients
from dapr.clients import DaprClient
import json

def publish_todo_event(todo_id, user_id, event_type, data):
    with DaprClient() as client:
        # Publish an event to the todo-events topic
        client.publish_event(
            pubsub_name='kafka-pubsub',
            topic_name='todo-events',
            data=json.dumps({
                "todo_id": todo_id,
                "user_id": user_id,
                "event_type": event_type,
                "timestamp": "2023-01-01T00:00:00Z",
                "data": data
            }),
            metadata={
                "partitionKey": user_id
            }
        )
        print(f'Published event: {event_type}')
```

### Invoking Another Service
```python
from dapr.clients import DaprClient

def call_backend_service(method, data):
    with DaprClient() as client:
        # Invoke the todo-backend service
        response = client.invoke_method(
            app_id='todo-backend',
            method_name=method,
            data=data,
            content_type='application/json'
        )

        return response.text()
```

### Saving State
```python
from dapr.clients import DaprClient

def save_conversation_state(conversation_id, state_data):
    with DaprClient() as client:
        # Save state with the conversation ID as the key
        client.save_state(
            store_name='statestore',
            key=f'conversation-{conversation_id}',
            value=json.dumps(state_data)
        )
        print(f'Saved state for conversation: {conversation_id}')
```

### Getting State
```python
from dapr.clients import DaprClient
import json

def get_conversation_state(conversation_id):
    with DaprClient() as client:
        # Get state using the conversation ID as the key
        response = client.get_state(
            store_name='statestore',
            key=f'conversation-{conversation_id}'
        )

        if response.data:
            return json.loads(response.data)
        else:
            return None
```

### Getting Secrets
```python
from dapr.clients import DaprClient

def get_secret(secret_store_name, secret_name):
    with DaprClient() as client:
        # Get the secret from the secret store
        response = client.get_secret(
            store_name=secret_store_name,
            key=secret_name
        )

        return response.data
```

## Environment-Specific Configurations

### Minikube Configuration
```yaml
# For local Minikube development
dapr:
  enabled: true
  appId: "todo-frontend-local"
  appPort: 3000
  config: "dapr-config-local"
  resources:
    cpu:
      limit: "0.2"
      request: "0.1"
    memory:
      limit: "256Mi"
      request: "128Mi"
  components:
    kafka:
      brokers: "kafka-minikube:9092"
    redis:
      host: "redis-minikube:6379"
```

### Oracle OKE Configuration
```yaml
# For Oracle OKE production
dapr:
  enabled: true
  appId: "todo-frontend-prod"
  appPort: 3000
  config: "dapr-config-prod"
  resources:
    cpu:
      limit: "0.5"
      request: "0.25"
    memory:
      limit: "512Mi"
      request: "256Mi"
  components:
    kafka:
      brokers: "kafka.oracle-oke.internal:9093"
    redis:
      host: "redis.oracle-oke.internal:6379"
```

## Validation and Testing

### Component Validation Script
```bash
#!/bin/bash
# validate_dapr_components.sh

# Check if Dapr is running
echo "Checking Dapr status..."
dapr status -k

# List all Dapr components
echo "Listing Dapr components..."
dapr components -k

# Test pubsub functionality
echo "Testing pubsub component..."
dapr publish --pubsub kafka-pubsub --topic test-topic --data '{"message":"test"}'

# Check if our specific components exist
COMPONENTS=("kafka-pubsub" "statestore" "kubernetes-secrets-store")
for component in "${COMPONENTS[@]}"; do
    if kubectl get component.dapr.io $component -o name 2>/dev/null; then
        echo "✓ Component $component exists"
    else
        echo "✗ Component $component not found"
    fi
done
```

### Health Check Endpoint Integration
```python
from fastapi import FastAPI
from dapr.ext.grpc import App
import asyncio

app = FastAPI()

@app.get("/health")
async def health_check():
    """Health check endpoint that also validates Dapr connectivity"""
    try:
        from dapr.clients import DaprClient

        with DaprClient() as client:
            # Test basic Dapr connectivity
            health_response = client.wait(10)  # Wait up to 10 seconds for Dapr

            # Test state store connectivity
            client.get_state(store_name='statestore', key='health-test')

        return {
            "status": "healthy",
            "dapr_connected": True,
            "checks": {
                "dapr_sidecar": "ok",
                "state_store": "ok"
            }
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "dapr_connected": False,
            "error": str(e)
        }
```