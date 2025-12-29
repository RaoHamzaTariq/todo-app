# Tasks: In-Memory Todo CLI

**Input**: Design documents from `specs/001-todo-cli/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), data-model.md, contracts/cli-commands.md

**Tests**: Tests are OPTIONAL - not explicitly requested in spec, but unit tests recommended for core logic per constitution.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Skill Use in all Phases: @python-cli-architect/SKILL.md

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths shown below assume single project

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project directory structure: src/cli/, src/core/, tests/
- [X] T002 Initialize uv project with Python 3.13+ in pyproject.toml
- [X] T003 [P] Create __init__.py files in src/cli/ and src/core/
- [X] T004 [P] Configure pyproject.toml with requires-python = ">=3.13" and todo script entry point

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**CRITICAL**: No user story work can begin until this phase is complete

- [X] T005 [P] Create TaskStatus enum in src/core/models.py with PENDING and COMPLETED values
- [X] T006 [P] Create Task dataclass in src/core/models.py with id, title, description, status fields
- [X] T007 Create TodoManager class skeleton in src/core/todo_manager.py with __init__ method
- [X] T008 Implement TodoManager._tasks (list) and _next_id (int) initialization in __init__
- [X] T009 [P] Create empty test file tests/test_todo_manager.py

**Checkpoint**: ✅ Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Add New Task (Priority: P1) 🎯 MVP

**Goal**: Users can add a new task with a title and optional description. Task is stored with unique ID and 'Pending' status.

**Independent Test**: Run `todo add "Buy groceries"` and verify task appears with ID 1 and 'Pending' status in `todo list`.

### Implementation for User Story 1

- [X] T010 [US1] Implement TodoManager.add_task() method in src/core/todo_manager.py
  - Signature: def add_task(self, title: str, description: str = "") -> Task
  - Validate title is non-empty (raise ValueError if empty)
  - Create Task with auto-incremented ID from _next_id
  - Set status to TaskStatus.PENDING
  - Append to _tasks list
  - Increment _next_id
  - Return created Task

- [X] T011 [US1] Implement add CLI command in src/cli/commands.py
  - Create add_command(args: argparse.Namespace, manager: TodoManager) -> None
  - Parse title (required) and description (optional) arguments
  - Call manager.add_task()
  - Print success message: "Added task {id}: {title}"

- [X] T012 [US1] Create argparse setup function in src/cli/commands.py
  - Create create_parser() function
  - Configure subparsers for add, list, update, complete, delete commands
  - Set up 'add' subcommand with title (positional) and description (optional) arguments

- [X] T013 [US1] Create main.py entry point
  - Import create_parser from src.cli.commands
  - Import TodoManager from src.core.todo_manager
  - Create main() function that parses args and calls appropriate command handler

**Definition of Done for US1**:
- [X] `todo add "Task title"` creates a task with unique ID
- [X] `todo add "Task title" "Description"` creates task with description
- [X] Empty title shows error message and task is not created
- [X] New tasks have 'Pending' status

**Checkpoint**: ✅ User Story 1 is fully functional and testable independently

---

## Phase 4: User Story 2 - View All Tasks (Priority: P1)

**Goal**: Users can see all tasks in a readable format with ID, title, and status.

**Independent Test**: After adding tasks with US1, run `todo list` and verify all tasks display correctly.

### Implementation for User Story 2

- [X] T014 [US2] Implement TodoManager.list_tasks() method in src/core/todo_manager.py
  - Signature: def list_tasks(self) -> list[Task]
  - Return all tasks ordered by ID ascending

- [X] T015 [US2] Implement list CLI command in src/cli/commands.py
  - Create list_command(args: argparse.Namespace, manager: TodoManager) -> None
  - Call manager.list_tasks()
  - Format output: "Tasks:\n1. [Pending] Buy groceries\n2. [Completed] Finish report"
  - Handle empty list case with helpful message

**Definition of Done for US2**:
- [X] `todo list` shows all tasks with ID, title, and status
- [X] Empty list shows "No tasks found" message
- [X] Format matches specification (bullet points or numbered list)

**Checkpoint**: ✅ User Stories 1 AND 2 work independently

---

## Phase 5: User Story 3 - Update Existing Task (Priority: P2)

**Goal**: Users can modify the title and/or description of an existing task by ID.

**Independent Test**: Add a task, run `todo update 1 --title "New title"`, verify changes in `todo list`.

### Implementation for User Story 3

- [X] T016 [US3] Implement TodoManager.get_task() method in src/core/todo_manager.py
  - Signature: def get_task(self, task_id: int) -> Task | None
  - Find and return task by ID, or None if not found

- [X] T017 [US3] Implement TodoManager.update_task() method in src/core/todo_manager.py
  - Signature: def update_task(self, task_id: int, title: str | None = None, description: str | None = None) -> Task | None
  - Find task by ID (raise KeyError if not found)
  - Validate at least one of title/description provided
  - Validate title is non-empty if provided
  - Update only provided fields (partial updates allowed)
  - Return updated Task or None

- [X] T018 [US3] Implement update CLI command in src/cli/commands.py
  - Create update_command(args: argparse.Namespace, manager: TodoManager) -> None
  - Parse task_id (positional), --title (optional), --description (optional)
  - Validate at least one of --title or --description provided
  - Call manager.update_task()
  - Print success message

**Definition of Done for US3**:
- [X] `todo update 1 --title "New title"` updates task title
- [X] `todo update 1 --description "New desc"` updates task description
- [X] `todo update 1 --title "New" --description "New desc"` updates both
- [X] Updating non-existent ID shows error
- [X] Providing empty title shows error

---

## Phase 6: User Story 4 - Complete Task (Priority: P2)

**Goal**: Users can mark a task as 'Completed' by ID. Toggling completes incomplete tasks.

**Independent Test**: Add a task, run `todo complete 1`, verify status changes from 'Pending' to 'Completed'.

### Implementation for User Story 4

- [X] T019 [US4] Implement TodoManager.toggle_complete() method in src/core/todo_manager.py
  - Signature: def toggle_complete(self, task_id: int) -> Task | None
  - Find task by ID (raise KeyError if not found)
  - Flip status: PENDING -> COMPLETED, COMPLETED -> PENDING
  - Return updated Task

- [X] T020 [US4] Implement complete CLI command in src/cli/commands.py
  - Create complete_command(args: argparse.Namespace, manager: TodoManager) -> None
  - Parse task_id (positional)
  - Call manager.toggle_complete()
  - Print success message

**Definition of Done for US4**:
- [X] `todo complete 1` marks task 1 as 'Completed'
- [X] Running complete on already completed task keeps it completed
- [X] Non-existent ID shows error

---

## Phase 7: User Story 5 - Delete Task (Priority: P3)

**Goal**: Users can remove a task from the list by ID.

**Independent Test**: Add tasks, run `todo delete 1`, verify task no longer appears in `todo list`.

### Implementation for User Story 5

- [X] T021 [US5] Implement TodoManager.delete_task() method in src/core/todo_manager.py
  - Signature: def delete_task(self, task_id: int) -> bool
  - Find task by ID
  - Remove from _tasks list
  - Return True if deleted, False if not found

- [X] T022 [US5] Implement delete CLI command in src/cli/commands.py
  - Create delete_command(args: argparse.Namespace, manager: TodoManager) -> None
  - Parse task_id (positional)
  - Call manager.delete_task()
  - Print success or "not found" message

**Definition of Done for US5**:
- [X] `todo delete 1` removes task 1 from the list
- [X] Task no longer appears in `todo list`
- [X] Non-existent ID shows error

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T023 [P] Add unit tests for TodoManager in tests/test_todo_manager.py
  - Test add_task with valid inputs
  - Test add_task with empty title (should raise ValueError)
  - Test list_tasks returns all tasks
  - Test update_task with valid inputs
  - Test update_task with non-existent ID
  - Test delete_task with valid ID
  - Test toggle_complete status change

- [ ] T024 [P] Add error handling for KeyError in CLI commands
  - Catch KeyError when task not found
  - Print user-friendly error message
  - Exit with code 1

- [ ] T025 Run quickstart.md validation - verify all commands work as documented

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-7)**: All depend on Foundational phase completion
  - User stories can proceed in priority order (US1 → US2 → US3 → US4 → US5)
  - All user stories depend only on Phase 2, not on each other
- **Polish (Phase 8)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (Add)**: Can start after Phase 2 - No dependencies on other stories
- **User Story 2 (View)**: Can start after Phase 2 - No dependencies on other stories
- **User Story 3 (Update)**: Can start after Phase 2 - No dependencies on other stories
- **User Story 4 (Complete)**: Can start after Phase 2 - No dependencies on other stories
- **User Story 5 (Delete)**: Can start after Phase 2 - No dependencies on other stories

### Within Each User Story

- Models (Task, TaskStatus) before TodoManager methods
- TodoManager methods before CLI commands
- CLI command handlers after their corresponding TodoManager methods
- Each story complete before moving to polish phase

### Parallel Opportunities

- Phase 1 tasks marked [P] can run in parallel
- Phase 2 tasks marked [P] can run in parallel
- User stories can proceed in parallel after Phase 2 (US1, US2, US3, US4, US5 are independent)
- Polish tasks marked [P] can run in parallel

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1 (Add New Task)
4. **STOP and VALIDATE**: Test add and list commands
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Demo (Add + List works!)
3. Add User Story 3 → Test independently → Demo (Update works!)
4. Add User Story 4 → Test independently → Demo (Complete works!)
5. Add User Story 2 → Test independently → Demo (All CRUD + View works!)
6. Add User Story 5 → Test independently → Demo (All features work!)
7. Polish → Final release

### Single Developer Strategy

1. Complete Setup (T001-T004)
2. Complete Foundational (T005-T009)
3. Implement US1 Add (T010-T013) → Test
4. Implement US2 View (T014-T015) → Test
5. Implement US3 Update (T016-T018) → Test
6. Implement US4 Complete (T019-T020) → Test
7. Implement US5 Delete (T021-T022) → Test
8. Polish (T023-T025) → Finalize

---

## Notes

- **[P] tasks** = different files, no dependencies - can be done in parallel
- **[Story] label** = maps task to specific user story for traceability
- Each user story should be independently completable and testable
- All code must include SDD task ID comment: `# SDD: Implements Task ID: T-XXX`
- All functions must have strict type hints per constitution
- All public classes and methods must have docstrings per constitution
