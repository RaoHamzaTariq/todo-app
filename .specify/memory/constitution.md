<!--
Sync Impact Report:
- Version change: 1.1.0 -> 2.0.0 (MAJOR: fundamental architecture and persistence changes)
- Replaced principles:
  - III. In-Memory Storage -> IX. Persistence Law (Neon PostgreSQL + SQLModel)
  - IV. Core Feature Focus -> X. Web-First Architecture (CLI deprecated)
- Added principles:
  - III. Monorepo Architecture (Frontend/Backend separation)
  - VI. Multi-User Security (user_id ownership + JWT verification)
  - VII. Authentication (Better Auth + JWT plugin)
  - VIII. API Standards (/api/{user_id}/tasks/ pattern)
- Updated sections: Technology Stack Constraints, Development Workflow
- Templates requiring updates:
  - .specify/templates/plan-template.md (✅ Structure section already flexible)
  - .specify/templates/spec-template.md (✅ Already technology-agnostic)
  - .specify/templates/tasks-template.md (✅ Already references plan structure)
- Templates validated: phr-template.md (aligned)
- Follow-up TODOs: None
-->
# Todo Application Constitution

## Core Principles

### I. Spec-Driven Development (SDD)

All development MUST follow the SDD workflow sequence: `/sp.specify` -> `/sp.plan` -> `/sp.tasks` -> `/sp.implement`. This ensures traceable, aligned development.

**Law 1 - No Pre-Task Code Generation:**
- Never write a single line of code before the `/sp.tasks` file is finalized and exists
- If implementation is requested but `specs/<feature>/tasks.md` does not exist -> **BLOCK** and guide user to complete the SDD workflow

**Law 2 - Task Reference Mandate:**
- Every code implementation MUST reference a specific Task ID from the corresponding `specs/<feature>/tasks.md`
- Code comments and PR descriptions must include: `# SDD: Implements Task ID: T-XXX`
- If user asks for code without task context -> **BLOCK** and require task ID specification

**Law 3 - Constitution Pre-Check:**
- Before any feature work, check if it exists in `.specify/memory/constitution.md`
- If feature violates constitutional principles -> **BLOCK** and surface the conflict
- If feature is not addressed in constitution -> Suggest running `/sp.constitution` to add guidance

### II. Python 3.13+ Standard (Backend Only)

Use Python 3.13+ with strict type hinting, PEP 8 standards, and functional programming principles where applicable. Leverage `uv` for package management to ensure consistent dependency handling. This applies to the `/backend` directory only.

### III. Monorepo Architecture

The project MUST be structured as a Monorepo with strict separation between frontend and backend:

**Frontend (`/frontend`):**
- Next.js 16+ application
- Handles UI rendering and user interaction
- Manages authentication via Better Auth
- Communicates with backend via REST API

**Backend (`/backend`):**
- FastAPI application
- Provides REST API endpoints
- Manages data persistence in Neon PostgreSQL
- Validates JWT tokens from frontend authentication

**Separation Rules:**
- No business logic in frontend components
- No UI code in backend services
- All data flow through API contracts
- Each directory has independent package management

### IV. Code Quality Standards

Maintain strict type hinting, PEP 8 compliance, and functional programming principles. All code must be clean, well-documented, and testable. Backend uses Python type hints; frontend uses TypeScript.

### V. Task ID Requirement

Every code change MUST be associated with a specific Task ID from the tasks.md file. This ensures traceability and prevents unauthorized feature creep. All implementations must include a comment: `# SDD: Implements Task ID: T-XXX`.

### VI. Multi-User Security Law

**Data Ownership:**
- Every task MUST be owned by a `user_id`
- Tasks cannot be accessed or modified without verifying ownership

**JWT Verification:**
- No API endpoint shall return or modify data without verifying the `user_id` against a valid JWT
- Shared secrets for JWT MUST be managed via environment variables (`BETTER_AUTH_SECRET`)
- Backend MUST validate JWT signature and expiration on every protected request

**Access Control:**
- Users can only access their own tasks
- API responses must not leak other users' data
- Authentication errors must not reveal sensitive information

### VII. Authentication Law

**Frontend (Better Auth):**
- User management (signup/signin) MUST be handled by Better Auth on the frontend
- Better Auth handles session lifecycle and token refresh
- JWT tokens are issued to authenticated users

**Backend (JWT Verification):**
- Backend MUST verify sessions via the JWT plugin
- All protected endpoints require valid JWT token in Authorization header
- Backend trusts JWT claims from authenticated frontend sessions

**Token Requirements:**
- JWT tokens MUST include `user_id` claim
- Token expiration MUST be enforced
- Invalid tokens MUST return 401 Unauthorized

### VIII. API Standards

All endpoints MUST follow the RESTful pattern:

**URL Structure:**
- `/api/{user_id}/tasks/` - Base endpoint for user tasks
- `/api/{user_id}/tasks/{task_id}` - Specific task operations

**HTTP Methods:**
- `GET /api/{user_id}/tasks/` - List user's tasks
- `POST /api/{user_id}/tasks/` - Create new task
- `GET /api/{user_id}/tasks/{task_id}` - Get specific task
- `PUT /api/{user_id}/tasks/{task_id}` - Update task
- `DELETE /api/{user_id}/tasks/{task_id}` - Delete task

**Response Format:**
- Success responses include task data with `user_id`
- Error responses include appropriate status codes and messages
- No data leakage between users

### IX. Persistence Law

**Storage Requirement:**
- In-memory storage is FORBIDDEN
- All data MUST persist in Neon Serverless PostgreSQL

**ORM Requirement:**
- Use SQLModel as the ORM for database operations
- Define entities using SQLModel declarative syntax
- Leverage SQLModel's Pydantic integration for validation

**Connection Management:**
- Use environment variables for database credentials
- Connection pooling configured for serverless environment
- Proper resource cleanup on application shutdown

### X. Web-First Architecture

**CLI Deprecation:**
- The CLI from Phase 1 is now DEPRECATED in favor of the Web UI
- Core business logic MUST remain modular to support future interfaces
- Business rules should be in shared libraries, not tied to interface

**Modularity Requirements:**
- Core business logic in `/backend/src/services/` or `/backend/src/lib/`
- Reusable components accessible by any interface (Web, CLI, API)
- Data models independent of presentation layer

### XI. Constitution Compliance Enforcement

Before saving any code:
1. Verify implementation does not violate `.specify/memory/constitution.md` principles
2. Confirm code follows defined code standards
3. Ensure no secrets hardcoded (uses `.env` per constitution)
4. Validate implementation is the smallest viable change
5. Check code includes proper file references and Task ID comment

### XII. Smallest Viable Change

All implementations must be the smallest viable change per task requirements. Avoid refactoring unrelated code, adding premature features, or making architectural changes outside the planned scope. Changes should be focused, testable, and directly address the Task ID.

## Technology Stack Constraints

**Frontend:**
- Next.js 16+
- TypeScript
- Better Auth for authentication

**Backend:**
- Python 3.13+
- FastAPI
- SQLModel
- Neon Serverless PostgreSQL

**Shared:**
- JWT for authentication tokens
- `uv` for Python package management
- Environment variables for secrets (`BETTER_AUTH_SECRET`, database credentials)

## Development Workflow

All development must follow the SDD sequence: Specify -> Plan -> Tasks -> Implement. The agent must reject any request to implement code that hasn't been through the `/sp.plan` and `/sp.tasks` phase.

### Spec-Driven Enforcement

No code changes in `/frontend` or `/backend` are permitted unless they map directly to a verified specification in the `/specs` directory. Every implementation must reference a task from `specs/<feature>/tasks.md`.

### Pre-Implementation Checklist

Before writing any code:
1. Read the specific task from tasks.md
2. Read constitution.md
3. Run "Constitution Alignment Check":
   - Does this implementation violate any principle?
   - Does it follow code standards?
   - Is it the smallest viable change?
   - Does it follow API standards?
   - Is JWT verification implemented where required?
4. If alignment fails -> **DO NOT SAVE** -> Surface violation with specific principle reference
5. If alignment passes -> Proceed with implementation

### Error Handling

| Condition | Action |
|-----------|--------|
| `tasks.md` missing | Redirect to `/sp.specify` -> `/sp.plan` -> `/sp.tasks` |
| `tasks.md` not finalized | Check for "Status: finalized", if absent request confirmation |
| No Task ID provided | Block and request specific Task ID |
| Task ID not found in `tasks.md` | Surface: "Task ID T-XXX not found in specs/<feature>/tasks.md" |
| Constitution conflict | Halt with principle citation and resolution requirement |
| Code fails alignment check | Do not save, surface violation, propose fix |
| No JWT verification on protected endpoint | Block and require JWT middleware |
| Missing `user_id` on task operations | Block and require user_id validation |

## Governance

All development must comply with the SDD principles. Amendments to this constitution require explicit approval. All pull requests must verify compliance with these principles before merging. Code reviews must check for proper Task ID references.

### Versioning Policy

- **MAJOR**: Backward incompatible governance/principle removals or redefinitions
- **MINOR**: New principle/section added or materially expanded guidance
- **PATCH**: Clarifications, wording, typo fixes, non-semantic refinements

### Compliance Review

Constitution compliance is verified at:
1. Feature specification phase (`/sp.specify`) - Validate scope against principles
2. Planning phase (`/sp.plan`) - Constitution Check before design
3. Task generation (`/sp.tasks`) - Ensure all tasks reference plan sections
4. Implementation (`/sp.implement`) - Task ID validation and alignment check
5. Code reviews - Verify Task ID comments, JWT verification, and principle adherence

**Version**: 2.0.0 | **Ratified**: 2025-12-28 | **Last Amended**: 2026-01-03
