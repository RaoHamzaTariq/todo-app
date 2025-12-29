# Todo CLI Application Guide

A simple command-line todo application with in-memory storage. Built with Python 3.13+ following Spec-Driven Development principles.

## Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Commands](#commands)
- [Examples](#examples)
- [Features](#features)
- [Architecture](#architecture)
- [Development](#development)

## Installation

### Prerequisites

- Python 3.13 or higher
- `uv` package manager

### Setup

```bash
# Clone the repository
git clone <repository-url>
cd todo-app

# Install dependencies with uv
uv sync

# Verify installation
python --version  # Should be 3.13+
```

### Run the Application

```bash
# Using uv
uv run python main.py <command>

# Or using the script entry point (if configured)
todo <command>
```

## Quick Start

```bash
# Add your first task
uv run python main.py add "Learn Python" "Study dataclasses and enums"

# List all tasks
uv run python main.py list

# Mark a task as complete
uv run python main.py complete 1

# Update a task
uv run python main.py update 1 --title "Learn Python 3.13"

# Delete a task
uv run python main.py delete 1
```

## Commands

### `add` - Add a New Task

Create a new task with a title and optional description.

```bash
uv run python main.py add "Task title" "Optional description"
```

**Arguments:**
| Position | Name | Type | Required | Description |
|----------|------|------|----------|-------------|
| 1 | title | string | Yes | Task title (non-empty) |
| 2 | description | string | No | Optional task description |

**Example:**
```bash
uv run python main.py add "Buy groceries" "Milk, eggs, bread"
# Output: Added task 1: Buy groceries
```

---

### `list` - View All Tasks

Display all tasks with their ID, status, and title.

```bash
uv run python main.py list
```

**Example:**
```bash
uv run python main.py list
# Output:
# Tasks:
# 1. [Pending] Buy groceries
# 2. [Completed] Finish report
```

**Empty List:**
```bash
uv run python main.py list
# Output: No tasks found. Add a task with: todo add "Title" "Description"
```

---

### `update` - Update a Task

Modify the title and/or description of an existing task.

```bash
uv run python main.py update <task_id> [--title "New title"] [--description "New description"]
```

**Arguments:**
| Position/Flag | Name | Type | Required | Description |
|---------------|------|------|----------|-------------|
| 1 | task_id | int | Yes | Task ID to update |
| --title | title | string | No* | New task title |
| --description | description | string | No* | New task description |

*At least one of `--title` or `--description` must be provided.

**Examples:**
```bash
# Update title only
uv run python main.py update 1 --title "New title"

# Update description only
uv run python main.py update 1 --description "New description"

# Update both
uv run python main.py update 1 --title "New title" --description "New description"
```

---

### `complete` - Mark Task as Completed

Toggle a task's completion status.

```bash
uv run python main.py complete <task_id>
```

**Arguments:**
| Position | Name | Type | Required | Description |
|----------|------|------|----------|-------------|
| 1 | task_id | int | Yes | Task ID to complete |

**Example:**
```bash
uv run python main.py complete 1
# Output: Completed task 1: Buy groceries
```

---

### `delete` - Delete a Task

Remove a task from the list.

```bash
uv run python main.py delete <task_id>
```

**Arguments:**
| Position | Name | Type | Required | Description |
|----------|------|------|----------|-------------|
| 1 | task_id | int | Yes | Task ID to delete |

**Example:**
```bash
uv run python main.py delete 1
# Output: Deleted task 1
```

---

## Examples

### Complete Workflow Session

```bash
# Start with an empty list
$ uv run python main.py list
No tasks found. Add a task with: todo add "Title" "Description"

# Add some tasks
$ uv run python main.py add "Buy groceries" "Milk, eggs, bread"
Added task 1: Buy groceries

$ uv run python main.py add "Finish report" "Q4 summary"
Added task 2: Finish report

$ uv run python main.py add "Call dentist"
Added task 3: Call dentist

# View all tasks
$ uv run python main.py list
Tasks:
1. [Pending] Buy groceries
2. [Pending] Finish report
3. [Pending] Call dentist

# Complete the first task
$ uv run python main.py complete 1
Completed task 1: Buy groceries

# Update a task
$ uv run python main.py update 2 --title "Finish Q4 report"
Updated task 2: Finish Q4 report

# Check the list again
$ uv run python main.py list
Tasks:
1. [Completed] Buy groceries
2. [Pending] Finish Q4 report
3. [Pending] Call dentist

# Delete a completed task
$ uv run python main.py delete 1
Deleted task 1

# Final state
$ uv run python main.py list
Tasks:
2. [Pending] Finish Q4 report
3. [Pending] Call dentist
```

---

## Features

### Core Features

| Feature | Description |
|---------|-------------|
| Add Task | Create tasks with title and optional description |
| View Tasks | List all tasks with ID, status, and title |
| Update Task | Modify task title and/or description by ID |
| Complete Task | Toggle task status between Pending/Completed |
| Delete Task | Remove task by ID |

### Task Properties

- **ID**: Auto-incremented integer (1, 2, 3, ...)
- **Title**: Required string (1-255 characters)
- **Description**: Optional string (0-1000 characters)
- **Status**: Either "Pending" or "Completed"

### Validation

- Task titles cannot be empty
- Task IDs must exist for update/complete/delete operations
- At least one field (title or description) must be provided for updates

### Data Persistence

- All data is stored **in-memory** only
- Data persists for the duration of the session
- Data is lost when the application exits
- No external database or file storage

---

## Architecture

### Project Structure

```
todo-app/
├── src/
│   ├── cli/
│   │   ├── __init__.py
│   │   └── commands.py      # CLI layer - argument parsing, command handlers
│   └── core/
│       ├── __init__.py
│       ├── models.py        # Task dataclass, TaskStatus enum
│       └── todo_manager.py  # Business logic - CRUD operations
├── main.py                  # Application entry point
├── pyproject.toml           # Project configuration
├── tests/
│   └── test_todo_manager.py # Unit tests
└── guide.md                 # This file
```

### Design Principles

1. **Modular Architecture**: Clear separation between CLI layer and business logic
2. **Type Hints**: All functions have strict type annotations (Python 3.13+)
3. **In-Memory Storage**: Simple list-based storage, no external dependencies
4. **SDD Compliance**: Follows Spec-Driven Development workflow

### Separation of Concerns

| Layer | Responsibility | Files |
|-------|----------------|-------|
| CLI | User interaction, argument parsing, output formatting | `commands.py`, `main.py` |
| Business Logic | Task management, validation, state operations | `todo_manager.py`, `models.py` |

---

## Development

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with verbose output
uv run pytest -v

# Run specific test file
uv run pytest tests/test_todo_manager.py
```

### Code Quality

```bash
# Check code style (if ruff is installed)
uv add ruff --dev
uv run ruff check src/

# Check types (if mypy is installed)
uv add mypy --dev
uv run mypy src/
```

### Adding New Features

This project follows the Spec-Driven Development (SDD) workflow:

1. **Specify**: Create/update `specs/<feature>/spec.md`
2. **Plan**: Run `/sp.plan` to generate architecture
3. **Tasks**: Run `/sp.tasks` to generate implementation tasks
4. **Implement**: Run `/sp.implement <task_id>` to implement

### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success (operation completed) |
| 1 | Operation failed (validation error, not found, etc.) |
| 2 | Invalid command usage (missing arguments, unknown flags) |

---

## Troubleshooting

### "Module not found" Error

```bash
Error: ModuleNotFoundError: No module named 'src'
Solution: Run from project root directory
```

### "Task not found" Error

```bash
Error: Task <id> not found
Solution: Use `todo list` to see valid task IDs
```

### Empty Title Error

```bash
Error: Title cannot be empty
Solution: Provide a non-empty title for the task
```

---

## Version History

- **v0.1.0**: Initial implementation with 5 core features (Add, View, Update, Complete, Delete)
