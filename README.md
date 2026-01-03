# todo-app
Evolution of Todo App from Console to fully Agentic AI web application.


/sp.specify to generate the Master Specification for Phase 2: Full-Stack Web Evolution.

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