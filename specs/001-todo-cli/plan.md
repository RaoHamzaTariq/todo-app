# Implementation Plan: In-Memory Todo CLI

**Branch**: `001-todo-cli` | **Date**: 2025-12-29 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `specs/001-todo-cli/spec.md`

**Note**: This template is filled in by the `/sp.plan` command.

## Summary

Build a Python 3.13+ CLI application for managing todo tasks with in-memory storage. The application provides 5 core features: Add, View, Update, Delete, and Mark Complete. Architecture follows modular design with clear separation between CLI layer (`src/cli/`) and business logic layer (`src/core/`). All data persists only during the session using Python lists/dictionaries.

## Technical Context

**Language/Version**: Python 3.13+ (specified in spec: PIR-001, PIR-003)
**Primary Dependencies**: `uv` for package management (spec: PIR-002) - no external dependencies required
**Storage**: In-memory using Python lists/dictionaries (spec: SR-001, SR-004) - NO external databases
**Testing**: pytest for unit tests (per constitution code quality standards)
**Target Platform**: Cross-platform CLI (Linux, macOS, Windows)
**Project Type**: Single project - Python CLI application
**Performance Goals**: Application starts instantly (SC-004), operations complete in under 2 seconds (SC-001)
**Constraints**:
- In-memory storage only (Phase 1) per constitution Principle III
- Modular architecture: CLI layer separated from business logic per spec AR-001
- Python 3.13+ with strict type hints per constitution Principle V
- SDD workflow compliance per constitution Principle I
**Scale/Scope**: Single user, local CLI tool - 5 core features only per constitution Principle IV

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Gate Evaluation

| Principle | Requirement | Status | Notes |
|-----------|-------------|--------|-------|
| I. SDD | Follow workflow: Specify -> Plan -> Tasks -> Implement | ✅ PASS | Currently in Plan phase |
| II. Python 3.13+ | Use Python 3.13+ with uv | ✅ PASS | Specified in PIR-001, PIR-003 |
| III. In-Memory Storage | No external databases | ✅ PASS | Specified in SR-001 through SR-004 |
| IV. Core Feature Focus | 5 core features only | ✅ PASS | Add, View, Update, Delete, Complete |
| V. Code Quality | Type hints, PEP 8, testable | ✅ PASS | Specified in PIR-004 through PIR-007 |
| VI. Task ID Requirement | Reference Task ID in code | ✅ PASS | Will be enforced during implementation |
| IX. Modular Architecture | CLI/Business layer separation | ✅ PASS | Specified in AR-001 through AR-005 |

**Result**: ✅ ALL GATES PASS - Proceed to Phase 1 design

## Project Structure

### Documentation (this feature)

```text
specs/001-todo-cli/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (skipped - all requirements clear)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
│   └── cli-commands.md  # CLI command contracts
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
src/
  cli/
    __init__.py
    commands.py          # CLI entry points, argument parsing
  core/
    __init__.py
    models.py            # Data models (type-hinted)
    todo_manager.py      # Business logic operations
main.py                  # Application entry point
pyproject.toml           # Python 3.13+, uv config
tests/
  test_todo_manager.py   # Unit tests for core logic
```

**Structure Decision**: Single project structure (Option 1) selected per spec requirements. Modular architecture with `src/cli/` for UI layer and `src/core/` for business logic layer, adhering to AR-001 and AR-002.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A | No violations identified | N/A |

---

## Phase 0: Research

*Skipped - all technical requirements are clearly specified in the feature spec and technical requirements section. No NEEDS CLARIFICATION items identified.*

### Decisions Resolved

| Item | Decision | Rationale |
|------|----------|-----------|
| ID generation strategy | Integer increment | Simpler than UUID, sufficient for single-user CLI, matches spec option |
| Task model | Python dataclass | Native to Python 3.13+, reduces boilerplate, supports type hints |
| CLI framework | argparse (stdlib) | No external dependencies required, sufficient for 5 commands |
| Storage structure | List of dicts/dataclasses | Simple in-memory structure, easy to iterate and filter |

## Phase 1: Design & Contracts

### Data Model Design

**Task Entity** (from spec: Key Entities section):

```python
from dataclasses import dataclass
from enum import Enum
from typing import Optional

class TaskStatus(Enum):
    PENDING = "Pending"
    COMPLETED = "Completed"

@dataclass
class Task:
    id: int
    title: str
    description: str
    status: TaskStatus
```

**Storage Design** (in-memory within TodoManager):

```python
class TodoManager:
    def __init__(self) -> None:
        self._tasks: list[Task] = []
        self._next_id: int = 1
```

### TodoManager CRUD Methods

```python
class TodoManager:
    def add_task(self, title: str, description: str = "") -> Task:
        """Add a new task with auto-incremented ID."""

    def list_tasks(self) -> list[Task]:
        """Return all tasks ordered by ID."""

    def get_task(self, task_id: int) -> Task | None:
        """Retrieve task by ID."""

    def update_task(self, task_id: int, title: str | None = None, description: str | None = None) -> Task | None:
        """Update task title and/or description by ID."""

    def delete_task(self, task_id: int) -> bool:
        """Delete task by ID. Returns True if deleted."""

    def toggle_complete(self, task_id: int) -> Task | None:
        """Toggle task status between Pending and Completed."""
```

### CLI Interface Design

**Command Structure** (using argparse subcommands):

```
$ todo add "Task title" "Task description"
$ todo list
$ todo update 1 --title "New title" --description "New desc"
$ todo complete 1
$ todo delete 1
```

**CLI Layer** (`src/cli/commands.py`):

```python
import argparse
from core.todo_manager import TodoManager

def add_command(args: argparse.Namespace, manager: TodoManager) -> None:
    """Handle 'add' subcommand."""

def list_command(args: argparse.Namespace, manager: TodoManager) -> None:
    """Handle 'list' subcommand."""

def update_command(args: argparse.Namespace, manager: TodoManager) -> None:
    """Handle 'update' subcommand."""

def complete_command(args: argparse.Namespace, manager: TodoManager) -> None:
    """Handle 'complete' subcommand."""

def delete_command(args: argparse.Namespace, manager: TodoManager) -> None:
    """Handle 'delete' subcommand."""
```

**Entry Point** (`main.py`):

```python
import argparse
from core.todo_manager import TodoManager

def main() -> None:
    manager = TodoManager()
    parser = create_parser()
    args = parser.parse_args()
    args.func(args, manager)
```

### Error Handling Strategy

| Condition | Handling Approach |
|-----------|-------------------|
| Empty title on add | Raise `ValueError("Title cannot be empty")` |
| Invalid task ID (update/delete/complete) | Raise `KeyError(f"Task {task_id} not found")` |
| Unexpected user input | argparse handles invalid arguments with help message |
| Keyboard interrupt (Ctrl+C) | Exit gracefully with message |

### Output Format

**List Command Output** (bullet point format per spec FR-011):

```
Tasks:
1. [Pending] Buy groceries
2. [Completed] Finish report
```

### Validation Rules

| Operation | Validation |
|-----------|------------|
| add_task | title must be non-empty string |
| update_task | task_id must exist; at least one of title/description provided |
| delete_task | task_id must exist |
| toggle_complete | task_id must exist |

---

## Generated Artifacts

### contracts/cli-commands.md

See `contracts/cli-commands.md` for detailed CLI command specifications.

### quickstart.md

See `quickstart.md` for development setup and usage guide.

### data-model.md

See `data-model.md` for complete entity definitions and validation rules.

---

**Plan Status**: ✅ Finalized
**Next Step**: Run `/sp.tasks` to generate actionable implementation tasks
