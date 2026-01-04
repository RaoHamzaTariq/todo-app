# Research: Phase 2 Full-Stack Todo Application

**Date**: 2026-01-04
**Phase**: 0 (Research & Technology Decisions)
**Plan Reference**: [plan.md](./plan.md)

## Research Summary

This document consolidates findings for all technology decisions required for Phase 2 implementation. All research tasks from plan.md have been resolved with concrete decisions, rationales, and alternative considerations.

---

## R-001: Better Auth JWT Plugin Configuration

### Decision

Use Better Auth v1.x with the `jwtClient()` plugin from `better-auth/plugins` for JWT token generation and management on the frontend.

### Configuration

```typescript
// frontend/src/lib/auth-client.ts
import { createAuthClient } from "better-auth/client";
import { jwtClient } from "better-auth/plugins";

export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
  plugins: [
    jwtClient({
      // Enable JWT token generation
      // Token automatically includes user_id and exp claims
    }),
  ],
});

// Usage: Retrieve token for API calls
const tokenData = await authClient.token();
const jwtToken = tokenData.token; // Bearer token string
```

### JWT Token Structure

```json
{
  "user_id": "clx123456789",
  "sub": "clx123456789",
  "exp": 1704470400,
  "iat": 1703865600
}
```

- `user_id`: User identifier (primary claim for backend verification)
- `sub`: Subject (standard JWT claim, same as user_id)
- `exp`: Expiration timestamp (Unix time)
- `iat`: Issued at timestamp

### Rationale

- **Better Auth Native**: jwtClient() is the official plugin for JWT token generation in Better Auth
- **Automatic Claims**: Plugin automatically includes required claims (user_id, exp) without manual configuration
- **Session Integration**: Seamlessly integrates with Better Auth session management
- **Token Refresh**: Handles token refresh logic internally when tokens approach expiration

### Alternatives Considered

| Alternative | Reason Rejected |
|-------------|-----------------|
| Custom JWT generation with jsonwebtoken | Better Auth provides this natively, no need for custom implementation |
| Session cookies only (no JWT) | Backend requires stateless verification; JWT enables this |
| OAuth2/OpenID Connect | Over-engineered for Phase 2 requirements; adds unnecessary complexity |

---

## R-002: FastAPI JWT Verification with python-jose

### Decision

Implement stateless JWT verification in FastAPI using `python-jose[cryptography]` library with HS256 algorithm.

### Implementation Pattern

```python
# backend/src/app/middleware/auth.py
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from datetime import datetime
import os

security_scheme = HTTPBearer()

class JWTBearer:
    """JWT verification middleware for FastAPI"""

    def __init__(self):
        self.secret = os.getenv("BETTER_AUTH_SECRET")
        if not self.secret:
            raise ValueError("BETTER_AUTH_SECRET environment variable not set")
        self.algorithm = "HS256"

    async def __call__(
        self,
        credentials: HTTPAuthorizationCredentials = Depends(security_scheme)
    ) -> dict:
        """
        Decode and verify JWT token.
        Returns payload with user_id if valid, raises 401 if invalid.
        """
        token = credentials.credentials

        try:
            # Decode JWT using shared secret
            payload = jwt.decode(
                token,
                self.secret,
                algorithms=[self.algorithm]
            )

            # Validate expiration (exp claim)
            exp = payload.get("exp")
            if exp and datetime.utcnow().timestamp() > exp:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token has expired",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            # Extract user_id from token
            user_id = payload.get("user_id") or payload.get("sub")
            if not user_id:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token: missing user_id",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            return {"user_id": user_id, "payload": payload}

        except JWTError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid token: {str(e)}",
                headers={"WWW-Authenticate": "Bearer"},
            )

# Create singleton instance
jwt_bearer = JWTBearer()
```

### Usage in Routes

```python
# backend/src/app/routers/tasks.py
from fastapi import APIRouter, Depends
from app.middleware.auth import jwt_bearer

router = APIRouter(prefix="/api", tags=["tasks"])

@router.get("/{user_id}/tasks")
async def list_tasks(
    user_id: str,
    auth_user: dict = Depends(jwt_bearer),
):
    """List tasks for authenticated user"""
    # Verify user_id from token matches path parameter
    if auth_user["user_id"] != user_id:
        raise HTTPException(status_code=403, detail="Access denied")

    # Fetch tasks using verified user_id
    tasks = await get_tasks_for_user(auth_user["user_id"])
    return {"tasks": tasks}
```

### Rationale

- **Stateless Verification**: No database lookup required for token validation
- **python-jose Standard**: Industry-standard library for JWT handling in Python
- **HS256 Algorithm**: Symmetric encryption suitable for single-tenant applications
- **FastAPI Native**: HTTPBearer and Depends() are FastAPI's idiomatic patterns
- **Error Handling**: Clear 401 responses with WWW-Authenticate header per RFC 6750

### Alternatives Considered

| Alternative | Reason Rejected |
|-------------|-----------------|
| PyJWT library | python-jose has better FastAPI integration and cryptography support |
| RS256 (asymmetric) algorithm | HS256 sufficient for single-secret setup; RS256 adds key management complexity |
| Database token validation | Violates stateless principle; adds latency and database load |
| Auth0/Clerk integration | Over-engineered for Phase 2; Better Auth sufficient |

---

## R-003: Neon PostgreSQL Connection Patterns

### Decision

Connect FastAPI + SQLModel to Neon Serverless PostgreSQL using `postgresql+psycopg` connection string with environment-based configuration.

### Connection Configuration

```python
# backend/src/app/database.py
from sqlmodel import create_engine, Session, SQLModel
from contextlib import contextmanager
import os

# Connection string from environment
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable not set")

# Create engine with serverless-optimized settings
engine = create_engine(
    DATABASE_URL,
    echo=True,  # Log SQL queries (disable in production)
    pool_pre_ping=True,  # Verify connections before use
    pool_recycle=3600,  # Recycle connections every hour
    connect_args={
        "server_settings": {"application_name": "todo-app-backend"}
    }
)

@contextmanager
def get_session():
    """Dependency for database sessions"""
    session = Session(engine)
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

# Initialize tables (for development)
def init_db():
    """Create all tables"""
    SQLModel.metadata.create_all(engine)
```

### Environment Variables

```env
# backend/.env
DATABASE_URL=postgresql+psycopg://username:password@ep-xyz-123456.us-east-1.neon.tech/todo_db?sslmode=require
BETTER_AUTH_SECRET=your-256-bit-secret-key
```

### Neon-Specific Considerations

- **Connection Pooling**: Use `pool_pre_ping=True` to handle serverless connection recycling
- **SSL Required**: Neon requires `sslmode=require` in connection string
- **Connection Limits**: Default poolsize=5 suitable for serverless; adjust for high concurrency
- **Regional Endpoint**: Use region-specific endpoint (us-east-1, eu-west-1, etc.)

### Rationale

- **psycopg (v3) Adapter**: Modern PostgreSQL adapter with async support (psycopg3)
- **Serverless Optimized**: pool_pre_ping and pool_recycle handle Neon's connection model
- **SQLModel Native**: create_engine() is SQLModel's standard approach
- **Environment Configuration**: Secrets never hardcoded, follows FR-012

### Alternatives Considered

| Alternative | Reason Rejected |
|-------------|-----------------|
| asyncpg adapter | SQLModel better supports psycopg; async not required for Phase 2 scope |
| SQLAlchemy directly | SQLModel provides cleaner Pydantic integration |
| Direct psycopg3 connection | SQLModel ORM provides type safety and validation |
| Connection string in code | Violates Constitution XI (no hardcoded secrets) |

---

## R-004: Next.js App Router Authentication Patterns

### Decision

Implement authentication in Next.js App Router using Better Auth with server-side session validation, client-side token management, and middleware-based route protection.

### Architecture Pattern

**Server Components (Default)**:
- Validate session on server before rendering
- Redirect unauthenticated users to /sign-in
- No client-side JavaScript for authentication checks

**Client Components (When Interactive)**:
- Use `"use client"` directive for forms and interactive UI
- Call Better Auth APIs for sign in/sign up/sign out
- Handle loading states and errors

### Implementation

```typescript
// frontend/src/app/layout.tsx (Server Component)
import { auth } from "@/lib/auth-client";

export default async function RootLayout({ children }) {
  const session = await auth();

  return (
    <html lang="en">
      <body>
        <AuthProvider session={session}>
          {children}
        </AuthProvider>
      </body>
    </html>
  );
}

// frontend/src/middleware.ts (Route Protection)
import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

export function middleware(request: NextRequest) {
  const token = request.cookies.get("better-auth-token")?.value;

  // Protect /tasks routes
  if (request.nextUrl.pathname.startsWith("/tasks")) {
    if (!token) {
      return NextResponse.redirect(new URL("/sign-in", request.url));
    }
  }

  // Redirect authenticated users away from auth pages
  if (request.nextUrl.pathname.startsWith("/sign-in") ||
      request.nextUrl.pathname.startsWith("/sign-up")) {
    if (token) {
      return NextResponse.redirect(new URL("/tasks", request.url));
    }
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/tasks/:path*", "/sign-in", "/sign-up"],
};

// frontend/src/components/AuthForm.tsx (Client Component)
"use client";

import { authClient } from "@/lib/auth-client";
import { useState } from "react";

export function SignInForm() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      await authClient.signIn.email({ email, password });
      // Better Auth handles redirect after successful sign in
    } catch (error) {
      // Handle error
    } finally {
      setLoading(false);
    }
  };

  return <form onSubmit={handleSubmit}>{/* form fields */}</form>;
}
```

### Session Persistence

- **Cookie Storage**: Better Auth stores JWT in HTTP-only cookie (secure by default)
- **Server-Side Validation**: Session checked on server before page render
- **Automatic Refresh**: Better Auth handles token refresh when approaching expiration

### Rationale

- **Server Components**: Faster initial loads, better SEO, session validation before render
- **Middleware Protection**: Centralized route guarding, prevents flash of unauthenticated content
- **Client Interactivity**: Forms and buttons need client-side state management
- **Cookie Security**: HTTP-only cookies prevent XSS attacks on tokens

### Alternatives Considered

| Alternative | Reason Rejected |
|-------------|-----------------|
| Client-side only auth | Slower, insecure (token in localStorage), poor SEO |
| getServerSideProps (Pages Router) | App Router is Next.js 13+ standard; Pages Router is legacy |
| HOC-based protection | Middleware is more performant and centralized |
| localStorage for token | Vulnerable to XSS; HTTP-only cookies more secure |

---

## R-005: API Client Token Interceptor Pattern

### Decision

Create a centralized API client wrapper using `fetch` with automatic Bearer token attachment and error handling.

### Implementation

```typescript
// frontend/src/lib/api.ts
import { authClient } from "./auth-client";

export class ApiError extends Error {
  constructor(public status: number, message: string) {
    super(message);
    this.name = "ApiError";
  }
}

export async function apiRequest<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  // Get JWT token from Better Auth
  const tokenData = await authClient.token();

  if (!tokenData?.token) {
    throw new ApiError(401, "Not authenticated");
  }

  const url = `${process.env.NEXT_PUBLIC_API_URL}${endpoint}`;

  const response = await fetch(url, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${tokenData.token}`,
      ...options.headers,
    },
  });

  if (!response.ok) {
    if (response.status === 401) {
      // Token expired or invalid - redirect to sign in
      window.location.href = "/sign-in";
      throw new ApiError(401, "Session expired");
    }

    const error = await response.json().catch(() => ({ detail: response.statusText }));
    throw new ApiError(response.status, error.detail || "Request failed");
  }

  return response.json();
}

// Convenience methods for common operations
export const taskApi = {
  getTasks: (userId: string) =>
    apiRequest<{ tasks: Task[] }>(`/api/${userId}/tasks`),

  createTask: (userId: string, data: CreateTaskInput) =>
    apiRequest<Task>(`/api/${userId}/tasks`, {
      method: "POST",
      body: JSON.stringify(data),
    }),

  updateTask: (userId: string, taskId: number, data: UpdateTaskInput) =>
    apiRequest<Task>(`/api/${userId}/tasks/${taskId}`, {
      method: "PUT",
      body: JSON.stringify(data),
    }),

  deleteTask: (userId: string, taskId: number) =>
    apiRequest<void>(`/api/${userId}/tasks/${taskId}`, {
      method: "DELETE",
    }),

  toggleComplete: (userId: string, taskId: number) =>
    apiRequest<Task>(`/api/${userId}/tasks/${taskId}/complete`, {
      method: "PATCH",
    }),
};
```

### Error Handling Strategy

| Status Code | Action | User Experience |
|-------------|--------|-----------------|
| 401 Unauthorized | Redirect to /sign-in | "Session expired, please sign in again" |
| 403 Forbidden | Show error toast | "Access denied" |
| 404 Not Found | Show error toast | "Task not found" |
| 400 Validation Error | Show form errors | Specific field validation messages |
| 500 Server Error | Show error toast | "Something went wrong. Please try again." |

### Rationale

- **Automatic Token Injection**: No need to manually add Authorization header in components
- **Type Safety**: Generic `apiRequest<T>` provides TypeScript types for responses
- **Error Handling**: Centralized error handling with ApiError class
- **401 Redirect**: Automatic redirect on session expiration improves UX
- **Convenience Methods**: taskApi object provides clean API for components

### Alternatives Considered

| Alternative | Reason Rejected |
|-------------|-----------------|
| axios library | Native fetch is sufficient; no need for additional dependency |
| React Query/SWR integration | Phase 2 doesn't require caching; can add later if needed |
| Manual token injection in components | Error-prone; violates DRY principle |
| GraphQL client | REST API is simpler for Phase 2 scope |

---

## R-006: SQLModel Table Creation and Migrations

### Decision

Use `SQLModel.metadata.create_all()` for initial table creation in development. Defer Alembic migrations to post-Phase 2 for production schema changes.

### Initial Table Creation

```python
# backend/src/app/database.py
from sqlmodel import SQLModel, create_engine

def init_db():
    """Initialize database tables"""
    # Import all models to register them
    from app.models.task import Task
    # Note: User model managed by Better Auth

    # Create all tables
    SQLModel.metadata.create_all(engine)
    print("✅ Database tables created successfully")

# Call during application startup
# backend/src/main.py
from fastapi import FastAPI
from app.database import init_db

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    init_db()
```

### Task Model Definition

```python
# backend/src/app/models/task.py
from sqlmodel import SQLModel, Field, Index
from datetime import datetime
from typing import Optional

class Task(SQLModel, table=True):
    __tablename__ = "tasks"
    __table_args__ = (
        Index("idx_tasks_user_id", "user_id"),
        Index("idx_tasks_completed", "completed"),
        Index("idx_tasks_user_completed", "user_id", "completed"),
        Index("idx_tasks_created_at", "created_at"),
        Index("idx_tasks_title", "title"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="users.id", nullable=False, index=True)
    title: str = Field(min_length=1, max_length=200, nullable=False)
    description: Optional[str] = Field(max_length=1000, default=None)
    completed: bool = Field(default=False, nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
```

### Alembic Integration (Post-Phase 2)

**When to use Alembic**:
- Production schema changes (adding columns, indexes, constraints)
- Team environments with multiple developers
- Rollback capabilities for schema changes

**Phase 2 Decision**: Skip Alembic for initial implementation to reduce complexity. Revisit if schema changes become frequent.

### Rationale

- **Simplicity**: `create_all()` is sufficient for Phase 2 MVP
- **Development Speed**: No migration files to manage during initial development
- **SQLModel Native**: Uses SQLModel's built-in table creation
- **Indexes Defined**: Performance indexes defined in model (no separate migration)
- **Deferred Complexity**: Alembic can be added later without refactoring models

### Alternatives Considered

| Alternative | Reason Rejected |
|-------------|-----------------|
| Alembic from start | Over-engineered for Phase 2; adds setup complexity |
| Raw SQL migrations | SQLModel provides type-safe schema definition |
| No indexes initially | Indexes improve query performance (SC-003: < 2 second operations) |
| Separate migration tool (Flyway, Liquibase) | Python ecosystem standard is Alembic; no need for Java tools |

---

## Summary of Decisions

| Research Task | Decision | Key Technology |
|---------------|----------|----------------|
| R-001 | Better Auth JWT Plugin | jwtClient() from better-auth/plugins |
| R-002 | FastAPI JWT Verification | python-jose[cryptography] with HS256 |
| R-003 | Neon PostgreSQL Connection | postgresql+psycopg with SQLModel |
| R-004 | Next.js Authentication | Server Components + Middleware protection |
| R-005 | API Client Pattern | Fetch wrapper with automatic Bearer token |
| R-006 | Table Creation | SQLModel.metadata.create_all() (Alembic deferred) |

**All NEEDS CLARIFICATION items from plan.md Technical Context have been resolved.**

---

**Research Status**: ✅ Complete
**Next Phase**: Phase 1 - Data Model & Contracts
