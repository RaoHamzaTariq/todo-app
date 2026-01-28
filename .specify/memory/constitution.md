<!--
Sync Impact Report:
- Version change: 3.0.0 -> 4.0.0 (MAJOR: fundamental shift to Cloud-Native Kubernetes deployment with Minikube, Helm, AI-assisted DevOps)
- Added principles:
  - XVIII. Kubernetes Deployment Law (Minikube, Helm Charts, containerization)
  - XIX. AI-Assisted DevOps Law (Docker AI Gordon, kubectl-ai, kagent usage)
  - XX. Cloud-Native Architecture Law (container-first, service mesh, resilience)
  - XXI. Infrastructure as Code Law (Helm charts, YAML manifests, version control)
  - XXII. Local-Only Deployment Law (Minikube constraint, no cloud assumptions)
- Updated sections: Technology Stack Constraints (added Kubernetes, Helm, Minikube, AI DevOps tools), Development Workflow (added containerization and deployment validation)
- Templates requiring updates:
  - .specify/templates/plan-template.md (✅ Need to add K8s/IaC considerations)
  - .specify/templates/spec-template.md (✅ Need to add K8s requirements)
  - .specify/templates/tasks-template.md (✅ Need to add deployment-related tasks)
- Templates validated: phr-template.md (aligned)
- Follow-up TODOs: None
-->
# Cloud-Native Todo Chatbot Constitution

## Core Principles

### I. Spec-Driven Development (SDD)

All development MUST follow the SDD workflow sequence: `/sp.specify` -> `/sp.plan` -> `/sp.tasks` -> `/sp.implement`. This ensures traceable, aligned development in the cloud-native context. This principle remains unchanged but now applies to infrastructure as well as application code.

**Law 1 - No Pre-Task Code Generation:**
- Never write a single line of code before the `/sp.tasks` file is finalized and exists
- If implementation is requested but `specs/<feature>/tasks.md` does not exist -> **BLOCK** and guide user to complete the SDD workflow
- This applies to both application code and infrastructure definitions

**Law 2 - Task Reference Mandate:**
- Every code implementation MUST reference a specific Task ID from the corresponding `specs/<feature>/tasks.md`
- Code comments and PR descriptions must include: `# SDD: Implements Task ID: T-XXX`
- If user asks for code without task context -> **BLOCK** and require task ID specification

**Law 3 - Constitution Pre-Check:**
- Before any feature work, check if it exists in `.specify/memory/constitution.md`
- If feature violates constitutional principles -> **BLOCK** and surface the conflict
- If feature is not addressed in constitution -> Suggest running `/sp.constitution` to add guidance

### II. Python 3.13+ Standard (Backend Only)

Use Python 3.13+ with strict type hinting, PEP 8 standards, and functional programming principles where applicable. Leverage `uv` for package management to ensure consistent dependency handling. This applies to the `/backend` directory only. Containerized applications must maintain these standards within Kubernetes deployments.

### III. Monorepo Architecture

The project MUST be structured as a Monorepo with strict separation between frontend and backend, now extended to include infrastructure definitions in Kubernetes-compatible formats:

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

**Infrastructure (`/k8s`, `/helm`):**
- Kubernetes manifests and Helm charts
- Container images for all services
- Service discovery and networking configurations
- Resource allocation and scaling policies

**Separation Rules:**
- No business logic in frontend components
- No UI code in backend services
- All data flow through API contracts
- Infrastructure definitions separate from application code
- Each directory has independent package management

### IV. Code Quality Standards

Maintain strict type hinting, PEP 8 compliance, and functional programming principles for application code. For infrastructure, maintain clean, well-documented, and testable YAML/JSON manifests. Backend uses Python type hints; frontend uses TypeScript; infrastructure uses properly structured Kubernetes resources and Helm templates with schema validation where possible.

### V. Task ID Requirement

Every code change MUST be associated with a specific Task ID from the tasks.md file. This ensures traceability and prevents unauthorized feature creep. All implementations must include a comment: `# SDD: Implements Task ID: T-XXX`. This applies to application code, infrastructure definitions, and deployment configurations alike.

### VI. Multi-User Security Law

**Data Ownership:**
- Every task MUST be owned by a `user_id`
- Tasks cannot be accessed or modified without verifying ownership

**JWT Verification:**
- No API endpoint shall return or modify data without verifying the `user_id` against a valid JWT
- Shared secrets for JWT MUST be managed via Kubernetes Secrets (`BETTER_AUTH_SECRET`)
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

All endpoints MUST follow the RESTful pattern in the Kubernetes deployment context:

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
- All data MUST persist in Neon Serverless PostgreSQL or Kubernetes PersistentVolumes

**ORM Requirement:**
- Use SQLModel as the ORM for database operations
- Define entities using SQLModel declarative syntax
- Leverage SQLModel's Pydantic integration for validation

**Connection Management:**
- Use Kubernetes Secrets for database credentials
- Connection pooling configured for serverless/containerized environment
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

### XI. AI Agent Architecture Law

**OpenAI Agents SDK Integration:**
- All AI functionality MUST use the OpenAI Agents SDK
- Natural language processing for task management is the primary AI use case
- Agent design must follow the patterns: agents, handoffs, guardrails, sessions, and tracing

**Agent Behavior Requirements:**
- Agents must use MCP tools exclusively for task operations
- Never modify tasks directly without using MCP tools
- Always confirm actions in natural language to users
- Handle errors gracefully and ask for clarification when ambiguous

### XII. MCP (Model Context Protocol) Tools Law

**MCP Tool Requirements:**
- Task operations MUST be exposed as MCP tools for AI agents
- MCP tools must follow the specified schema: `add_task`, `list_tasks`, `complete_task`, `delete_task`, `update_task`
- MCP tools MUST validate `user_id` for data ownership
- MCP tools MAY access database but MUST NOT store session state
- MCP tools MUST NOT call OpenAI directly

**Tool Schema Compliance:**
- `add_task`: { "user_id": "string", "title": "string", "description": "string?" }
- `list_tasks`: { "user_id": "string", "status": "all | pending | completed" }
- `complete_task`: { "user_id": "string", "task_id": 3 }
- `delete_task`: { "user_id": "string", "task_id": 2 }
- `update_task`: { "user_id": "string", "task_id": 1, "title": "string?", "description": "string?" }

### XIII. Stateless Architecture Law

**Server Statelessness:**
- Server stores NO memory or session state
- Conversation context MUST be rebuilt from database every request
- Runtime state MUST be discarded after each request (Rule 9 in flow)
- All state persisted in database (tasks, conversations, messages)

**State Recovery:**
- System MUST be restart-safe
- Conversation context MUST be resumable after server restart
- No reliance on in-memory caches for critical state

### XIV. Chat API Standards

**Endpoint Pattern:**
- `POST /api/{user_id}/chat` - Primary chat endpoint (stateless)
- Request: { "conversation_id": 12, "message": "Add a task to buy groceries" }
- Response: { "conversation_id": 12, "response": "✅ I've added 'Buy groceries' to your tasks.", "tool_calls": [...] }

**Chat Flow Requirements:**
- Fetch conversation history from DB (Step 2)
- Append and save user message (Steps 3-4)
- Run agent with full history (Step 5)
- Agent invokes MCP tool(s) (Step 6)
- Save assistant message (Step 7)
- Return response and discard runtime state (Steps 8-9)

### XV. Conversation Context Management

**Database Models:**
- **Task Model**: id, user_id, title, description, completed, created_at, updated_at
- **Conversation Model**: id, user_id, created_at, updated_at
- **Message Model**: id, conversation_id, user_id, role (user | assistant), content, created_at

**Context Persistence:**
- All conversation history stored in database
- Messages linked to conversations and users
- Conversation context rebuilt from DB for each request

### XVI. Constitution Compliance Enforcement

Before saving any code or infrastructure definition:
1. Verify implementation does not violate `.specify/memory/constitution.md` principles
2. Confirm code follows defined code standards
3. Ensure no secrets hardcoded (uses Kubernetes Secrets per constitution)
4. Validate implementation is the smallest viable change
5. Check code includes proper file references and Task ID comment

### XVII. Smallest Viable Change

All implementations must be the smallest viable change per task requirements. Avoid refactoring unrelated code, adding premature features, or making architectural changes outside the planned scope. Changes should be focused, testable, and directly address the Task ID. This applies equally to application code and infrastructure definitions.

### XVIII. Kubernetes Deployment Law

**Local-Only Deployment Constraint:**
- All deployments MUST be local using Minikube only
- No cloud provider assumptions or dependencies allowed
- All configurations MUST work in isolated local environments
- External dependencies MUST be containerized and deployed locally

**Containerization Requirements:**
- All services MUST be packaged as Docker containers using AI-assisted tools (Docker AI Gordon)
- Images MUST be built from generated Dockerfiles with minimal base images
- Container images MUST be optimized for size and security
- All services MUST run in containers within Kubernetes

**Kubernetes Resources:**
- Services MUST be deployed using Helm Charts with configurable parameters
- Deployments MUST include proper resource limits and requests
- Health checks MUST be implemented for all services
- Service-to-service communication MUST use Kubernetes Services

### XIX. AI-Assisted DevOps Law

**Tool Usage Guidelines:**
- Docker AI Gordon MUST be used for containerization (Dockerfile generation)
- kubectl-ai MUST be used for Kubernetes operations via natural language commands
- kagent MUST be used for intelligent Kubernetes resource management
- All DevOps operations SHOULD prioritize AI-assisted tools over manual commands

**Operational Procedures:**
- Deployment operations MUST use AI-assisted tools where available
- Monitoring and debugging SHOULD leverage AI tools for faster diagnosis
- Scaling operations MUST be performed using AI-assisted commands
- Configuration changes SHOULD be applied through AI tools when possible

**Conflict Resolution:**
- When multiple AI tools provide conflicting recommendations, defer to kubectl-ai as authoritative source
- Manual overrides of AI tool suggestions MUST be documented with rationale
- AI tool errors MUST be escalated to human operators with clear error context

### XX. Cloud-Native Architecture Law

**Container-First Design:**
- All services MUST be designed for containerized deployment
- Applications MUST be stateless with externalized configuration
- Services MUST be horizontally scalable without shared state
- Applications MUST handle graceful shutdown and startup

**Service Mesh Considerations:**
- Internal service communication MUST use Kubernetes Services
- Load balancing MUST be handled by Kubernetes
- Service discovery MUST use Kubernetes DNS
- Traffic management SHOULD leverage Kubernetes networking features

**Resilience Patterns:**
- Applications MUST implement circuit breaker patterns
- Retry logic MUST be configurable and bounded
- Deadlock prevention MUST be implemented in distributed operations
- Failover mechanisms MUST be tested and validated

### XXI. Infrastructure as Code Law

**Helm Chart Standards:**
- Each service MUST have its own Helm chart with proper templating
- Values files MUST be separated for different environments
- Templates MUST use proper Kubernetes resource definitions
- Charts MUST include proper dependency management and versioning

**Manifest Management:**
- All Kubernetes resources MUST be defined in version-controlled YAML/JSON
- Manual edits to live resources MUST be avoided
- Drift detection SHOULD be implemented to monitor configuration consistency
- Rollback capabilities MUST be maintained for all deployments

**Configuration Management:**
- Application configuration MUST be externalized via ConfigMaps and Secrets
- Sensitive data MUST be stored in Kubernetes Secrets only
- Environment-specific configurations MUST use Helm value overrides
- Configuration changes MUST follow the same SDD workflow as code changes

### XXII. Local-Only Deployment Law

**Minikube Constraint:**
- All deployments MUST target Minikube only
- No assumptions about cloud provider services allowed
- External dependencies MUST be deployed locally within Minikube
- Network configurations MUST work in isolated Minikube environment

**No Cloud Assumptions:**
- No cloud-specific APIs or services allowed
- No cloud provider SDKs or libraries in application code
- All infrastructure components MUST be deployable locally
- Storage, networking, and compute MUST use Kubernetes-native resources

**Environment Parity:**
- Development and deployment environments MUST be identical
- All team members MUST be able to replicate the exact same deployment
- No "works on my machine" scenarios allowed
- Deployment process MUST be deterministic and repeatable

## Technology Stack Constraints

**Frontend:**
- Next.js 16+
- TypeScript
- Better Auth for authentication
- Custom chatbot UI (Tailwind CSS)

**Backend:**
- Python 3.13+
- FastAPI
- SQLModel
- Neon Serverless PostgreSQL
- OpenAI Agents SDK
- Official MCP SDK

**Cloud-Native Infrastructure:**
- Kubernetes v1.28+
- Minikube for local deployment
- Helm v3+ for package management
- Docker for containerization
- Docker AI Gordon for AI-assisted Dockerfile creation
- kubectl-ai for AI-assisted Kubernetes operations
- kagent for intelligent Kubernetes resource management

**Shared:**
- JWT for authentication tokens
- `uv` for Python package management
- Kubernetes Secrets for sensitive data (`BETTER_AUTH_SECRET`, database credentials)
- Kubernetes ConfigMaps for non-sensitive configuration

## Development Workflow

All development must follow the SDD sequence: Specify -> Plan -> Tasks -> Implement. The agent must reject any request to implement code that hasn't been through the `/sp.plan` and `/sp.tasks` phase. This now includes infrastructure changes alongside application code changes.

### Spec-Driven Enforcement

No code changes in `/frontend`, `/backend`, or infrastructure directories are permitted unless they map directly to a verified specification in the `/specs` directory. Every implementation must reference a task from `specs/<feature>/tasks.md`.

### Pre-Implementation Checklist

Before writing any application code or infrastructure definitions:
1. Read the specific task from tasks.md
2. Read constitution.md
3. Run "Constitution Alignment Check":
   - Does this implementation violate any principle?
   - Does it follow code standards?
   - Is it the smallest viable change?
   - Does it follow API standards?
   - Is JWT verification implemented where required?
   - Does it comply with stateless architecture?
   - Does it use MCP tools for task operations?
   - Does it follow Kubernetes deployment constraints?
   - Does it use AI-assisted DevOps tools where applicable?
   - Does it comply with local-only deployment requirements?
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
| Direct task modification bypassing MCP | Block and require MCP tool usage |
| Session state storage on server | Block and require database persistence |
| Violates local-only deployment constraint | Block and require Minikube-compliant approach |
| Bypasses AI-assisted DevOps tools | Block and require AI tool usage |
| Hardcoded secrets instead of Kubernetes Secrets | Block and require proper secret management |

## Governance

All development must comply with the SDD principles. Amendments to this constitution require explicit approval. All pull requests must verify compliance with these principles before merging. Code reviews must check for proper Task ID references. Infrastructure changes must follow the same governance as application code changes, with additional validation for Kubernetes best practices and security requirements.

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
5. Code reviews - Verify Task ID comments, JWT verification, MCP usage, K8s compliance, and principle adherence

**Version**: 4.0.0 | **Ratified**: 2026-01-24 | **Last Amended**: 2026-01-24
