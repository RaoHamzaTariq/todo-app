# Feature Specification: In-Memory Todo CLI

**Feature Branch**: `001-todo-cli`
**Created**: 2025-12-28
**Status**: Draft
**Input**: User description: "to create the functional requirements for Phase 1: In-Memory Todo CLI.

Include the following specifications:

User Personas: A developer who needs a quick command-line tool to manage tasks.

Core Features:

 - Add Task: User can provide a title and a description.
 - List Tasks: Display all tasks with an ID, status (Pending/Completed), and title.
 - Update Task: Modify the title or description of an existing task by ID.
 - Delete Task: Remove a task from the list using its ID.
 - Complete Task: Toggle the status of a task to 'Completed'
 - Data Requirements: Define a Task object with fields: id (UUID or Integer), title (String), description (String), and status (Boolean/Enum).
 - Non-Functional Requirements: > * The application must start instantly.
 - Data should persist only during the session (In-Memory).
 - The CLI should have clear, readable output (use simple tables or bullet points).
 - Validation: Ensure titles cannot be empty and IDs must exist for updates/deletions."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Add New Task (Priority: P1)

A developer wants to quickly add a new task to their todo list to keep track of work items.

**Why this priority**: This is the foundational functionality that enables all other use cases - without the ability to add tasks, the application has no value.

**Independent Test**: Can be fully tested by running the add task command with a title and description, and verifying that the task appears in the list with a unique ID and 'Pending' status.

**Acceptance Scenarios**:

1. **Given** the application is running, **When** the user adds a task with a title and description, **Then** the task is stored with a unique ID and 'Pending' status
2. **Given** the application is running, **When** the user adds a task with only a title, **Then** the task is stored with a unique ID, the provided title, an empty description, and 'Pending' status
3. **Given** the application is running, **When** the user attempts to add a task with an empty title, **Then** an error message is displayed and no task is created

---

### User Story 2 - View All Tasks (Priority: P1)

A developer wants to see all their tasks to understand what needs to be done and what has been completed.

**Why this priority**: This is the core viewing functionality that allows users to interact with their data and understand their workload.

**Independent Test**: Can be fully tested by adding tasks and then running the list command to verify all tasks are displayed with correct ID, status, and title.

**Acceptance Scenarios**:

1. **Given** there are tasks in the system, **When** the user requests to list all tasks, **Then** all tasks are displayed in a readable format with ID, title, and status clearly visible
2. **Given** there are no tasks in the system, **When** the user requests to list all tasks, **Then** an appropriate message is displayed indicating no tasks exist

---

### User Story 3 - Update Existing Task (Priority: P2)

A developer wants to modify the details of an existing task when requirements change or more information becomes available.

**Why this priority**: Allows users to maintain accurate task information, which is important for effective task management.

**Independent Test**: Can be fully tested by adding a task, updating its details, and then listing tasks to verify the changes were applied.

**Acceptance Scenarios**:

1. **Given** a task exists in the system, **When** the user updates the task title and description by ID, **Then** the task details are modified and the status remains unchanged
2. **Given** a task exists in the system, **When** the user updates only the title by ID, **Then** only the title is modified and other fields remain unchanged
3. **Given** no task exists with the specified ID, **When** the user attempts to update a task by that ID, **Then** an error message is displayed and no changes are made

---

### User Story 4 - Complete Task (Priority: P2)

A developer wants to mark tasks as completed when they finish working on them.

**Why this priority**: Critical for tracking progress and maintaining an accurate view of what work remains.

**Independent Test**: Can be fully tested by adding a task, marking it as complete, and then listing tasks to verify the status changed from 'Pending' to 'Completed'.

**Acceptance Scenarios**:

1. **Given** a task exists with 'Pending' status, **When** the user marks the task as complete by ID, **Then** the task status changes to 'Completed'
2. **Given** a task exists with 'Completed' status, **When** the user marks the task as complete by ID, **Then** the task status remains 'Completed'
3. **Given** no task exists with the specified ID, **When** the user attempts to complete a task by that ID, **Then** an error message is displayed and no changes are made

---

### User Story 5 - Delete Task (Priority: P3)

A developer wants to remove tasks that are no longer relevant or needed.

**Why this priority**: Allows users to maintain a clean, relevant list of tasks by removing obsolete items.

**Independent Test**: Can be fully tested by adding tasks, deleting one, and then listing tasks to verify the deleted task is no longer present.

**Acceptance Scenarios**:

1. **Given** a task exists in the system, **When** the user deletes the task by ID, **Then** the task is removed from the system
2. **Given** no task exists with the specified ID, **When** the user attempts to delete a task by that ID, **Then** an error message is displayed and no changes are made

---

### Edge Cases

- What happens when a user tries to add a task with a very long title or description?
- How does system handle invalid or malformed task IDs in update/delete operations?
- What happens when a user tries to perform operations on the task list while another operation is in progress?


## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST allow users to add a new task with a title and optional description
- **FR-002**: System MUST assign a unique identifier to each task upon creation
- **FR-003**: System MUST store tasks in memory with fields: id, title, description, and status
- **FR-004**: System MUST display all tasks with their ID, title, and status in a readable format
- **FR-005**: System MUST allow users to update the title and description of an existing task by ID
- **FR-006**: System MUST allow users to mark a task as 'Completed' by ID
- **FR-007**: System MUST allow users to delete a task by ID
- **FR-008**: System MUST validate that task titles cannot be empty when adding a new task
- **FR-009**: System MUST validate that the specified task ID exists before performing update, delete, or complete operations
- **FR-010**: System MUST maintain data only during the current session (in-memory persistence)
- **FR-011**: System MUST provide clear, readable output using tables or bullet points for task listings

### Key Entities

- **Task**: The primary data entity representing a todo item with the following attributes:
  - id: Unique identifier (integer or UUID) for the task
  - title: Required string representing the task name
  - description: Optional string providing additional details about the task
  - status: Enum or boolean indicating if the task is 'Pending' or 'Completed'

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can add a new task in under 2 seconds from command execution
- **SC-002**: Users can view all tasks with clear formatting and readable layout that displays all required information (ID, title, status)
- **SC-003**: 100% of valid operations (add, list, update, delete, complete) execute successfully without errors
- **SC-004**: Application starts instantly with no noticeable delay when launched from command line
- **SC-005**: 95% of users can successfully complete basic task management operations without requiring documentation

## Technical Requirements *(mandatory)*

### Python Implementation Standards

- **PIR-001**: All Python code MUST target Python 3.13+ syntax and features
- **PIR-002**: Dependency management MUST use `uv` exclusively - reject any `pip` or `poetry` suggestions
- **PIR-003**: `pyproject.toml` must be configured with `requires-python = ">=3.13"`
- **PIR-004**: All functions MUST have strict type hints on parameters and return values
- **PIR-005**: All code MUST comply with PEP 8 standards (line length ≤ 88 characters)
- **PIR-006**: Imports MUST be sorted and grouped (stdlib, third-party, local)
- **PIR-007**: All public classes and methods MUST include docstrings

### Architectural Requirements

- **AR-001**: Project MUST use modular architecture with clear separation of concerns:
  - `src/cli/` - UI layer for CLI input/output, argument parsing, output formatting
  - `src/core/` - Business logic layer for domain operations and in-memory state
- **AR-002**: Business logic layer MUST have NO CLI dependencies
- **AR-003**: CLI layer MUST have NO direct data persistence logic
- **AR-004**: REJECT monolithic single-file implementations
- **AR-005**: Core logic MUST be 100% testable (pure functions where possible, no side effects)

### Storage Requirements

- **SR-001**: Data MUST be stored in-memory using Python lists or dictionaries
- **SR-002**: REJECT SQLite, PostgreSQL, or any external database proposals in Phase 1
- **SR-003**: REJECT any external API or network calls in Phase 1
- **SR-004**: Data persists only during the current session

### Required Project Structure

```
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
