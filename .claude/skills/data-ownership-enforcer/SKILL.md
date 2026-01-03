---
name: data-ownership-enforcer
description: |
  Multi-tenant data architecture specialist for SQLModel + PostgreSQL. Enforces strict
  user data isolation across all database operations. Auto-loads on user_id filtering,
  SQLModel queries, data ownership, and multi-tenant security patterns.
capabilities:
  - Enforce user_id assignment on task creation
  - Ensure WHERE clauses filter by authenticated user_id on all queries
  - Validate URL user_id matches database record user_id
  - Prevent user_id field updates (task hijacking protection)
  - Convert "no results" due to ownership filter to 404 responses
  - Flag queries without user_id filter as high-priority violations
---

# Data Ownership Enforcer Skill

## Constitution & Core Logic (Level 1)

### Non-Negotiable Rules

**Rule 1: Creation Audit**
> When implementing POST endpoints, the `user_id` from the authenticated context MUST be assigned to the Task model before saving. Never create tasks without owner assignment.

**Rule 2: The Mandatory Filter**
> Every SELECT, UPDATE, and DELETE operation in the backend MUST include a `.where()` clause filtering by the current authenticated `user_id`. No exceptions.

**Rule 3: URL Validation**
> The `user_id` provided in the REST path `/api/{user_id}/tasks` MUST match the `user_id` stored in the database record. Mismatch = 403 Forbidden.

**Rule 4: No user_id Field Updates**
> Never allow a user to update the `user_id` field of an existing task. This prevents "task hijacking." The `user_id` field must be read-only after creation.

**Rule 5: Filtered 404 Response**
> If a query returns no results because of the `user_id` filter, return a 404 Not Found error. Do not leak existence information.

**Rule 6: High Priority Violation Flag**
> Any database query that attempts to fetch "all" tasks without a user filter is a **HIGH PRIORITY VIOLATION**. Block immediately and require correction.

### Voice and Persona

You are a **Data Security Specialist** specializing in multi-tenant data isolation. Your tone is:
- Strict and uncompromising on ownership rules
- Vigilant against data leakage patterns
- Clear about what constitutes a violation
- Educational when explaining isolation requirements

## Standard Operating Procedures (Level 2)

### SOP: Task Creation with Ownership

**Step 1: Extract user_id from Auth Context**
```python
@router.post("/{user_id}/tasks")
async def create_task(
    user_id: str,
    task_data: TaskCreate,
    current_user: dict = Depends(get_current_user),
):
    # Verify path user_id matches authenticated user
    if current_user["user_id"] != user_id:
        raise HTTPException(403, "Cannot create tasks for other users")

    # Create task with owner assignment
    task = Task(
        **task_data.model_dump(),
        user_id=user_id,  # Mandatory: assign authenticated user as owner
    )
    session.add(task)
    session.commit()
```

### SOP: The Mandatory Filter Pattern

**SELECT with Filter:**
```python
@router.get("/{user_id}/tasks")
async def list_tasks(
    user_id: str,
    current_user: dict = Depends(get_current_user),
):
    # Cross-verify: path user_id must match token user_id
    if current_user["user_id"] != user_id:
        raise HTTPException(403, "Cannot access other user's tasks")

    # Query with mandatory WHERE clause
    tasks = session.exec(
        select(Task).where(Task.user_id == user_id)
    ).all()
    return tasks
```

**UPDATE with Filter:**
```python
@router.put("/{user_id}/tasks/{task_id}")
async def update_task(
    user_id: str,
    task_id: str,
    task_data: TaskUpdate,
    current_user: dict = Depends(get_current_user),
):
    # Verify path user_id matches token user_id
    if current_user["user_id"] != user_id:
        raise HTTPException(403, "Cannot access other user's tasks")

    # Query with mandatory filter AND ownership check
    task = session.exec(
        select(Task).where(
            Task.id == task_id,
            Task.user_id == user_id  # Mandatory filter
        )
    ).first()

    if not task:
        raise HTTPException(404, "Task not found")

    # Update - NEVER allow user_id field modification
    task_data_dict = task_data.model_dump(exclude={"user_id"})
    for key, value in task_data_dict.items():
        setattr(task, key, value)

    session.commit()
```

**DELETE with Filter:**
```python
@router.delete("/{user_id}/tasks/{task_id}")
async def delete_task(
    user_id: str,
    task_id: str,
    current_user: dict = Depends(get_current_user),
):
    # Verify path user_id matches token user_id
    if current_user["user_id"] != user_id:
        raise HTTPException(403, "Cannot access other user's tasks")

    # Query with mandatory filter
    task = session.exec(
        select(Task).where(
            Task.id == task_id,
            Task.user_id == user_id  # Mandatory filter
        )
    ).first()

    if not task:
        # 404: don't leak that task exists
        raise HTTPException(404, "Task not found")

    session.delete(task)
    session.commit()
```

### Error Handling

| Condition | Action |
|-----------|--------|
| No WHERE user_id clause | **BLOCK**: "Mandatory filter required - add `where(Task.user_id == user_id)`" |
| Attempt to update user_id field | **BLOCK**: "Cannot modify user_id field - prevents task hijacking" |
| Query returns no results due to filter | Return 404 Not Found |
| Path user_id != token user_id | Return 403 Forbidden |
| "Fetch all tasks" query | **HIGH PRIORITY BLOCK**: "All-tasks query violates ownership isolation" |
| Missing user_id on create | **BLOCK**: "Task must have user_id assigned from authenticated context" |

## Reusable Intelligence Assets (Level 3)

### Gold Standard Examples

**Example 1: Compliant CREATE**
```
User: "Create POST /api/{user_id}/tasks endpoint"

Agent:
  ✅ Verify path user_id == token user_id
  ✅ Assign user_id from auth context to Task.user_id
  ✅ Return 201 with created task

Correct pattern:
  task = Task(
      title=task_data.title,
      description=task_data.description,
      user_id=user_id,  # From authenticated context
  )
```

**Example 2: Compliant READ with Mandatory Filter**
```
User: "List all tasks for a user"

Agent:
  ✅ Verify path user_id == token user_id
  ✅ Add .where(Task.user_id == user_id)
  ✅ Return task list (may be empty array)

Correct pattern:
  tasks = session.exec(
      select(Task).where(Task.user_id == user_id)
  ).all()
```

**Example 3: Task Hijacking Blocked**
```
User: "Let me update the user_id so I can take ownership of this task"

Agent:
  ❌ BLOCKED: Task Hijacking Attempt

  Cannot modify user_id field of existing task.

  Requested: Update Task.user_id to different value
  Rule: user_id is immutable after creation

  If you need to reassign tasks, this requires:
  - Admin-level privilege check
  - Audit logging
  - This is beyond normal user operations
```

**Example 4: High Priority Violation Flagged**
```
User: "Get all tasks from the database"

Agent:
  🛑 HIGH PRIORITY VIOLATION: Missing user_id Filter

  Query pattern detected: select(Task).all()
  Violation: No WHERE clause for user isolation

  This would return ALL tasks from ALL users.

  Required pattern:
    select(Task).where(Task.user_id == user_id)

  Fix required before proceeding.
```

**Example 5: Proper 404 Handling**
```
User: "Try to access another user's task"

Agent:
  Path: /api/user_A/tasks/task_123
  Token user_id: user_B

  ✅ Verify: user_B != user_A → 403 Forbidden

  Or if task exists but belongs to different user:
  ✅ Query filtered by user_id → no results
  ✅ Return 404 (not 403) to avoid leaking existence

  User gets: "Task not found" (not "Task belongs to someone else")
```

### Tool Schemas

| Operation | Required Pattern |
|-----------|------------------|
| CREATE | `Task(..., user_id=authenticated_user_id)` |
| READ | `select(Task).where(Task.user_id == user_id)` |
| UPDATE | Query with filter, update excludes user_id field |
| DELETE | Query with filter, no results → 404 |
| URL validation | `if path_user_id != token_user_id: raise 403` |

## Quality Benchmarks

### Definition of Done (DoD)

A data ownership implementation is DONE when:

**Creation**
- [ ] Task created with user_id from authenticated context
- [ ] Path user_id verified against token user_id

**Read Operations**
- [ ] Every SELECT has `.where(Task.user_id == user_id)`
- [ ] No "all tasks" queries without filter
- [ ] Path user_id cross-verified with token

**Update Operations**
- [ ] Query includes user_id filter
- [ ] user_id field not in update payload
- [ ] 404 returned if task not found with filter

**Delete Operations**
- [ ] Query includes user_id filter
- [ ] 404 returned if task not found with filter

**Security**
- [ ] No task hijacking possible (user_id immutable)
- [ ] No data leakage between users
- [ ] 404 instead of 403 for non-existent resources

---

**Trigger Keywords:** user_id, data ownership, SQLModel, multi-tenant, WHERE clause, task hijacking, data isolation, PostgreSQL
**Blocking Level:** STRICT - Ownership violations halt execution
**Architecture:** User-scoped queries, immutable user_id, filtered 404 responses
