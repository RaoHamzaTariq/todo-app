# Todo Chatbot Application Documentation

Welcome to the documentation for the Todo Chatbot application. This application is an advanced task management system featuring recurring tasks, due dates, reminders, priorities, tags, and event-driven architecture.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Architecture](#architecture)
3. [Components](#components)
4. [Development](#development)
5. [Deployment](#deployment)
6. [Troubleshooting](#troubleshooting)

## Getting Started

To run the application locally, please refer to the [RUNNING_LOCALLY.md](RUNNING_LOCALLY.md) guide for detailed instructions.

## Architecture

The application follows a microservices architecture with the following components:

### Core Services
- **Backend API**: FastAPI application handling business logic, data persistence, and MCP (Model Context Protocol) functionality
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

## Components

### Frontend
The frontend is built with Next.js and provides:
- Task management interface
- Dashboard with statistics
- Recurring task configuration
- Reminder settings
- User profile management

### Backend
The backend is built with FastAPI and provides:
- RESTful API endpoints
- Business logic implementation
- Data validation and processing
- MCP (Model Context Protocol) functionality for AI agent integration
- Integration with event services

### MCP Integration
The MCP (Model Context Protocol) functionality is integrated directly into the Python backend and provides:
- Model Context Protocol functionality
- AI model integration capabilities
- Context management for AI interactions
- MCP tools that AI agents can call to perform task operations

### Event Services
Various Python services that handle:
- Reminder processing
- Recurring task generation
- Audit logging
- Notifications

## Development

### Prerequisites
- Docker and Docker Compose
- Python 3.11+
- Node.js 18+
- Rust
- uv (Python package manager)
- Helm 3.x
- Kubernetes CLI (kubectl)

### Local Development
1. Set up the development environment following the [RUNNING_LOCALLY.md](RUNNING_LOCALLY.md) guide
2. Make changes to the code
3. Test your changes
4. Submit a pull request

## Deployment

For deployment instructions, please refer to the [DEPLOYMENT_GUIDE.md](../DEPLOYMENT_GUIDE.md) file.

## Troubleshooting

Common issues and solutions:

### Application Not Starting
1. Check if all required services are running
2. Verify environment variables are set correctly
3. Check logs for specific error messages

### Database Connection Issues
1. Ensure PostgreSQL is running
2. Verify database connection string is correct
3. Check if database migrations have been applied

### Kafka Connection Issues
1. Verify Kafka and Zookeeper are running
2. Check if Kafka broker address is configured correctly
3. Ensure network connectivity between services

For more detailed troubleshooting, refer to the deployment guide.