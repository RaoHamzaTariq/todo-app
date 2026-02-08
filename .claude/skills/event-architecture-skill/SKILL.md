---
name: event-architecture-skill
description: Manage event-driven system for Todo Chatbot using Kafka and Dapr. Design topics, consumers, producers for reminders, recurring tasks, audit logs, and real-time sync. Validate event schemas and Dapr Pub/Sub integration. Use kafka-dapr-agent, dapr-runtime-agent, and k8s-deployment-agent to ensure cluster compatibility. Align with Phase V constitution and use Context7 MCP server for guidance.
---

# Event Architecture Skill

## Overview
This skill manages the event-driven architecture for the Todo Chatbot using Kafka and Dapr. It designs and validates event flows, topics, consumers, and producers to support reminders, recurring tasks, audit logs, and real-time synchronization.

## When to Use This Skill
Use this skill when:
1. Designing event-driven systems for the Todo Chatbot
2. Creating Kafka topics and consumers for task events
3. Implementing Dapr Pub/Sub integration
4. Setting up event flows for reminders, recurring tasks, audit logs, or real-time sync
5. Validating event schemas and ensuring cluster compatibility
6. Ensuring alignment with Phase V constitution requirements

## Prerequisites
- Access to kafka-dapr-agent for designing topics, consumers, and producers
- Access to dapr-runtime-agent for runtime configuration
- Access to k8s-deployment-agent for cluster compatibility
- Context7 MCP server for latest Kafka + Dapr guidance
- Understanding of Phase V constitution

## Core Responsibilities

### 1. Kafka Topic Design
- Design appropriate Kafka topics for the system:
  - `task-events` - For all task lifecycle events
  - `reminders` - For scheduled reminder events
  - `task-updates` - For task modification events
  - `audit-logs` - For system audit events
- Ensure proper partitioning and replication factors
- Define retention policies based on system requirements

### 2. Consumer and Producer Implementation
- Create event producers that publish to appropriate topics
- Implement consumers that process events reliably
- Ensure proper error handling and dead letter queue setup
- Implement retry mechanisms for failed events

### 3. Event Flow Management
- Design event flows for:
  - Reminder scheduling and delivery
  - Recurring task execution
  - Audit logging of all important operations
  - Real-time synchronization between services
- Ensure event ordering where necessary
- Implement circuit breakers for resilience

### 4. Dapr Integration
- Configure Dapr Pub/Sub components to work with Kafka
- Define Dapr component configurations for Kafka
- Implement service invocation using Dapr
- Set up state management using Dapr where appropriate

### 5. Schema Validation
- Define and maintain event schemas for all topics
- Implement schema validation for incoming events
- Ensure backward compatibility for schema evolution
- Document all event formats and structures

## Architecture Guidelines

### Event-Driven Architecture Principles
1. **Decoupling**: Services should communicate asynchronously through events
2. **Resilience**: System should continue operating even if individual components fail
3. **Scalability**: Event processing should scale independently of producers
4. **Auditability**: All important operations should be captured as events
5. **Real-time Processing**: Time-sensitive events (like reminders) should be processed promptly

### Kafka Configuration
- Use appropriate partition counts based on throughput requirements
- Configure proper replication factors for durability
- Set up appropriate retention policies for different event types
- Monitor consumer lag to ensure timely processing

### Dapr Component Configuration
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
    value: "dapr-group"
```

## Implementation Steps

### 1. Event Design Phase
1. Identify all event types needed for the system
2. Define event schemas with appropriate fields
3. Map events to Kafka topics based on domain boundaries
4. Define consumer groups for different services
5. Validate schema design against Phase V constitution

### 2. Infrastructure Setup
1. Deploy Kafka cluster (locally with Minikube or cloud with Oracle OKE)
2. Configure Dapr with Kafka pub/sub component
3. Set up monitoring and alerting for event processing
4. Implement health checks for event-driven services

### 3. Service Integration
1. Modify existing services to publish relevant events
2. Create new event-driven services for:
   - Reminder processing
   - Recurring task execution
   - Audit logging
   - Real-time synchronization
3. Implement proper error handling and retries
4. Ensure all services validate user permissions before processing events

### 4. Validation and Testing
1. Test event flow end-to-end
2. Validate schema compliance
3. Test failure scenarios and recovery
4. Verify performance under load
5. Ensure all operations comply with Multi-User Security Law (Principle VI)

## Best Practices

### Event Design
- Keep events small and focused on a single action
- Include correlation IDs for tracking related operations
- Use consistent naming conventions
- Include timestamps for all events
- Design for eventual consistency

### Error Handling
- Implement dead letter queues for unprocessable events
- Use exponential backoff for retries
- Log all errors with sufficient context for debugging
- Alert on sustained error rates

### Monitoring
- Track consumer lag for all topics
- Monitor event processing rates
- Alert on failed event processing
- Track end-to-end event latency

## Integration with Other Components

### MCP Integration
- Ensure event-driven services validate `user_id` for data ownership as required by MCP law
- Publish relevant events when MCP tools are invoked
- Subscribe to events that may affect task state

### Authentication Integration
- Validate JWT tokens in event consumers where necessary
- Ensure user permissions are checked before processing user-specific events
- Maintain audit trails of all authenticated operations

### Database Integration
- Use events to trigger database updates rather than direct calls where appropriate
- Implement eventual consistency patterns between events and database state
- Maintain referential integrity across event and database systems

## Phase V Constitution Compliance

This skill ensures compliance with:
- **XXIV. Event-Driven Architecture Law**: Proper Kafka topic design and event processing
- **XXV. Dapr Integration Law**: Correct Dapr pub/sub and state management implementation
- **XXIII. Advanced Todo Features Law**: Event flows for recurring tasks and reminders
- **VI. Multi-User Security Law**: Proper user validation in event consumers
- **XXVI. Cloud Deployment Law**: Compatibility with Oracle OKE deployment

## Common Commands and Operations

### Using kafka-dapr-agent
- Design topics: `kafka-dapr-agent design topics --domain task-management`
- Generate consumers: `kafka-dapr-agent generate consumer --topic task-events`
- Validate schemas: `kafka-dapr-agent validate schemas --against latest`

### Using dapr-runtime-agent
- Configure components: `dapr-runtime-agent configure pubsub --type kafka`
- Check status: `dapr-runtime-agent status --component kafka-pubsub`

### Using k8s-deployment-agent
- Deploy Kafka: `k8s-deployment-agent deploy kafka-cluster --namespace event-system`
- Scale consumers: `k8s-deployment-agent scale consumer --replicas 3`

## Troubleshooting

### Common Issues
1. **Consumer Lag**: Increase consumer replicas or optimize processing logic
2. **Schema Validation Errors**: Check event format against defined schema
3. **Dapr Component Issues**: Verify component configuration and connectivity
4. **Security Issues**: Ensure all event consumers validate user permissions

### Diagnostic Commands
- Check topic health: `kafka-dapr-agent diagnose topic --name task-events`
- View consumer groups: `kafka-dapr-agent list consumers --topic all`
- Monitor Dapr: `dapr-runtime-agent logs --component kafka-pubsub`