---
id: "0001"
title: "Phase 2 constitution update"
stage: "constitution"
date: "2026-01-03"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "none"
branch: "main"
user: "Claude Code user"
command: "/sp.constitution"
labels: [constitution,governance,phase2]
links:
  spec: "null"
  ticket: "null"
  adr: "null"
  pr: "null"
files:
  - ".specify/memory/constitution.md"
tests:
  - "N/A"
---

## Prompt

to update the project governance for Phase 2: Full-Stack Web Evolution.

Incorporate these mandatory Phase 2 Laws:

Architectural Mandate: The project is now a Monorepo. All logic must be strictly separated into /frontend (Next.js 16+) and /backend (FastAPI).

Persistence Law: In-memory storage is now forbidden. All data must persist in Neon Serverless PostgreSQL using SQLModel as the ORM.

The Multi-User Security Law: > - Every task must be owned by a user_id.

No API endpoint shall return or modify data without verifying the user_id against a valid JWT.

Shared secrets for JWT must be managed via environment variables (BETTER_AUTH_SECRET).

Authentication Law: User management (signup/signin) must be handled by Better Auth on the frontend. The backend must verify these sessions via the JWT plugin.

API Standards: All endpoints must follow the RESTful pattern: /api/{user_id}/tasks/.

Spec-Driven Enforcement: No code changes in /frontend or /backend are permitted unless they map directly to a verified specification in the /specs directory.

Constraint: The CLI from Phase 1 is now deprecated in favor of the Web UI, but core business logic should remain modular to support future interfaces.

## Response snapshot

Updated constitution from v1.1.0 to v2.0.0 with Phase 2 governance laws:

- Added Principle III (Monorepo Architecture) - frontend/backend separation
- Added Principle VI (Multi-User Security) - user_id ownership + JWT verification
- Added Principle VII (Authentication) - Better Auth frontend, JWT plugin backend
- Added Principle VIII (API Standards) - RESTful /api/{user_id}/tasks/ pattern
- Replaced Principle III (In-Memory) with Principle IX (Persistence Law - Neon PostgreSQL + SQLModel)
- Replaced Principle IV (Core Feature Focus) with Principle X (Web-First Architecture - CLI deprecated)
- Updated Technology Stack Constraints section with full Phase 2 stack
- Updated Development Workflow with spec-driven enforcement and JWT error handling

## Outcome

- ✅ Impact: Major governance update - Phase 2 Full-Stack Web Evolution
- 🧪 Tests: N/A
- 📁 Files: 1 file modified (.specify/memory/constitution.md)
- 🔁 Next prompts: /sp.specify for new features, /sp.plan for implementation
- 🧠 Reflection: Fundamental architectural shift from CLI to web, in-memory to PostgreSQL, single-user to multi-user

## Evaluation notes (flywheel)

- Failure modes observed: N/A
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
