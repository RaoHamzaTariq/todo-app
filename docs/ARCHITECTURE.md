# Todo Chatbot Application Architecture

## Overview

The Todo Chatbot application is an advanced task management system built with a microservices architecture. It consists of two main components: a Python FastAPI backend and a Next.js frontend. The application features recurring tasks, due dates, reminders, priorities, tags, and event-driven architecture. The Model Context Protocol (MCP) functionality is integrated directly into the Python backend, eliminating the need for a separate server.

## Architecture Components

### 1. Backend (Python/FastAPI)

The backend is built with Python 3.13 and FastAPI, providing the core business logic, API endpoints, and MCP (Model Context Protocol) integration.

#### Key Technologies:
- **Python 3.13**: Runtime environment
- **FastAPI**: Web framework with automatic API documentation
- **SQLModel**: ORM/database modeling
- **Dapr**: Distributed application runtime for service-to-service communication
- **Kafka**: Event streaming platform
- **PostgreSQL**: Primary database (Neon Serverless)

#### Key Modules:
- **Models**: Task, User, RecurringTask, Reminder models using SQLModel
- **Services**: Business logic for tasks, recurring tasks, reminders, and event handling
- **API Routes**: RESTful endpoints for tasks, recurring tasks, reminders, and events
- **MCP Integration**: Model Context Protocol tools for AI agent integration (within the same backend)
- **Dapr Middleware**: Service invocation and pub/sub integration
- **Event Handlers**: Processing for task events, reminders, and recurring tasks

#### Key Features:
- JWT authentication with user isolation
- Full CRUD operations for tasks with advanced features
- Recurring task management with various frequencies
- Reminder scheduling and processing
- Event-driven architecture with Kafka
- MCP tools for AI agent integration (Python-based implementation)

### 2. Frontend (Next.js)

The frontend is built with Next.js 14+ using the App Router, providing a modern user interface.

#### Key Technologies:
- **Next.js 14+**: React framework with App Router
- **TypeScript**: Type-safe JavaScript
- **Tailwind CSS**: Utility-first CSS framework
- **Framer Motion**: Animation library
- **Better Auth**: Authentication system
- **Lucide React**: Icon library

#### Key Components:
- **Layout Components**: Header, Sidebar, Footer with responsive design
- **Task Management**: Task forms, lists, and management UI
- **Chat Interface**: Conversational UI with floating widget
- **Dashboard**: Analytics and statistics
- **Authentication**: Sign-in/up forms
- **Calendar**: Task scheduling view
- **Settings**: User preferences and configuration

#### Key Features:
- Responsive design for all device sizes
- Real-time task management
- Conversational AI interface
- Advanced task filtering and search
- User authentication and authorization
- Dark/light mode support

### 3. MCP Integration (Python-based)

The Model Context Protocol (MCP) functionality is integrated directly into the Python backend, providing AI agent integration capabilities without requiring a separate server.

#### Key Technologies:
- **Python**: Same runtime as the backend
- **FastMCP**: Python-based framework for MCP implementation
- **OpenAI Agents SDK**: Integration with OpenAI's agent framework

#### Key Features:
- MCP tools for task operations that AI agents can call
- Direct integration with the backend's task management system
- Standardized protocol for AI model context access
- Secure tool access for AI agents
- Same deployment and scaling as the main backend

## Architecture Flow

### 1. User Interaction Flow
1. User interacts with the Next.js frontend
2. Frontend makes API calls to the FastAPI backend
3. Backend processes requests, validates user permissions
4. Backend stores data in PostgreSQL
5. Backend publishes events to Kafka via Dapr
6. Event services consume events and perform actions
7. Results are returned to the frontend

### 2. AI Agent Integration Flow
1. AI agent communicates with the backend through OpenAI-compatible API
2. Agent calls MCP tools exposed by the Python backend
3. MCP tools perform operations on tasks within the same process
4. Operations are validated and persisted in the database
5. Events are published for other services via Kafka

### 3. Event-Driven Architecture
1. Task operations trigger events in the backend
2. Events are published to Kafka via Dapr pub/sub
3. Various event services consume relevant events:
   - Reminder service processes reminder events
   - Recurring task service manages recurring patterns
   - Audit log service maintains system logs
   - Notification service sends user notifications
4. Services can publish their own events for other services

## Deployment Architecture

### Local Development
- Docker Compose for local service orchestration
- PostgreSQL, Kafka, and other dependencies in containers
- Hot-reload for frontend and backend development
- Single Python process serving both API and MCP functionality

### Production Deployment
- Kubernetes (Oracle OKE) for container orchestration
- Helm charts for deployment management
- Dapr for service mesh and building blocks
- Horizontal Pod Autoscaler for scaling
- Prometheus and Grafana for monitoring
- GitHub Actions for CI/CD pipeline

## Security Considerations

- JWT-based authentication with user isolation
- Strict validation of user_id in all requests
- Dapr for secure service-to-service communication
- Environment variable management for secrets
- SQL injection prevention through SQLModel
- Rate limiting and input validation
- Secure MCP tool access with proper authentication

## Data Flow

1. User creates a task via the frontend
2. Frontend sends request to backend API
3. Backend validates JWT and user permissions
4. Backend creates task in PostgreSQL
5. Backend publishes "task.created" event to Kafka
6. Event services process the event as needed
7. Response is returned to frontend
8. Frontend updates UI with new task

## Integration Points

- **Frontend ↔ Backend**: REST API with JWT authentication
- **AI Agent ↔ Backend**: MCP protocol for AI agent tools (Python-based)
- **Backend ↔ Kafka**: Event publishing via Dapr
- **Event Services ↔ Kafka**: Event consumption via Dapr
- **Backend ↔ PostgreSQL**: Data persistence via SQLModel
- **Services ↔ Dapr**: Service invocation and pub/sub

This architecture provides a scalable, maintainable, and feature-rich task management system with AI integration capabilities, with the MCP functionality seamlessly integrated into the main backend service.