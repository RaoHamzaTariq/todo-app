# Todo App Overview

## Purpose
A todo application that evolves from console app to AI chatbot.

## Current Phase
Phase II: Full-Stack Web Application

## Vision
Transform the console-based todo application into a modern, multi-user full-stack web application with persistent storage using Next.js, FastAPI, and Neon Serverless PostgreSQL.

## Tech Stack

### Frontend
- Next.js 16+ (App Router)
- TypeScript
- Tailwind CSS
- Better Auth (authentication)

### Backend
- FastAPI
- SQLModel (ORM)
- Neon Serverless PostgreSQL
- Python 3.13+

### Infrastructure
- JWT-based authentication
- RESTful API architecture
- Container-ready (Docker)

## Features

### Phase II Features
- [ ] Task CRUD operations
- [ ] User authentication (signup/signin)
- [ ] Task filtering and sorting
- [ ] JWT-based API security
- [ ] Responsive web UI

### Future Phases
- Phase III: AI Chatbot integration

## Architecture Overview

- **Frontend:** Next.js app handles UI and user authentication via Better Auth
- **Backend:** FastAPI server exposes REST API endpoints
- **Database:** Neon PostgreSQL stores user and task data
- **Auth Flow:** JWT tokens issued by Better Auth, validated by FastAPI

## Related Specifications

- Architecture: `@specs/architecture.md`
- Task CRUD: `@specs/features/task-crud.md`
- Authentication: `@specs/features/authentication.md`
- API Endpoints: `@specs/api/rest-endpoints.md`
- Database Schema: `@specs/database/schema.md`
