---
id: "004"
title: "Generate Todo CLI Tasks"
stage: "tasks"
date: "2025-12-29"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "001-todo-cli"
branch: "001-todo-cli"
user: "human"
command: "/sp.tasks"
labels: ["tasks","implementation","todo-cli","python"]
links:
  spec: "specs/001-todo-cli/spec.md"
  ticket: "null"
  adr: "null"
  pr: "null"
files:
  - "specs/001-todo-cli/tasks.md"
  - "specs/001-todo-cli/plan.md"
  - "specs/001-todo-cli/spec.md"
  - "specs/001-todo-cli/data-model.md"
  - "specs/001-todo-cli/contracts/cli-commands.md"
tests: []
---

## Prompt

Generate the tasks file for Phase 1: In-Memory Todo CLI.

Based on the approved speckit.plan, break the implementation down into small, sequential, and testable tasks. Ensure each task follows the 'One Task, One Goal' rule.

Required Task Breakdown Structure:

Project Scaffolding: Create the base directory structure, pyproject.toml (via uv), and the entry point script.

Data Modeling: Define the Task data class with proper type hints and status enums.

Core Logic (Manager): Implement the TodoManager class with methods for Add, List, Update, Delete, and Toggle Complete.

CLI Interface: Implement the user input loop or command parser to interact with the TodoManager.

Validation & Error Handling: Add logic to handle invalid inputs and edge cases (e.g., deleting a non-existent ID).

Final Integration: Ensure all components work together and the UI reflects the current state of the in-memory list.

Constraint: Each task must have a unique ID (e.g., T-001, T-002) and a clear 'Definition of Done'. Do not include any tasks for database persistence or external APIs as per the Phase 1 Constitution.

## Response snapshot

- Created tasks.md with 25 sequential, testable tasks
- Organized into 8 phases:
  - Phase 1: Setup (4 tasks) - project structure, uv init, pyproject.toml
  - Phase 2: Foundational (5 tasks) - Task model, TaskStatus enum, TodoManager skeleton
  - Phase 3: US1 Add New Task (4 tasks) - add_task method, add command, parser setup
  - Phase 4: US2 View All Tasks (2 tasks) - list_tasks method, list command
  - Phase 5: US3 Update Task (3 tasks) - get_task, update_task, update command
  - Phase 6: US4 Complete Task (2 tasks) - toggle_complete, complete command
  - Phase 7: US5 Delete Task (2 tasks) - delete_task, delete command
  - Phase 8: Polish (3 tasks) - unit tests, error handling, validation
- Each task has unique ID (T001-T025), clear file path, and Definition of Done
- All user stories marked with [US1], [US2], etc. labels
- Parallelizable tasks marked with [P]
- All tasks follow the strict checklist format: - [ ] ID [P?] [Story?] Description with path

## Outcome

- ✅ Impact: 25 actionable, testable tasks generated for Phase 1 implementation
- 🧪 Tests: N/A (task generation)
- 📁 Files: 1 created (specs/001-todo-cli/tasks.md)
- 🔁 Next prompts: /sp.implement to start coding with Task IDs
- 🧠 Reflection: Tasks successfully generated following SDD workflow

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
