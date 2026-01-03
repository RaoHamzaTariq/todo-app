## Phase II: Full-Stack Todo Web Application

### Objective

In Phase II, the goal is to transform the existing **console-based Todo application** into a **modern, multi-user full-stack web application** with **persistent storage**, using **Claude Code** and **Spec-Kit Plus**.

---

## Development Approach

You must strictly follow the **Agentic Development Stack workflow**:

1. Write specifications
2. Generate an implementation plan
3. Break the plan into tasks
4. Implement using **Claude Code only**

⚠️ **Manual coding is not allowed.**
Each phase—including prompts, iterations, and implementation steps—will be reviewed and evaluated.

---

## Functional Requirements

* Implement **all 5 Basic Level Todo features** as a web application
* Expose functionality via **RESTful API endpoints**
* Build a **responsive frontend UI**
* Persist data using **Neon Serverless PostgreSQL**
* Implement **user authentication** (signup/signin) using **Better Auth**

---

## Technology Stack

| Layer                   | Technology                  |
| ----------------------- | --------------------------- |
| Frontend                | Next.js 16+ (App Router)    |
| Backend                 | Python FastAPI              |
| ORM                     | SQLModel                    |
| Database                | Neon Serverless PostgreSQL  |
| Spec-Driven Development | Claude Code + Spec-Kit Plus |
| Authentication          | Better Auth                 |

---

## REST API Endpoints

| Method | Endpoint                             | Description            |
| ------ | ------------------------------------ | ---------------------- |
| GET    | `/api/{user_id}/tasks`               | List all tasks         |
| POST   | `/api/{user_id}/tasks`               | Create a new task      |
| GET    | `/api/{user_id}/tasks/{id}`          | Get task details       |
| PUT    | `/api/{user_id}/tasks/{id}`          | Update a task          |
| DELETE | `/api/{user_id}/tasks/{id}`          | Delete a task          |
| PATCH  | `/api/{user_id}/tasks/{id}/complete` | Toggle task completion |

---

## Securing the REST API

### Challenge

Better Auth runs on the **Next.js frontend**, while the **FastAPI backend** is a separate service. The backend must reliably identify which authenticated user is making each API request.

---

## Solution: JWT-Based Authentication

Better Auth will be configured to issue **JWT (JSON Web Tokens)** upon user login.

### Authentication Flow

1. User logs in via frontend
2. Better Auth creates a session and issues a JWT
3. Frontend sends API requests with:
   `Authorization: Bearer <JWT>`
4. Backend verifies the JWT signature using a shared secret
5. Backend extracts user details from the token
6. Backend ensures the user ID in the token matches the requested data
7. Backend returns **only the authenticated user’s tasks**

---

## Required Changes

### Component-Level Updates

| Component           | Required Changes                            |
| ------------------- | ------------------------------------------- |
| Better Auth Config  | Enable JWT token issuance                   |
| Frontend API Client | Attach JWT token to all requests            |
| FastAPI Backend     | Add JWT verification middleware             |
| API Routes          | Filter all queries by authenticated user ID |

🔐 **Important:**
Both frontend and backend must share the same JWT secret, typically set via the environment variable:

```
BETTER_AUTH_SECRET
```

---

## Security Benefits

| Benefit                  | Description                                     |
| ------------------------ | ----------------------------------------------- |
| User Isolation           | Users only access their own tasks               |
| Stateless Auth           | Backend does not rely on frontend sessions      |
| Token Expiry             | JWTs automatically expire (e.g., 7 days)        |
| Independent Verification | Frontend and backend validate tokens separately |

---

## API Behavior After Authentication

* All endpoints require a valid JWT
* Requests without a token return **401 Unauthorized**
* Every operation enforces task ownership
* Users can only view or modify their own tasks

✅ **Key Point:**
API endpoints remain unchanged, but **JWT authentication is now mandatory**, and responses are always user-scoped.

---

## Monorepo Organization with Spec-Kit + Claude Code

This project uses a **monorepo** structure to allow Claude Code and Spec-Kit Plus to work seamlessly across frontend and backend.

### Folder Structure

```
hackathon-todo/
├── .spec-kit/
│   └── config.yaml
├── specs/
│   ├── overview.md
│   ├── architecture.md
│   ├── features/
│   │   ├── task-crud.md
│   │   ├── authentication.md
│   │   └── chatbot.md
│   ├── api/
│   │   ├── rest-endpoints.md
│   │   └── mcp-tools.md
│   ├── database/
│   │   └── schema.md
│   └── ui/
│       ├── components.md
│       └── pages.md
├── CLAUDE.md
├── frontend/
│   └── CLAUDE.md
├── backend/
│   └── CLAUDE.md
├── docker-compose.yml
└── README.md
```

---

## Spec-Kit Configuration (`.spec-kit/config.yaml`)

```yaml
name: hackathon-todo
version: "1.0"

structure:
  specs_dir: specs
  features_dir: specs/features
  api_dir: specs/api
  database_dir: specs/database
  ui_dir: specs/ui

phases:
  - name: phase1-console
    features: [task-crud]
  - name: phase2-web
    features: [task-crud, authentication]
  - name: phase3-chatbot
    features: [task-crud, authentication, chatbot]
```

---

## CLAUDE.md Usage

### Root `CLAUDE.md`

* Provides project overview
* Explains how to reference and use specs
* Defines development workflow

### Frontend `CLAUDE.md`

* Next.js App Router guidelines
* API client usage
* Component and styling conventions

### Backend `CLAUDE.md`

* FastAPI project structure
* Database and ORM usage
* API and error-handling conventions

---

## Example Spec Highlights

### Task CRUD Feature

* Create, read, update, delete tasks
* Tasks belong to the authenticated user
* Support task completion status

### Database Schema

* `users` table (managed by Better Auth)
* `tasks` table linked by `user_id`
* Indexed fields for performance

---

## Spec-Driven Workflow

1. Write or update a spec file
2. Ask Claude Code to implement the spec
3. Claude Code reads:

   * Root `CLAUDE.md`
   * Relevant feature, API, and DB specs
   * Frontend and backend guidelines
4. Claude Code implements across the stack
5. Test and iterate by updating specs

---

## Monorepo Recommendation

**Use a monorepo for the hackathon.**

### Benefits

* Single Claude Code context
* Easier cross-stack changes
* Clear separation of frontend and backend
* Structured, referenceable specs

---

### Final Takeaway

Spec-Kit Plus defines **what to build**.
`CLAUDE.md` files define **how to build it**.
Claude Code uses both to implement the system **end-to-end without manual coding**.