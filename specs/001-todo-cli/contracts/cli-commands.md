# CLI Command Contracts

**Feature**: 001-todo-cli | **Last Updated**: 2025-12-29

## Command Overview

| Command | Description | Priority |
|---------|-------------|----------|
| `add` | Create a new task | P1 |
| `list` | Display all tasks | P1 |
| `update` | Modify an existing task | P2 |
| `complete` | Mark task as completed | P2 |
| `delete` | Remove a task | P3 |

## Command Specifications

### `add` - Create a New Task

**Command**: `todo add "TITLE" ["DESCRIPTION"]`

**Arguments**:
| Position | Name | Type | Required | Default | Description |
|----------|------|------|----------|---------|-------------|
| 1 | title | string | Yes | - | Task title (non-empty) |
| 2 | description | string | No | "" | Optional task description |

**Output**:
```
Added task 1: Buy groceries
```

**Error Cases**:
| Condition | Output | Exit Code |
|-----------|--------|-----------|
| Empty title | "Error: Title cannot be empty" | 1 |
| Missing title argument | argparse error + help | 2 |

**Validation**:
- Title must be non-empty after stripping whitespace
- Description is optional (defaults to empty string)

---

### `list` - Display All Tasks

**Command**: `todo list`

**Arguments**: None

**Output** (when tasks exist):
```
Tasks:
1. [Pending] Buy groceries
2. [Completed] Finish report
```

**Output** (when no tasks):
```
No tasks found. Add a task with: todo add "Title" "Description"
```

**Error Cases**: None (always succeeds)

---

### `update` - Modify an Existing Task

**Command**: `todo update ID [--title "TITLE"] [--description "DESCRIPTION"]`

**Arguments**:
| Position/Flag | Name | Type | Required | Description |
|---------------|------|------|----------|-------------|
| 1 | id | int | Yes | Task ID to update |
| --title | title | string | No* | New task title |
| --description | description | string | No* | New task description |

*At least one of --title or --description must be provided

**Output**:
```
Updated task 1: Buy groceries - Milk, eggs, bread
```

**Error Cases**:
| Condition | Output | Exit Code |
|-----------|--------|-----------|
| Task ID not found | "Error: Task 5 not found" | 1 |
| Neither --title nor --description provided | "Error: Must provide --title or --description" | 1 |
| Empty title provided | "Error: Title cannot be empty" | 1 |
| Invalid ID format | argparse error | 2 |

---

### `complete` - Mark Task as Completed

**Command**: `todo complete ID`

**Arguments**:
| Position | Name | Type | Required | Description |
|----------|------|------|----------|-------------|
| 1 | id | int | Yes | Task ID to complete |

**Output**:
```
Completed task 1: Buy groceries
```

**Error Cases**:
| Condition | Output | Exit Code |
|-----------|--------|-----------|
| Task ID not found | "Error: Task 5 not found" | 1 |
| Already completed | "Task 1 is already completed" | 0 (informational) |
| Invalid ID format | argparse error | 2 |

---

### `delete` - Remove a Task

**Command**: `todo delete ID`

**Arguments**:
| Position | Name | Type | Required | Description |
|----------|------|------|----------|-------------|
| 1 | id | int | Yes | Task ID to delete |

**Output**:
```
Deleted task 1: Buy groceries
```

**Error Cases**:
| Condition | Output | Exit Code |
|-----------|--------|-----------|
| Task ID not found | "Error: Task 5 not found" | 1 |
| Invalid ID format | argparse error | 2 |

---

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success (operation completed) |
| 1 | Operation failed (validation error, not found, etc.) |
| 2 | Invalid command usage (missing arguments, unknown flags) |

## Implementation Contract

### CLI Layer Responsibilities (`src/cli/commands.py`)

1. Parse user input using `argparse`
2. Validate command arguments
3. Call appropriate `TodoManager` method
4. Format and display output
5. Handle errors with user-friendly messages
6. Exit with appropriate exit code

### Business Logic Layer Responsibilities (`src/core/todo_manager.py`)

1. Manage in-memory task storage
2. Implement CRUD operations with validation
3. Raise appropriate exceptions (`ValueError`, `KeyError`)
4. Return `Task` objects to CLI layer
5. Handle all data manipulation logic

### Separation of Concerns

| Layer | Should NOT |
|-------|------------|
| CLI | Have direct access to task storage |
| Business Logic | Import argparse or handle CLI output formatting |

## Example Usage Session

```bash
$ todo add "Buy groceries" "Milk, eggs, bread"
Added task 1: Buy groceries

$ todo add "Finish report" "Q4 summary"
Added task 2: Finish report

$ todo list
Tasks:
1. [Pending] Buy groceries
2. [Pending] Finish report

$ todo complete 1
Completed task 1: Buy groceries

$ todo update 2 --title "Finish Q4 report"
Updated task 2: Finish Q4 report

$ todo list
Tasks:
1. [Completed] Buy groceries
2. [Pending] Finish Q4 report

$ todo delete 1
Deleted task 1: Buy groceries

$ todo list
Tasks:
2. [Pending] Finish Q4 report
```
