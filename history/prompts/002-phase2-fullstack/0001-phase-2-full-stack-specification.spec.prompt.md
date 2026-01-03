---
id: "0001"
title: "Phase 2 Full-Stack specification"
stage: "spec"
date: "2026-01-03"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "002-phase2-fullstack"
branch: "002-phase2-fullstack"
user: "Claude Code user"
command: "/sp.specify"
labels: [spec,phase2,fullstack,todo-app]
links:
  spec: "specs/002-phase2-fullstack/spec.md"
  ticket: "null"
  adr: "null"
  pr: "null"
files:
  - "specs/002-phase2-fullstack/spec.md"
  - "specs/002-phase2-fullstack/checklists/requirements.md"
tests:
  - "N/A"
---

## Prompt

to generate the Master Specification for Phase 2: Full-Stack Todo Application.

Instructions for the Agent: Activating Skill: hackathon-governor and Skill: monorepo-architect. This specification must serve as the source of truth for all subsequent /sp.plan and /sp.tasks commands.

1. Technical Scope
Backend: FastAPI (Python 3.13) with SQLModel and Neon PostgreSQL.

Frontend: Next.js 16+ (App Router) with Tailwind CSS.

Security: Implement the auth-security-specialist protocol using Better Auth and JWT verification.

2. Data Contract (Skill: data-ownership-enforcer)
Define the Task SQLModel with mandatory user_id string field.

Specify that every database transaction MUST be filtered by the user_id extracted from the JWT.

3. API Contract (Skill: api-contract-steward)
Explicitly define the 6 REST endpoints following the /api/{user_id}/tasks/ pattern.

Define the PATCH /complete logic specifically for status toggling.

4. Implementation Requirements (Skill: clean-code-pythonist)
Plan Phase Requirement: The plan must include a clear separation between database session management and API route logic.

Task Phase Requirement: Implementation must be broken down into:

Scaffolding the Monorepo folders.

Database engine and SQLModel setup.

JWT Middleware for FastAPI.

CRUD Route implementation.

Next.js API Client and Page layout.

5. Definition of Done
The application allows multiple users to sign up/in via Better Auth.

Users can only CRUD their own tasks in the Neon Database.

The UI is responsive and reflects real-time database state via the FastAPI backend.

## Response snapshot

Created Master Specification for Phase 2 Full-Stack Todo Application:

- 6 User Stories (P1: Auth, Create, View; P2: Update, Delete, Toggle)
- 12 Functional Requirements covering authentication, task CRUD, security, and data isolation
- 2 Key Entities (User, Task) with mandatory user_id on Task
- 6 Measurable Success Criteria (SC-001 to SC-006)
- Quality checklist validated with all items passing

Specification is technology-agnostic and ready for planning phase.

## Outcome

- ✅ Impact: Master specification for Phase 2 full-stack transformation
- 🧪 Tests: N/A (specification phase)
- 📁 Files: 2 files (spec.md, checklists/requirements.md)
- 🔁 Next prompts: /sp.plan for architecture, /sp.tasks for implementation
- 🧠 Reflection: Specification covers all 6 skills activated - monorepo structure, auth security, data ownership, API contracts, and Python backend patterns

## Evaluation notes (flywheel)

- Failure modes observed: N/A
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
