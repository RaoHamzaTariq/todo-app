# Implementation Plan: Phase V - Advanced Cloud Deployment of Todo Chatbot

**Branch**: `005-advanced-cloud-deployment` | **Date**: 2026-02-05 | **Spec**: [specs/005-advanced-cloud-deployment/spec.md]
**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

## Summary

Based on the Phase V specification, this plan outlines the implementation of an event-driven Todo Chatbot with advanced features (recurring tasks, due dates, reminders, priorities, tags) using Kafka and Dapr for Oracle OKE deployment. The architecture leverages event-driven patterns with Kafka as the backbone and Dapr as the abstraction layer for pub/sub, state management, jobs, secrets, and service invocation.

## Technical Context

**Language/Version**: Python 3.13+ (backend), TypeScript (frontend), with FastAPI, SQLModel, Next.js, Better Auth
**Primary Dependencies**: Kafka, Dapr, Neon Serverless PostgreSQL, OpenAI Agents SDK, Official MCP SDK, Helm
**Storage**: Neon Serverless PostgreSQL, Redis (for caching), Dapr state management
**Testing**: pytest (backend), Jest (frontend), Helm test (infrastructure)
**Target Platform**: Kubernetes (Minikube for local, Oracle OKE for cloud)
**Project Type**: Web application with event-driven services
**Performance Goals**: Handle 1000+ concurrent users, process task events with <200ms latency, maintain 99.9% uptime
**Constraints**: <100ms p95 response time for API requests, <500MB memory per service, event-driven with <5 minutes reminder delivery
**Scale/Scope**: Support 10,000+ users, 1M+ tasks, auto-scale from 2 to 20 pods based on load

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Compliance Check**: All implementation aligns with Phase V Constitution (XXIII-XXIX)
- **Multi-User Security Law**: All event-driven services validate user_id for data ownership
- **Event-Driven Architecture Law**: Using Kafka topics for task events, reminders, updates, audit logs
- **Dapr Integration Law**: Using Dapr for pub/sub abstraction, state management, service invocation, secrets
- **Cloud Deployment Law**: Supporting both Minikube (local) and Oracle OKE (cloud) with Helm reuse
- **AI-Assisted DevOps Enhancement Law**: Leveraging Docker AI, kubectl-ai, Kagent for operations
- **Context Validation Law**: Validating all configurations with MCP server and best practices

## Project Structure

### Documentation (this feature)

```text
specs/005-advanced-cloud-deployment/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/
│   │   ├── task_model.py
│   │   ├── recurring_task_model.py
│   │   ├── reminder_model.py
│   │   └── user_model.py
│   ├── services/
│   │   ├── task_service.py
│   │   ├── recurring_task_service.py
│   │   ├── reminder_service.py
│   │   ├── kafka_producer.py
│   │   ├── dapr_integration.py
│   │   └── event_handlers.py
│   ├── api/
│   │   ├── main.py
│   │   ├── routes/
│   │   │   ├── tasks.py
│   │   │   ├── recurring_tasks.py
│   │   │   ├── reminders.py
│   │   │   └── events.py
│   │   └── middleware/
│   │       ├── auth_middleware.py
│   │       └── dapr_middleware.py
│   └── config/
│       ├── settings.py
│       └── dapr_config.py
└── tests/

frontend/
├── src/
│   ├── components/
│   │   ├── TaskManagement/
│   │   │   ├── TaskList.jsx
│   │   │   ├── TaskCard.jsx
│   │   │   ├── RecurringTaskForm.jsx
│   │   │   └── ReminderSettings.jsx
│   │   ├── EventStream/
│   │   │   ├── EventFeed.jsx
│   │   │   └── WebSocketHandler.jsx
│   │   └── Dashboard/
│   │       ├── AdvancedFeatures.jsx
│   │       └── UserPreferences.jsx
│   ├── pages/
│   │   ├── Dashboard.jsx
│   │   ├── Tasks.jsx
│   │   └── Settings.jsx
│   └── services/
│       ├── apiClient.js
│       ├── eventStream.js
│       └── daprIntegration.js
└── tests/

event-services/
├── reminder-service/
│   ├── src/
│   │   ├── main.py
│   │   ├── reminder_processor.py
│   │   └── kafka_consumer.py
│   └── Dockerfile
├── recurring-task-service/
│   ├── src/
│   │   ├── main.py
│   │   ├── recurring_task_scheduler.py
│   │   └── kafka_consumer.py
│   └── Dockerfile
├── audit-log-service/
│   ├── src/
│   │   ├── main.py
│   │   ├── audit_processor.py
│   │   └── kafka_consumer.py
│   └── Dockerfile
└── notification-service/
    ├── src/
    │   ├── main.py
    │   ├── notification_sender.py
    │   └── kafka_consumer.py
    └── Dockerfile

k8s/
├── kafka/
│   ├── kafka-deployment.yaml
│   ├── kafka-service.yaml
│   └── kafka-pvc.yaml
├── dapr/
│   ├── dapr-components/
│   │   ├── kafka-pubsub.yaml
│   │   ├── postgres-state.yaml
│   │   └── kubernetes-secrets.yaml
│   └── dapr-configuration.yaml
├── services/
│   ├── backend-deployment.yaml
│   ├── backend-service.yaml
│   ├── frontend-deployment.yaml
│   ├── frontend-service.yaml
│   ├── reminder-service-deployment.yaml
│   ├── recurring-task-service-deployment.yaml
│   ├── audit-log-service-deployment.yaml
│   └── notification-service-deployment.yaml
└── monitoring/
    ├── prometheus-config.yaml
    └── grafana-dashboard.yaml

helm/
├── todo-app/
│   ├── Chart.yaml
│   ├── values.yaml
│   └── templates/
│       ├── backend/
│       │   ├── deployment.yaml
│       │   ├── service.yaml
│       │   └── hpa.yaml
│       ├── frontend/
│       │   ├── deployment.yaml
│       │   ├── service.yaml
│       │   └── ingress.yaml
│       ├── event-services/
│       │   ├── reminder-service-deployment.yaml
│       │   ├── recurring-task-service-deployment.yaml
│       │   ├── audit-log-service-deployment.yaml
│       │   └── notification-service-deployment.yaml
│       ├── infrastructure/
│       │   ├── kafka/
│       │   └── dapr/
│       └── NOTES.txt
└── todo-backend/
    ├── Chart.yaml
    ├── values.yaml
    └── templates/
        └── (backend-specific templates)

.github/
└── workflows/
    ├── ci-cd-pipeline.yml
    ├── deploy-minikube.yml
    └── deploy-oracle-oke.yml
```

**Structure Decision**: Selected web application structure with additional event-driven services to support advanced features and cloud deployment. The monorepo contains backend, frontend, and event-driven services with supporting Kubernetes and Helm configurations.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Additional event-driven services | Event-driven architecture required for scalable task processing | Direct synchronous processing insufficient for recurring tasks and reminders |
| Dapr abstraction layer | Needed for vendor-neutral pub/sub, state management, and service invocation | Direct Kafka SDK would tie implementation to specific broker |
| Oracle OKE deployment | Phase V constitution mandates cloud deployment | Staying with local deployment would not meet cloud readiness requirement |

## Technical Strategy

### 1. Event-Driven Architecture (Kafka + Dapr)
**Skill to use**: `event-architecture-skill`
**Subagent contribution**: kafka-dapr-agent for topic design and consumer/producer generation
**Context7 validation**: Validate Kafka + Dapr configurations using MCP server
**Expected output artifacts**:
- Kafka topic definitions
- Event schema definitions
- Producer and consumer implementations
- Dapr component configurations

**Implementation details**:
- **Kafka Topics Design**:
  - `task-events` - For all task lifecycle events (creation, update, deletion)
  - `reminders` - For scheduled reminder events
  - `task-updates` - For task modification events
  - `audit-logs` - For system audit events
- **Event Producers**: Backend service publishes events to appropriate Kafka topics via Dapr
- **Event Consumers**: Specialized event-driven services consume from Kafka topics via Dapr
- **Schema Validation**: All events follow defined schema with versioning for backward compatibility

### 2. Distributed Runtime with Dapr
**Skill to use**: `dapr-runtime-skill`
**Subagent contribution**: dapr-runtime-agent for component configuration and validation
**Context7 validation**: Validate Dapr configurations using MCP server
**Expected output artifacts**:
- Dapr component configurations
- Sidecar injection annotations
- Service invocation implementations

**Implementation details**:
- **Pub/Sub Component**: Dapr pub/sub configured with Kafka as the underlying broker
- **State Management**: Dapr state management for non-critical transient data
- **Jobs API**: Utilize Dapr Jobs API for scheduled operations (reminders, recurring tasks)
- **Service Invocation**: Dapr service invocation for inter-service communication
- **Secrets Management**: Dapr secrets configured to access Kubernetes secrets

### 3. Kubernetes Deployment (Minikube → Oracle OKE)
**Skill to use**: `k8s-deployment-orchestrator`
**Subagent contribution**: k8s-deployment-agent for manifest generation and validation
**Context7 validation**: Validate Oracle OKE compatibility using MCP server
**Expected output artifacts**:
- Kubernetes deployment/service configurations
- Helm charts for deployment management
- Environment-specific values files

**Implementation details**:
- **Helm Chart Reuse**: Extend Phase IV Helm charts with event-driven service configurations
- **Namespace Management**: Separate namespaces for different environments (dev/staging/prod)
- **Sidecar Injection**: All services configured with Dapr sidecar injection
- **Resource Management**: Proper resource limits and requests for Oracle OKE deployment
- **Health Checks**: Liveness and readiness probes for all services

### 4. CI/CD and Observability
**Skill to use**: `ci-cd-observability-skill`
**Subagent contribution**: ci-cd-agent for pipeline design and implementation
**Context7 validation**: Validate CI/CD configurations using MCP server
**Expected output artifacts**:
- GitHub Actions workflows
- Monitoring and logging configurations
- Environment promotion configurations

**Implementation details**:
- **Pipeline Design**: Automated pipeline from Minikube to Oracle OKE
- **Monitoring**: Prometheus and Grafana for metrics, ELK stack for logs
- **Alerting**: Set up alerts for service failures and performance degradation
- **Environment Promotion**: Automated promotion from dev to staging to production

## Architecture Diagrams & Descriptions

### Logical Overview
```
┌─────────────┐    HTTP     ┌─────────────┐  Dapr Service   ┌──────────────────┐
│   Frontend  │ ─────────►  │   Backend   │ ──────────────► │ Event Services   │
│   (Next.js) │ ◄────────   │  (FastAPI)  │                 │ (Python)         │
└─────────────┘   Events    └─────────────┘                 └──────────────────┘
                                │                                    │
                                ▼                                    ▼
                    ┌─────────────────────────┐        ┌─────────────────────────┐
                    │     Dapr Runtime        │        │      Dapr Runtime       │
                    │   (Service Mesh)        │        │     (Event Services)    │
                    └─────────────────────────┘        └─────────────────────────┘
                                │                                    │
                                ▼                                    ▼
                    ┌─────────────────────────┐        ┌─────────────────────────┐
                    │        Kafka            │ ◄──────┤        Kafka            │
                    │    (Event Broker)       │        │    (Event Broker)       │
                    └─────────────────────────┘        └─────────────────────────┘
                                │
                                ▼
                    ┌─────────────────────────┐
                    │    Neon PostgreSQL      │
                    │     (Persistence)       │
                    └─────────────────────────┘
```

### Integration Points with Kafka & Dapr
- **Event Producers**: Backend service uses Dapr pub/sub to publish task events to Kafka
- **Event Consumers**: Specialized services subscribe to Kafka topics via Dapr pub/sub
- **State Management**: Dapr state management for temporary data, SQLModel for persistent data
- **Service Invocation**: Dapr service invocation for inter-service communication instead of direct calls

### Environment Differences: Minikube vs Oracle OKE
- **Minikube**: Local development, single-node cluster, resource constraints, simplified networking
- **Oracle OKE**: Production deployment, multi-node cluster, higher resource limits, enterprise-grade security, autoscaling

## Component Design Details

### Event Producers & Consumers
**Producers** (Backend Service):
- `TaskCreatedEventProducer`: Publishes task creation events to `task-events` topic
- `TaskUpdatedEventProducer`: Publishes task update events to `task-updates` topic
- `ReminderScheduledEventProducer`: Publishes reminder events to `reminders` topic

**Consumers** (Event Services):
- `ReminderProcessor`: Consumes from `reminders` topic, sends notifications to users
- `RecurringTaskScheduler`: Consumes from `task-events` to manage recurring task creation
- `AuditLogger`: Consumes from all topics to maintain audit logs
- `NotificationSender`: Consumes from various topics to send user notifications

### Pub/Sub and Jobs API Mapping
- **Tasks Pub/Sub**: `task-events` topic for task lifecycle events
- **Reminders Pub/Sub**: `reminders` topic for scheduled reminder processing
- **Updates Pub/Sub**: `task-updates` topic for task modification events
- **Audit Pub/Sub**: `audit-logs` topic for system audit events
- **Jobs API**: For scheduling recurring tasks and reminder notifications

### Service Invocation Flows with Dapr
- `frontend` → `dapr invoke --app-id backend --method /api/user_id/tasks` → `backend`
- `backend` → `dapr invoke --app-id reminder-service --method /schedule` → `reminder-service`
- `recurring-task-service` → `dapr invoke --app-id backend --method /api/user_id/tasks` → `backend`

### Secrets and State Management
- **Secrets**: Dapr configured to access Kubernetes secrets for JWT tokens, database credentials
- **State**: Dapr state management for session data, temporary processing states
- **Persistent Data**: SQLModel with Neon PostgreSQL for all permanent data

## Integration Points & Dependencies

### Kafka Topics and Consumer Groups
- **Topics**: `task-events`, `reminders`, `task-updates`, `audit-logs`
- **Consumer Groups**: `task-consumer-group`, `reminder-consumer-group`, `audit-consumer-group`
- **Partitions**: Configured based on expected throughput and parallelism requirements
- **Retention**: Policies set based on compliance and storage requirements

### Dapr Component Manifests
- **Kafka Pub/Sub Component**: Configures Dapr to use Kafka as message broker
- **PostgreSQL State Component**: Configures Dapr state management with PostgreSQL
- **Kubernetes Secrets Component**: Configures Dapr to access Kubernetes secrets

### Helm Chart Customization and Values
- **Values Files**: Environment-specific configurations for dev, staging, production
- **Template Customization**: Add event-driven services to existing Helm charts
- **Dependency Management**: Include Kafka and Dapr as chart dependencies

### CI/CD Triggers and Environment Promotion
- **Triggers**: GitHub Actions triggered on pushes to specific branches
- **Promotion Strategy**: Automated promotion with manual approval gates
- **Environment Validation**: Health checks and smoke tests before promotion

## Validation Strategy

### Using context-verifier-agent for validation:
1. **Architecture Validation**: Verify event-driven architecture complies with Kafka/Dapr best practices
2. **Cloud Readiness**: Confirm Oracle OKE compatibility and resource requirements
3. **Security Validation**: Validate all services properly authenticate and authorize requests
4. **Performance Validation**: Ensure system meets performance goals specified in requirements

### Validation checkpoints:
- [ ] Dapr configurations validated against current best practices
- [ ] Kafka topic design validated for performance and scalability
- [ ] Helm charts validated for Oracle OKE deployment
- [ ] CI/CD pipelines validated for multi-environment deployment
- [ ] Security configurations validated against compliance requirements
- [ ] Performance targets validated through testing and simulation