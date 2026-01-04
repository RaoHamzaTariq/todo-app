# Backend Guidelines (FastAPI)

## Project Structure

```
backend/
├── src/
│   ├── main.py
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── routers/
│   │   │   ├── __init__.py
│   │   │   └── tasks.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   └── task.py
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   └── task.py
│   │   └── middleware/
│   │       ├── __init__.py
│   │       └── auth.py
│   └── db/
│       ├── __init__.py
│       └── database.py
├── tests/
│   ├── __init__.py
│   └── test_tasks.py
├── .env
├── pyproject.toml
└── requirements.txt
```

## Technology Stack

- **Framework:** FastAPI
- **ORM:** SQLModel
- **Database:** Neon Serverless PostgreSQL
- **Authentication:** JWT (via Better Auth on frontend)
- **Language:** Python 3.13+

## Project Structure Details

- `main.py` - FastAPI app entry point
- `models.py` - SQLModel database models
- `routes/` - API route handlers
- `db.py` - Database connection

## API Conventions

- All routes under `/api/`
- Return JSON responses
- Use Pydantic models for request/response
- Handle errors with HTTPException

## Database and ORM Usage

Define models using SQLModel for type safety:

```python
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="users.id")
    title: str
    description: Optional[str] = None
    completed: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

Use SQLModel for all database operations.

## REST Endpoints

| Method | Endpoint | Description |
| ------ | -------- | ----------- |
| GET | `/api/{user_id}/tasks` | List all tasks |
| POST | `/api/{user_id}/tasks` | Create a new task |
| GET | `/api/{user_id}/tasks/{id}` | Get task details |
| PUT | `/api/{user_id}/tasks/{id}` | Update a task |
| DELETE | `/api/{user_id}/tasks/{id}` | Delete a task |
| PATCH | `/api/{user_id}/tasks/{id}/complete` | Toggle completion |

## JWT Verification Middleware

```python
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

async def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    token = credentials.credentials
    # Verify JWT and extract payload
    payload = decode_jwt(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    return payload
```

## Error Response Format

```python
class ErrorResponse(SQLModel):
    detail: str
```

## Database Connection

Connect to Neon Serverless PostgreSQL:

```python
from sqlmodel import create_engine

DATABASE_URL = "postgresql+psycopg://user:pass@host/db"
engine = create_engine(DATABASE_URL)
```

Connection string from environment variable: `DATABASE_URL`

## Development Workflow

1. Read database specs from `specs/database/schema.md`
2. Read API specs from `specs/api/rest-endpoints.md`
3. Implement models and schemas
4. Create API routes following the spec
5. Add JWT verification to all endpoints
6. Test endpoints with pytest

## Environment Variables

```env
DATABASE_URL=postgresql+psycopg://user:pass@host/db
BETTER_AUTH_SECRET=your-secret-key
JWT_ALGORITHM=HS256
```

## Running

```bash
cd backend && uvicorn main:app --reload --port 8000
```
