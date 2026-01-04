# MCP Tools

## Overview

Model Context Protocol (MCP) tools for AI chatbot integration. These tools enable an AI assistant to interact with the todo application programmatically.

## Tool Categories

### Task Management Tools

| Tool Name | Description |
|-----------|-------------|
| `get_tasks` | List user's tasks with optional filters |
| `get_task` | Get a specific task by ID |
| `create_task` | Create a new task |
| `update_task` | Update an existing task |
| `delete_task` | Delete a task |
| `toggle_task_complete` | Toggle task completion status |

## Tool Definitions

### get_tasks

List tasks for the authenticated user.

**Input:**
```json
{
  "status": "all" | "pending" | "completed",
  "sort": "created_at" | "title" | "updated_at"
}
```

**Output:**
```json
{
  "tasks": [...]
}
```

---

### get_task

Get a specific task by ID.

**Input:**
```json
{
  "task_id": number
}
```

**Output:**
```json
{
  "task": {...}
}
```

---

### create_task

Create a new task.

**Input:**
```json
{
  "title": string,
  "description": string | null
}
```

**Output:**
```json
{
  "task": {...}
}
```

---

### update_task

Update an existing task.

**Input:**
```json
{
  "task_id": number,
  "title": string | null,
  "description": string | null,
  "completed": boolean | null
}
```

**Output:**
```json
{
  "task": {...}
}
```

---

### delete_task

Delete a task.

**Input:**
```json
{
  "task_id": number
}
```

**Output:**
```json
{
  "success": true
}
```

---

### toggle_task_complete

Toggle task completion status.

**Input:**
```json
{
  "task_id": number
}
```

**Output:**
```json
{
  "task": {...}
}
```

## Usage Notes

- All tools require JWT authentication
- Tools operate on the authenticated user's data only
- Tool names follow naming convention: `prefix_verb_noun`
- Parameters use snake_case

## Implementation

See: `@backend/CLAUDE.md` for implementation details.
