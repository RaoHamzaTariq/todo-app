<!--
Sync Impact Report:
- Version change: 1.0.0 -> 1.1.0 (MINOR: new principles and expanded guidance)
- Enhanced principles:
  - I. Spec-Driven Development (SDD) - expanded with Laws 1-3
  - VI. Task ID Requirement - expanded with explicit Task ID mandate
- Added principles:
  - VII. Constitution Compliance Enforcement
  - VIII. Smallest Viable Change
- Updated sections: Technology Stack Constraints, Development Workflow, Governance
- Templates requiring updates: .specify/templates/plan-template.md (Constitution Check section OK - already references constitution)
- Templates validated: spec-template.md, tasks-template.md, phr-template.md (all align with SDD)
- Follow-up TODOs: None
-->
# Todo CLI Application Constitution

## Core Principles

### I. Spec-Driven Development (SDD)

All development MUST follow the SDD workflow sequence: `/sp.specify` -> `/sp.plan` -> `/sp.tasks` -> `/sp.implement`. This ensures traceable, aligned development.

**Law 1 - No Pre-Task Code Generation:**
- Never write a single line of `.py` code before the `/sp.tasks` file is finalized and exists
- If implementation is requested but `specs/<feature>/tasks.md` does not exist → **BLOCK** and guide user to complete the SDD workflow

**Law 2 - Task Reference Mandate:**
- Every code implementation MUST reference a specific Task ID from the corresponding `specs/<feature>/tasks.md`
- Code comments and PR descriptions must include: `# SDD: Implements Task ID: T-XXX`
- If user asks for code without task context → **BLOCK** and require task ID specification

**Law 3 - Constitution Pre-Check:**
- Before any feature work, check if it exists in `.specify/memory/constitution.md`
- If feature violates constitutional principles → **BLOCK** and surface the conflict
- If feature is not addressed in constitution → Suggest running `/sp.constitution` to add guidance

### II. Python 3.13+ Standard

Use Python 3.13+ with strict type hinting, PEP 8 standards, and functional programming principles where applicable. Leverage uv for package management to ensure consistent dependency handling.

### III. In-Memory Storage

Use in-memory storage only, with no external databases. This keeps the application lightweight and focused on core functionality without complex persistence concerns.

### IV. Core Feature Focus

Focus exclusively on the 5 core features: Add, View, Update, Delete, and Mark Complete. No additional features should be implemented during Phase 1.

### V. Code Quality Standards

Maintain strict type hinting, PEP 8 compliance, and functional programming principles. All code must be clean, well-documented, and testable.

### VI. Task ID Requirement

Every code change MUST be associated with a specific Task ID from the tasks.md file. This ensures traceability and prevents unauthorized feature creep. All implementations must include a comment: `# SDD: Implements Task ID: T-XXX`.

### VII. Constitution Compliance Enforcement

Before saving any code:
1. Verify implementation does not violate `.specify/memory/constitution.md` principles
2. Confirm code follows defined code standards
3. Ensure no secrets hardcoded (uses `.env` per constitution)
4. Validate implementation is the smallest viable change
5. Check code includes proper file references and Task ID comment

### VIII. Smallest Viable Change

All implementations must be the smallest viable change per task requirements. Avoid refactoring unrelated code, adding premature features, or making architectural changes outside the planned scope. Changes should be focused, testable, and directly address the Task ID.

## Technology Stack Constraints

Tech Stack: Python 3.13+, uv for package management, and no external databases (In-Memory only). No additional dependencies should be introduced without explicit approval.

## Development Workflow

All development must follow the SDD sequence: Specify -> Plan -> Tasks -> Implement. The agent must reject any request to implement code that hasn't been through the `/sp.plan` and `/sp.tasks` phase.

### Pre-Implementation Checklist

Before writing any code:
1. Read the specific task from tasks.md
2. Read constitution.md
3. Run "Constitution Alignment Check":
   - Does this implementation violate any principle?
   - Does it follow code standards?
   - Is it the smallest viable change?
4. If alignment fails → **DO NOT SAVE** → Surface violation with specific principle reference
5. If alignment passes → Proceed with implementation

### Error Handling

| Condition | Action |
|-----------|--------|
| `tasks.md` missing | Redirect to `/sp.specify` -> `/sp.plan` -> `/sp.tasks` |
| `tasks.md` not finalized | Check for "Status: finalized", if absent request confirmation |
| No Task ID provided | Block and request specific Task ID |
| Task ID not found in `tasks.md` | Surface: "Task ID T-XXX not found in specs/<feature>/tasks.md" |
| Constitution conflict | Halt with principle citation and resolution requirement |
| Code fails alignment check | Do not save, surface violation, propose fix |

## Governance

All development must comply with the SDD principles. Amendments to this constitution require explicit approval. All pull requests must verify compliance with these principles before merging. Code reviews must check for proper Task ID references.

### Versioning Policy

- **MAJOR**: Backward incompatible governance/principle removals or redefinitions
- **MINOR**: New principle/section added or materially expanded guidance
- **PATCH**: Clarifications, wording, typo fixes, non-semantic refinements

### Compliance Review

Constitution compliance is verified at:
1. Feature specification phase (`/sp.specify`) - Validate scope against Core Feature Focus
2. Planning phase (`/sp.plan`) - Constitution Check before design
3. Task generation (`/sp.tasks`) - Ensure all tasks reference plan sections
4. Implementation (`/sp.implement`) - Task ID validation and alignment check
5. Code reviews - Verify Task ID comments and principle adherence

**Version**: 1.1.0 | **Ratified**: 2025-12-28 | **Last Amended**: 2025-12-29
