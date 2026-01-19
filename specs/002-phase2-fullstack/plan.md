# Implementation Plan: Phase 2 Full-Stack Todo Application

**Branch**: `002-phase2-fullstack` | **Date**: 2026-01-04 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-phase2-fullstack/spec.md`

## Summary

Transform the Phase 1 CLI todo application into a modern, multi-user full-stack web application with persistent storage. The system will consist of a Next.js 16+ frontend with Better Auth authentication and a FastAPI backend with Neon PostgreSQL database. All task operations are protected by JWT authentication with strict user isolation.

**Technical Approach**: Monorepo architecture with frontend and backend separation, JWT-based stateless authentication, RESTful API with user-scoped endpoints, and SQLModel ORM for database operations.

## Technical Context

**Language/Version**:
- Frontend: TypeScript 5.x with Next.js 16+
- Backend: Python 3.13+

**Primary Dependencies**:
- Frontend: Next.js 16+, Better Auth v1.x (with jwtClient plugin), Tailwind CSS, React Query/SWR
- Backend: FastAPI, SQLModel, python-jose[cryptography], psycopg (PostgreSQL adapter)

**Storage**: Neon Serverless PostgreSQL (managed cloud PostgreSQL service)

**Testing**:
- Frontend: Jest, React Testing Library, Playwright (E2E)
- Backend: pytest, pytest-asyncio, httpx (FastAPI test client)

**Target Platform**:
- Frontend: Web browsers (Chrome, Firefox, Safari, Edge) - responsive design for mobile/tablet/desktop
- Backend: Linux server (containerized with Docker)

**Project Type**: Web application (monorepo with frontend + backend)

**Performance Goals**:
- Task CRUD operations complete within 2 seconds (SC-003)
- Signup/signin flows complete under 30 seconds each (SC-001)
- Support multiple concurrent users with data isolation (SC-002)
- Frontend: First Contentful Paint < 1.5s, Time to Interactive < 3s

**Constraints**:
- 100% data isolation between users (zero data leakage) (SC-004)
- All sensitive config via environment variables (FR-012)
- HTTPS required for production, HTTP allowed for localhost
- JWT expiration enforced on every request
- user_id from token claims only, never from request body

**Scale/Scope**:
- Initial deployment: 100-1000 concurrent users
- Task volume: up to 10,000 tasks per user
- 6 user stories with full CRUD operations
- Responsive UI for 3 viewport sizes (mobile, tablet, desktop)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Principle Compliance

| Principle | Status | Notes |
|-----------|--------|-------|
| **I. Spec-Driven Development (SDD)** | ✅ PASS | Following /sp.specify → /sp.plan → /sp.tasks → /sp.implement workflow |
| **II. Python 3.13+ Standard** | ✅ PASS | Backend uses Python 3.13+ with type hints, PEP 8, functional patterns |
| **III. Monorepo Architecture** | ✅ PASS | Frontend (/frontend) and backend (/backend) clearly separated |
| **IV. Code Quality Standards** | ✅ PASS | TypeScript for frontend, Python type hints for backend |
| **V. Task ID Requirement** | ✅ PASS | All implementations will reference tasks.md Task IDs |
| **VI. Multi-User Security Law** | ✅ PASS | Every task owned by user_id, JWT verification on all protected endpoints |
| **VII. Authentication Law** | ✅ PASS | Better Auth (frontend) + JWT verification (backend) |
| **VIII. API Standards** | ✅ PASS | RESTful /api/{user_id}/tasks/ pattern with proper HTTP methods |
| **IX. Persistence Law** | ✅ PASS | Neon PostgreSQL (no in-memory storage), SQLModel ORM |
| **X. Web-First Architecture** | ✅ PASS | CLI deprecated, web UI is primary interface |
| **XI. Constitution Compliance** | ✅ PASS | Pre-check completed, no violations |
| **XII. Smallest Viable Change** | ✅ PASS | Focused on 6 core user stories, minimal scope creep |

### Active Skills Referenced in Plan

Based on the specification's **Skills Activated** section and the user's request to mention skills in the plan:

- **better-auth-specialist**: JWT configuration, token verification, user_id validation
- **auth-security-specialist**: JWT middleware, stateless verification, Bearer token patterns
- **data-ownership-enforcer**: User isolation, ownership verification, 403/404 error handling
- **api-contract-steward**: RESTful endpoint design, OpenAPI contracts, response schemas
- **monorepo-architect**: Frontend/backend separation, independent package management
- **clean-code-pythonist**: Python code quality, type hints, PEP 8 compliance

**No Constitution Violations** - All principles aligned with feature requirements.

## Project Structure

### Documentation (this feature)

```text
specs/002-phase2-fullstack/
├── spec.md              # Feature specification (completed)
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (to be generated)
├── data-model.md        # Phase 1 output (to be generated)
├── quickstart.md        # Phase 1 output (to be generated)
├── contracts/           # Phase 1 output (to be generated)
│   ├── openapi.yaml     # OpenAPI 3.0 specification
│   └── schemas/         # Request/response schemas
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
# Monorepo structure: Web application (frontend + backend)

frontend/
├── src/
│   ├── app/
│   │   ├── layout.tsx           # Root layout with providers
│   │   ├── page.tsx             # Home/Dashboard
│   │   ├── globals.css          # Global styles
│   │   ├── (auth)/
│   │   │   ├── sign-in/
│   │   │   │   └── page.tsx
│   │   │   └── sign-up/
│   │   │       └── page.tsx
│   │   ├── tasks/
│   │   │   ├── page.tsx         # Task list
│   │   │   ├── new/
│   │   │   │   └── page.tsx     # Create task
│   │   │   └── [id]/
│   │   │       ├── page.tsx     # Task detail
│   │   │       └── edit/
│   │   │           └── page.tsx # Edit task
│   │   └── api/
│   │       ├── auth/
│   │       │   └── [...auth]/
│   │       │       └── route.ts # Better Auth API routes
│   │       └── tasks/
│   │           ├── route.ts     # Task list API routes (GET, POST)
│   │           └── [id]/
│   │               ├── route.ts # Individual task API routes (GET, PUT, DELETE)
│   │               └── complete/
│   │                   └── route.ts # Task completion API route (PATCH)
│   ├── components/
│   │   ├── TaskList.tsx
│   │   ├── TaskItem.tsx
│   │   ├── TaskForm.tsx
│   │   ├── AuthForm.tsx
│   │   ├── Header.tsx
│   │   └── ui/                  # Shared UI components (Button, Input, etc.)
│   └── lib/
│       ├── auth-client.ts       # Better Auth client with jwtClient() plugin
│       └── config.ts            # Environment validation
├── .env.local
├── next.config.js
├── package.json
├── tsconfig.json
└── tailwind.config.js

backend/
├── src/
│   ├── main.py                  # FastAPI app entry point
│   ├── app/
│   │   ├── __init__.py
│   │   ├── config.py            # Settings and environment validation
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── user.py          # User model (Better Auth schema reference)
│   │   │   └── task.py          # Task SQLModel definition
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── task.py          # Pydantic schemas (CreateTask, UpdateTask, TaskResponse)
│   │   │   └── error.py         # Error response schemas
│   │   ├── routers/
│   │   │   ├── __init__.py
│   │   │   └── tasks.py         # Task CRUD endpoints
│   │   ├── middleware/
│   │   │   ├── __init__.py
│   │   │   └── auth.py          # JWTBearer class for token verification
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   └── task_service.py  # Business logic for task operations
│   │   └── database.py          # Database connection and session management
│   └── db/
│       ├── __init__.py
│       └── migrations/          # Alembic migrations (optional)
├── tests/
│   ├── __init__.py
│   ├── conftest.py              # pytest fixtures
│   ├── test_auth.py             # Authentication tests
│   ├── test_tasks.py            # Task CRUD tests
│   └── test_security.py         # Security and isolation tests
├── .env
├── pyproject.toml
├── requirements.txt
└── Dockerfile

# Root level
docker-compose.yml                # Local development orchestration
.gitignore
README.md
```

**Structure Decision**: Selected **Option 2: Web application** because the feature explicitly requires "full-stack web application" with separate frontend (Next.js) and backend (FastAPI) services. The monorepo structure aligns with Constitution Principle III (Monorepo Architecture) and enables independent development, testing, and deployment of each service while maintaining a single source repository.

## Website UI Guidelines

### Responsive Design
- Mobile-first approach with responsive breakpoints
- Support for mobile, tablet, and desktop viewports
- Touch-friendly controls and adequate tap targets
- Responsive navigation patterns

### Accessibility (a11y)
- Semantic HTML structure
- Proper heading hierarchy (h1, h2, h3, etc.)
- ARIA labels and roles where appropriate
- Keyboard navigation support
- Sufficient color contrast ratios
- Focus indicators for interactive elements

### User Experience (UX)
- Clear visual hierarchy and information architecture
- Consistent design patterns throughout the application
- Loading states and skeleton screens for better perceived performance
- Form validation with clear error messaging
- Confirmation dialogs for destructive actions (deletion)
- Success feedback for user actions

### Navigation
- Intuitive navigation with clear breadcrumbs
- Consistent header/navigation across pages
- Proper handling of authentication state in navigation
- Back button support and browser history management

### Forms
- Input validation with immediate feedback
- Clear labeling of form fields
- Appropriate input types for different data (email, password, etc.)
- Loading states during form submission
- Error handling and recovery

### Error Handling
- Graceful error states and recovery options
- User-friendly error messages
- Proper 404 and 500 error pages
- Network error handling with retry mechanisms

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

*No violations detected* - Constitution Check passed all principles. This section is intentionally left empty as there are no violations requiring justification.

---

## Phase 0: Research & Technology Decisions

### Research Tasks

**R-001: Better Auth JWT Plugin Configuration**
- **Question**: How to configure Better Auth v1.x with jwtClient() plugin for JWT token generation?
- **Research Areas**:
  - Better Auth installation and setup
  - jwtClient plugin API and configuration options
  - JWT token structure and claims (user_id, exp)
  - Token retrieval and storage patterns

**R-002: FastAPI JWT Verification with python-jose**
- **Question**: How to implement stateless JWT verification in FastAPI using python-jose?
- **Research Areas**:
  - python-jose library for HS256 algorithm
  - HTTPBearer security scheme in FastAPI
  - Dependency injection for JWT verification
  - Extracting user_id from token claims

**R-003: Neon PostgreSQL Connection Patterns**
- **Question**: What are the best practices for connecting FastAPI + SQLModel to Neon Serverless PostgreSQL?
- **Research Areas**:
  - Connection string format for Neon (postgresql+psycopg)
  - SQLModel engine configuration
  - Connection pooling for serverless environments
  - Environment variable management

**R-004: Next.js App Router Authentication Patterns**
- **Question**: How to implement authentication in Next.js App Router with Better Auth?
- **Research Areas**:
  - Server vs client components for auth
  - Protecting routes with middleware
  - Session persistence across page loads
  - Redirects for unauthenticated users

**R-005: API Client Token Interceptor Pattern**
- **Question**: Best pattern for automatically attaching Bearer tokens to all frontend API requests?
- **Research Areas**:
  - Fetch API wrapper with token injection
  - Error handling for 401 Unauthorized
  - Token refresh flows (if applicable)
  - TypeScript types for API responses

**R-006: SQLModel Table Creation and Migrations**
- **Question**: How to create tables and manage schema changes with SQLModel?
- **Research Areas**:
  - SQLModel.metadata.create_all() for initial setup
  - Alembic integration for migrations (optional)
  - Foreign key relationships (tasks.user_id -> users.id)
  - Index creation for performance

### Consolidated Research Findings

*(To be generated in research.md by Phase 0)*

---

## Phase 1: Design & Contracts

### Data Model

*(To be generated in data-model.md)*

**Entities**:
- User (managed by Better Auth)
- Task (owned by user, with CRUD operations)

### API Contracts

*(To be generated in contracts/ directory)*

**REST Endpoints**:
- GET /api/{user_id}/tasks
- POST /api/{user_id}/tasks
- GET /api/{user_id}/tasks/{id}
- PUT /api/{user_id}/tasks/{id}
- DELETE /api/{user_id}/tasks/{id}
- PATCH /api/{user_id}/tasks/{id}/complete

**Schemas**: Request/response models for all endpoints

### Quickstart Guide

*(To be generated in quickstart.md)*

**Setup Steps**:
1. Clone repository
2. Install frontend dependencies (npm install)
3. Install backend dependencies (uv sync or pip install -r requirements.txt)
4. Configure environment variables (.env.local and .env)
5. Run database migrations
6. Start backend (uvicorn main:app --reload)
7. Start frontend (npm run dev)
8. Access application (http://localhost:3000)

---

## Implementation Phases (Post-Planning)

**Note**: The following phases are executed by subsequent commands, not by `/sp.plan`:

### Phase 2: Task Breakdown (`/sp.tasks`)
- Generate tasks.md with specific Task IDs
- Map tasks to plan sections
- Define acceptance criteria for each task

### Phase 3: Implementation (`/sp.implement`)
- Execute tasks in dependency order
- Reference Task IDs in all code commits
- Run tests for each completed task
- Update documentation as needed

---

**Plan Status**: Phase 0 (Research) and Phase 1 (Design) artifacts to be generated next.
**Next Command**: Continue with Phase 0 research generation (internal to /sp.plan).
