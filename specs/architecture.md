# Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                      Frontend (Next.js)                      │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │                   Browser / Client                       │ │
│  └─────────────────────────────────────────────────────────┘ │
│           │                                    ▲             │
│           │ JWT Token                         │             │
│           ▼                                    │             │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │                   Better Auth                            │ │
│  │           (Sign up / Sign in / Session Mgmt)             │ │
│  └─────────────────────────────────────────────────────────┘ │
│           │                                                   │
│           │ HTTP Requests + JWT                               │
│           ▼                                                   │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │                   FastAPI Backend                        │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐  │ │
│  │  │ JWT Verify  │  │   Routes    │  │   SQLModel DB   │  │ │
│  │  │ Middleware  │  │   (REST)    │  │     Layer       │  │ │
│  │  └─────────────┘  └─────────────┘  └─────────────────┘  │ │
│  └─────────────────────────────────────────────────────────┘ │
│           │                                                   │
│           │ PostgreSQL Protocol                               │
│           ▼                                                   │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │              Neon Serverless PostgreSQL                  │ │
│  │     (users table + tasks table with foreign keys)        │ │
│  └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## Authentication Flow

1. User accesses Next.js frontend
2. User signs up/in via Better Auth
3. Better Auth creates session and issues JWT
4. Frontend stores JWT (typically in cookie or memory)
5. Frontend sends API requests with `Authorization: Bearer <JWT>`
6. FastAPI validates JWT signature using shared secret
7. FastAPI extracts user details from token
8. FastAPI returns only authenticated user's tasks

## Component Responsibilities

### Frontend (Next.js)
- Render UI components
- Handle user interactions
- Manage authentication state via Better Auth
- Attach JWT token to API requests
- Display task data and handle forms

### Backend (FastAPI)
- Expose REST API endpoints
- Validate JWT tokens on all requests
- Query database via SQLModel
- Enforce user-task ownership
- Return JSON responses

### Database (Neon PostgreSQL)
- Store user accounts (managed by Better Auth)
- Store tasks with user association
- Provide indexes for performance
- Ensure data integrity via foreign keys

## API Architecture

### RESTful Design
- Resources: tasks, users
- HTTP methods: GET, POST, PUT, PATCH, DELETE
- Response codes: 200, 201, 400, 401, 404, 500

### User-Scoped Data
All task endpoints are scoped to the authenticated user:
- `GET /api/{user_id}/tasks`
- `POST /api/{user_id}/tasks`
- `GET /api/{user_id}/tasks/{id}`
- `PUT /api/{user_id}/tasks/{id}`
- `DELETE /api/{user_id}/tasks/{id}`
- `PATCH /api/{user_id}/tasks/{id}/complete`

## Security Measures

| Layer | Measure |
|-------|---------|
| Transport | HTTPS in production |
| Auth | JWT with expiration (7 days) |
| API | Bearer token validation |
| Data | User-task ownership enforcement |
| Secrets | Environment variables only |

## Environment Configuration

### Frontend
```env
BETTER_AUTH_SECRET=your-secret-key
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Backend
```env
DATABASE_URL=postgresql+psycopg://user:pass@host/db
BETTER_AUTH_SECRET=your-secret-key
JWT_ALGORITHM=HS256
```
