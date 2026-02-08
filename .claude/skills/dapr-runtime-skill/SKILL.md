---
name: dapr-runtime-skill
description: Design and enforce Dapr runtime usage. Configure Pub/Sub, Jobs API, State, Secrets, Service Invocation. Ensure Dapr sidecars are injected correctly in all services. Validate multi-environment operation (Minikube → Oracle OKE). Collaborate with context-verifier-agent for latest Dapr practices. All service communication must use Dapr APIs, no direct SDK calls.
---

# Dapr Runtime Skill

## Overview
This skill provides guidance for designing and enforcing Dapr runtime usage in the Todo Chatbot application. It focuses on configuring Dapr components (Pub/Sub, Jobs API, State, Secrets, Service Invocation), ensuring proper sidecar injection, and validating multi-environment operations from Minikube to Oracle OKE.

## When to Use This Skill
Use this skill when:
1. Configuring Dapr components for the Todo Chatbot services
2. Setting up Pub/Sub for event-driven communication
3. Implementing Dapr State management for transient data
4. Managing secrets using Dapr Secrets component
5. Setting up service-to-service communication using Dapr Service Invocation
6. Ensuring proper Dapr sidecar injection in Kubernetes deployments
7. Validating multi-environment compatibility (Minikube to Oracle OKE)
8. Ensuring compliance with Phase V constitution regarding Dapr integration

## Prerequisites
- Understanding of Dapr concepts and architecture
- Access to context-verifier-agent for latest Dapr practices
- Knowledge of Kubernetes and Helm deployments
- Understanding of the Todo Chatbot architecture and services

## Core Responsibilities

### 1. Dapr Component Configuration
Configure the five main Dapr building blocks:

#### Pub/Sub Component
- Set up message brokers (Kafka, RabbitMQ, etc.) for event-driven communication
- Configure topics and subscriptions for different services
- Ensure proper message serialization and deserialization

#### State Management Component
- Configure state stores (Redis, CosmosDB, PostgreSQL, etc.)
- Implement state operations (get, save, delete, transaction)
- Handle state consistency and concurrency

#### Secrets Management Component
- Configure secret stores (Kubernetes secrets, HashiCorp Vault, Azure Key Vault, etc.)
- Implement secure retrieval of sensitive data
- Manage secret rotation and access policies

#### Service Invocation Component
- Enable service-to-service communication via Dapr sidecars
- Handle service discovery and load balancing
- Implement circuit breakers and retry policies

#### Actors Component (if needed)
- Configure actor runtimes for stateful services
- Implement actor lifecycle management
- Handle actor reminders and timers

### 2. Sidecar Injection
- Ensure Dapr sidecars are properly injected into all services
- Configure sidecar resources (CPU, memory limits)
- Set up sidecar configuration for different environments
- Validate sidecar health and connectivity

### 3. Multi-Environment Validation
- Ensure configurations work in both Minikube and Oracle OKE
- Validate component compatibility across environments
- Test service communication patterns in different setups
- Verify resource allocation and scaling behavior

## Architecture Guidelines

### Dapr Configuration Principles
1. **Component Isolation**: Separate component configurations by environment and purpose
2. **Security First**: Always use secure communication between Dapr and components
3. **Resilience**: Implement proper error handling and retry mechanisms
4. **Observability**: Enable tracing and monitoring for all Dapr operations
5. **Consistency**: Maintain configuration consistency across all environments

### Service Communication Patterns
1. **No Direct SDK Calls**: All service communication must use Dapr APIs
2. **Service Discovery**: Use Dapr's built-in service discovery
3. **Load Balancing**: Leverage Dapr's automatic load balancing
4. **Circuit Breaking**: Implement circuit breakers through Dapr configuration

## Implementation Steps

### 1. Component Design Phase
1. Identify which Dapr components are needed for the Todo Chatbot
2. Choose appropriate underlying technologies for each component
3. Design component configurations for different environments
4. Validate configurations against security and performance requirements

### 2. Infrastructure Setup
1. Deploy Dapr runtime to the Kubernetes cluster
2. Configure Dapr components with appropriate settings
3. Set up monitoring and observability for Dapr operations
4. Implement health checks for Dapr components

### 3. Service Integration
1. Update existing services to use Dapr APIs instead of direct SDK calls
2. Configure Dapr sidecars for all services
3. Implement proper error handling for Dapr operations
4. Test service communication patterns

### 4. Validation and Testing
1. Test all Dapr components in Minikube environment
2. Validate configurations work in Oracle OKE
3. Verify performance under load
4. Ensure all operations comply with Phase V constitution

## Component Configuration Examples

### Kafka Pub/Sub Component
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
    value: "kafka:9092"
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
```

### Redis State Store Component
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
```

### Kubernetes Secrets Component
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

## Sidecar Injection Configuration

### Annotation-based Injection
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: todo-frontend
spec:
  template:
    metadata:
      annotations:
        dapr.io/enabled: "true"
        dapr.io/app-id: "todo-frontend"
        dapr.io/app-port: "3000"
        dapr.io/config: "dapr-config"
        dapr.io/log-level: "info"
        dapr.io/sidecar-cpu-limit: "0.5"
        dapr.io/sidecar-cpu-request: "0.2"
        dapr.io/sidecar-memory-limit: "512Mi"
        dapr.io/sidecar-memory-request: "256Mi"
```

### Helm Chart Configuration
```yaml
# In values.yaml
dapr:
  enabled: true
  appId: "todo-frontend"
  appPort: 3000
  config: "dapr-config"
  logLevel: "info"
  resources:
    cpu:
      limit: "0.5"
      request: "0.2"
    memory:
      limit: "512Mi"
      request: "256Mi"
```

## Best Practices

### Configuration Management
- Use environment-specific values files for different deployments
- Store sensitive information in Kubernetes secrets
- Use Dapr's built-in secret management when possible
- Implement configuration validation before deployment

### Security
- Enable mTLS for Dapr-to-Dapr communication
- Use appropriate authentication for all Dapr components
- Regularly rotate secrets and certificates
- Monitor for security vulnerabilities in Dapr runtime

### Performance
- Configure appropriate resource limits for Dapr sidecars
- Optimize component configurations for performance
- Monitor sidecar resource usage and adjust as needed
- Implement proper batching for high-throughput scenarios

### Observability
- Enable distributed tracing for all Dapr operations
- Monitor Dapr sidecar metrics
- Set up alerts for Dapr component failures
- Log all Dapr operations for debugging

## Multi-Environment Considerations

### Minikube vs Oracle OKE Differences
- Resource allocation: Adjust limits based on available resources
- Component endpoints: Different service addresses between environments
- Security: Oracle OKE may have stricter security policies
- Networking: Different network policies and firewall rules

### Validation Checklist
- [ ] All Dapr components configured correctly
- [ ] Sidecars properly injected in all services
- [ ] Service invocation working between services
- [ ] Pub/Sub messaging functional
- [ ] State management operations working
- [ ] Secrets properly retrieved and used
- [ ] No direct SDK calls to external services
- [ ] Performance acceptable under load
- [ ] Security policies enforced

## Phase V Constitution Compliance

This skill ensures compliance with:
- **XXV. Dapr Integration Law**: Proper Dapr pub/sub and state management implementation
- **XVIII. Kubernetes Deployment Law**: Proper sidecar injection in Kubernetes deployments
- **XXVI. Cloud Deployment Law**: Compatibility with Oracle OKE deployment
- **XIX. AI-Assisted DevOps Law**: Using tools for Dapr configuration and validation

## Common Commands and Operations

### Using context-verifier-agent
- Get latest Dapr best practices: `context-verifier-agent get dapr-best-practices --version latest`
- Validate Dapr configuration: `context-verifier-agent validate dapr-config --against phase-v-constitution`
- Check component compatibility: `context-verifier-agent check compatibility --component pubsub --target oracle-oke`

### Dapr CLI Operations
- Check Dapr status: `dapr status -k`
- List Dapr components: `dapr components -k`
- View Dapr logs: `dapr logs <app-id>`
- Get Dapr configuration: `dapr configurations -k`

## Troubleshooting

### Common Issues
1. **Sidecar Not Injecting**: Check if Dapr injector is running and annotations are correct
2. **Component Not Found**: Verify component names match between code and configuration
3. **Service Invocation Failing**: Check app-id configuration and network connectivity
4. **State Operations Slow**: Optimize state store configuration and connections
5. **Pub/Sub Not Working**: Verify broker connectivity and topic permissions

### Diagnostic Commands
- Check Dapr health: `dapr health-check --app-id <app-id>`
- Validate component config: `dapr components validate --file <component-file>`
- Trace service invocation: `dapr invoke --app-id <target-app> --method <method> --verb GET`
- Debug sidecar: `kubectl logs <pod-name> daprd`