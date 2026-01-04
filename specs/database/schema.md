# Database Schema

## Tables

### users (managed by Better Auth)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | string | PRIMARY KEY | Unique user identifier |
| email | string | UNIQUE, NOT NULL | User email address |
| name | string | | User display name |
| image | string | | Avatar URL (optional) |
| created_at | timestamp | NOT NULL | Account creation time |
| updated_at | timestamp | NOT NULL | Last update time |

**Note:** The users table is managed by Better Auth. Do not modify directly.

---

### tasks

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | integer | PRIMARY KEY | Unique task identifier |
| user_id | string | NOT NULL, FOREIGN KEY -> users.id | Owner of the task |
| title | string | NOT NULL, 1-200 chars | Task title |
| description | text | NULLABLE, max 1000 chars | Task description |
| completed | boolean | NOT NULL, DEFAULT false | Completion status |
| created_at | timestamp | NOT NULL | Creation timestamp |
| updated_at | timestamp | NOT NULL | Last update timestamp |

## Indexes

| Index Name | Columns | Purpose |
|------------|---------|---------|
| idx_tasks_user_id | user_id | Filter tasks by user |
| idx_tasks_completed | completed | Filter by status |
| idx_tasks_user_completed | user_id, completed | Combined filter |
| idx_tasks_created_at | created_at | Sort by creation |
| idx_tasks_title | title | Sort/search by title |

## Relationships

```
users (1) ──────< (N) tasks
  id                user_id
```

- Each task belongs to exactly one user
- A user can have many tasks (0 to N)
- Deleting a user should cascade to their tasks

## SQLModel Definition

```python
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="users.id", nullable=False)
    title: str = Field(min_length=1, max_length=200, nullable=False)
    description: Optional[str] = Field(max_length=1000, default=None)
    completed: bool = Field(default=False, nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
```

## Database Connection

**Connection String Format:**
```
postgresql+psycopg://username:password@host:port/database
```

**Neon Serverless Example:**
```
postgresql+psycopg://user:pass@ep-xyz.region.neon.tech/dbname
```

## Related Specifications

- Task CRUD: `@specs/features/task-crud.md`
- REST Endpoints: `@specs/api/rest-endpoints.md`
