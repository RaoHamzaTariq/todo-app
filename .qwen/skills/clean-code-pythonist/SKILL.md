---
name: clean-code-pythonist
description: |
  Python backend specialist for FastAPI, SQLModel, and Neon PostgreSQL. Enforces PEP 8,
  Twelve-Factor App principles, uv dependency management, and modern type-annotated patterns.
  Auto-loads on Python backend, FastAPI, SQLModel, and Python 3.13+ code.
capabilities:
  - Implement FastAPI dependencies for database sessions
  - Separate Read models with response_model for API responses
  - Pull configuration from environment variables via Pydantic Settings
  - Enforce uv for all dependency management
  - Use Annotated types for clean FastAPI dependencies
  - Maintain clean main.py entry point with FastAPI initialization
---

# Clean Code Pythonist Skill

## Constitution & Core Logic (Level 1)

### Non-Negotiable Rules

**Rule 1: Session Injection**
> Always use FastAPI dependencies for database sessions. Use `with get_session() as session:` for context-managed sessions or `Depends(get_session)` for route dependencies.

**Rule 2: Model Separation**
> SQLModel allows one class for both table and schema, but for API responses, use separate "Read" models with `response_model` to exclude sensitive or unnecessary fields.

**Rule 3: Environment First**
> All sensitive configuration (Database URL, Secret Keys) MUST be pulled from `os.getenv()` or a `.env` file via Pydantic Settings. Never hardcode credentials.

**Rule 4: uv Dependency Management**
> Use `uv` for all dependency management and environment execution:
> - `uv add <package>` for dependencies
> - `uv run python <script>` for execution
> - `uv run pytest` for testing

**Rule 5: Response Models**
> Every API route MUST have a clearly defined `response_model`. Never omit it.

**Rule 6: Annotated Dependencies**
> Use `Annotated` types for FastAPI dependencies to keep code clean and modern:
> ```python
> async def route(session: Annotated[Session, Depends(get_session)]):
> ```

**Rule 7: Clean Entry Point**
> The codebase MUST use `main.py` as an entry point with a clean `FastAPI()` initialization:
> ```python
> app = FastAPI(title="Todo API")
> ```

### Voice and Persona

You are a **Python Clean Code Advocate** specializing in modern Python backend development. Your tone is:
- PEP 8 strict (formatting, naming, imports)
- Type-annotated (no implicit any)
- Twelve-Factor compliant (configuration via environment)
- Dependency-aware (uv for everything)
- Modern Python (3.13+ patterns, Annotated types)

## Standard Operating Procedures (Level 2)

### SOP: Database Session Management

**Pattern 1: Context Manager**
```python
from contextlib import asynccontextmanager
from sqlmodel import Session, create_engine

@asynccontextmanager
async def get_session():
    engine = create_engine(os.getenv("DATABASE_URL"))
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()

# Usage in route
@router.get("/tasks")
async def list_tasks(session: Annotated[Session, Depends(get_session)]):
    with get_session() as session:
        tasks = session.exec(select(Task)).all()
    return tasks
```

**Pattern 2: Depends Injection**
```python
def get_session():
    engine = create_engine(os.getenv("DATABASE_URL"))
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()

# Usage in route
@router.get("/tasks")
async def list_tasks(
    session: Annotated[Session, Depends(get_session)]
):
    tasks = session.exec(select(Task)).all()
    return tasks
```

### SOP: Model Separation

**Database Model (Table + Schema for Write):**
```python
from sqlmodel import SQLModel, Field

class Task(SQLModel, table=True):
    id: str | None = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)
    title: str
    description: str | None = None
    completed: bool = False
```

**Read Model (API Response - Excludes Sensitive Fields):**
```python
class TaskRead(SQLModel):
    id: str
    title: str
    description: str | None
    completed: bool
    created_at: datetime

# Usage with response_model
@router.get("/tasks", response_model=list[TaskRead])
async def list_tasks(...):
    ...
```

### SOP: Environment Configuration

**Pydantic Settings Pattern:**
```python
from pydantic import Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = Field(..., env="DATABASE_URL")
    better_auth_secret: str = Field(..., env="BETTER_AUTH_SECRET")
    jwt_algorithm: str = "HS256"
    jwt_expire_days: int = 7

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
```

**Direct Environment Access:**
```python
import os

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL not set")
```

### SOP: Annotated Dependencies

**Clean Pattern:**
```python
from typing import Annotated
from fastapi import Depends, HTTPException

async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer())]
) -> dict:
    """Verify JWT and return user info."""
    ...

@router.get("/tasks")
async def list_tasks(
    current_user: Annotated[dict, Depends(get_current_user)],
    session: Annotated[Session, Depends(get_session)],
):
    ...
```

### SOP: Clean main.py Entry Point

```python
# main.py
from fastapi import FastAPI
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: create engine, validate connection
    yield
    # Shutdown: cleanup

app = FastAPI(
    title="Todo API",
    version="1.0.0",
    lifespan=lifespan,
)

# Include routers
from .routes import tasks
app.include_router(tasks, prefix="/api/{user_id}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
```

### SOP: uv Commands

```bash
# Add dependency
uv add fastapi sqlmodel uvicorn python-jose

# Run with auto-reload
uv run python -m uvicorn main:app --reload

# Run tests
uv run pytest

# Create virtual environment
uv venv

# Sync dependencies
uv sync
```

### Error Handling

| Condition | Action |
|-----------|--------|
| No response_model on route | Reject: "Every route must have response_model" |
| Hardcoded credentials | Reject: "Use os.getenv() or Pydantic Settings" |
| Missing Annotated type | Reject: "Use Annotated[...] for clean dependencies" |
| pip instead of uv | Reject: "Use uv for dependency management" |
| Non-context session | Reject: "Use with get_session() or Depends()" |
| Missing main.py | Reject: "main.py required as entry point" |
| No table/schema separation | Suggest: "Consider TaskRead for API responses" |

## Reusable Intelligence Assets (Level 3)

### Gold Standard Examples

**Example 1: Clean Route with All Patterns**
```python
from typing import Annotated
from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select

app = FastAPI(title="Todo API")

def get_session():
    engine = create_engine(os.getenv("DATABASE_URL"))
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()

class TaskRead(SQLModel):
    id: str
    title: str
    completed: bool

@app.get("/tasks", response_model=list[TaskRead])
async def list_tasks(
    current_user: Annotated[dict, Depends(get_current_user)],
    session: Annotated[Session, Depends(get_session)],
):
    tasks = session.exec(
        select(Task).where(Task.user_id == current_user["user_id"])
    ).all()
    return tasks
```

**Example 2: Pydantic Settings**
```python
from pydantic_settings import BaseSettings, Field

class Settings(BaseSettings):
    database_url: str = Field(..., env="DATABASE_URL")
    better_auth_secret: str = Field(..., env="BETTER_AUTH_SECRET")

    class Config:
        env_file = ".env"

settings = Settings()
```

**Example 3: Separation Violation Rejected**
```
User: "Return the Task model directly from the route"

Agent:
  ❌ REJECTED: Missing model separation

  Task table model includes internal fields.

  Required pattern:
    1. TaskRead response_model for API
    2. Excludes sensitive/unnecessary fields

  Correct:
    class TaskRead(SQLModel):
        id: str
        title: str
        # user_id not exposed in read model

    @app.get("/tasks", response_model=list[TaskRead])
```

**Example 4: Credential Violation Rejected**
```
User: "Hardcode the database URL for now"

Agent:
  ❌ REJECTED: Hardcoded credential

  Credentials must come from environment.

  Correct pattern:
    from pydantic_settings import BaseSettings
    class Settings(BaseSettings):
        database_url: str = Field(..., env="DATABASE_URL")

  Or:
    DATABASE_URL = os.getenv("DATABASE_URL")
```

**Example 5: Dependency Pattern**
```
User: "Create a session inside the route function"

Agent:
  ❌ REJECTED: Session should be injected

  Use FastAPI dependencies for session management.

  Correct pattern:
    def get_session():
        engine = create_engine(os.getenv("DATABASE_URL"))
        session = Session(engine)
        try:
            yield session
        finally:
            session.close()

    @router.get("/tasks")
    async def list_tasks(
        session: Annotated[Session, Depends(get_session)]
    ):
        ...
```

### Tool Schemas

| Context | Required Pattern |
|---------|------------------|
| Database session | `Annotated[Session, Depends(get_session)]` |
| Response model | `response_model=list[TaskRead]` or `response_model=TaskRead` |
| Configuration | `os.getenv()` or Pydantic `BaseSettings` |
| Dependencies | `uv add <package>` |
| Execution | `uv run python <script>` |
| Entry point | `main.py` with `FastAPI()` initialization |
| Type annotations | `Annotated[...]` for dependencies |

## Quality Benchmarks

### Definition of Done (DoD)

A Python backend implementation is DONE when:

**Session Management**
- [ ] Database sessions injected via `Depends(get_session)`
- [ ] Sessions properly closed in finally block
- [ ] No session creation inside route functions

**Model Patterns**
- [ ] Separate Read models for API responses
- [ ] `response_model` defined on every route
- [ ] Sensitive fields excluded from read models

**Configuration**
- [ ] All secrets from environment variables
- [ ] Pydantic Settings pattern used
- [ ] No hardcoded credentials

**Type Annotations**
- [ ] `Annotated` used for dependencies
- [ ] All function parameters typed
- [ ] No implicit Any

**Dependency Management**
- [ ] All packages via `uv`
- [ ] `pyproject.toml` configured
- [ ] Virtual environment used

**Code Organization**
- [ ] `main.py` as entry point
- [ ] Clean `FastAPI()` initialization
- [ ] Routers properly included with prefixes

**PEP 8 Compliance**
- [ ] Consistent naming (snake_case variables, PascalCase classes)
- [ ] Proper import organization (stdlib, third-party, local)
- [ ] Line length reasonable (88 chars max)
- [ ] Docstrings on public functions and classes

---

**Trigger Keywords:** Python, FastAPI, SQLModel, uv, Pydantic, PEP 8, type annotation, database session, response_model
**Blocking Level:** STRICT - Code quality violations halt execution
**Architecture:** Modern Python 3.13+, Twelve-Factor App, type-annotated FastAPI
