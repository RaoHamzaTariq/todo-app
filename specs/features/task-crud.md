# Feature: Task CRUD Operations

## User Stories

- As a user, I can create a new task
- As a user, I can view all my tasks
- As a user, I can view a specific task
- As a user, I can update a task
- As a user, I can delete a task
- As a user, I can mark a task as complete/incomplete

## Acceptance Criteria

### Create Task

- Title is required (1-200 characters)
- Description is optional (max 1000 characters)
- Task is associated with logged-in user
- Task defaults to incomplete status
- Returns 201 on success
- Returns 400 if title is invalid

### View All Tasks

- Only show tasks for current user (scoped by JWT)
- Display: id, title, description, status, created_at, updated_at
- Support filtering by status: "all", "pending", "completed"
- Support sorting by: "created_at", "title", "updated_at"
- Returns 200 with array of tasks
- Returns 401 if not authenticated

### View Single Task

- Task must belong to authenticated user
- Returns 200 with task details
- Returns 404 if task not found
- Returns 401 if not authenticated
- Returns 403 if task belongs to another user

### Update Task

- Title is optional (1-200 characters if provided)
- Description is optional (max 1000 characters if provided)
- Completed status can be toggled
- Only owner can update
- Returns 200 with updated task
- Returns 404 if task not found
- Returns 401 if not authenticated
- Returns 403 if task belongs to another user

### Delete Task

- Only owner can delete
- Returns 204 on success (no content)
- Returns 404 if task not found
- Returns 401 if not authenticated
- Returns 403 if task belongs to another user

### Toggle Complete

- Switches completed status (true <-> false)
- Returns 200 with updated task
- Returns 404 if task not found
- Returns 401 if not authenticated
- Returns 403 if task belongs to another user

## Data Model

```typescript
interface Task {
  id: number;
  user_id: string;
  title: string;
  description: string | null;
  completed: boolean;
  created_at: string; // ISO 8601
  updated_at: string; // ISO 8601
}
```

## API Endpoints

See: `@specs/api/rest-endpoints.md`

## UI Requirements

See: `@specs/ui/components.md` and `@specs/ui/pages.md`