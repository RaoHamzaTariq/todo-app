# Tasks: Phase 2 Full-Stack Todo Application

**Input**: Design documents from `/specs/002-phase2-fullstack/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, quickstart.md

**Tests**: Not explicitly requested - implementation-focused tasks only

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

**Skills Referenced**:
- `better-auth-specialist`: JWT configuration, token verification, user_id validation
- `auth-security-specialist`: JWT middleware, stateless verification, Bearer token patterns
- `data-ownership-enforcer`: User isolation, ownership verification, 403/404 error handling
- `api-contract-steward`: RESTful endpoint design, OpenAPI contracts, response schemas
- `monorepo-architect`: Frontend/backend separation, independent package management
- `clean-code-pythonist`: Python code quality, type hints, PEP 8 compliance

## Website UI Guidelines

### Responsive Design
- Mobile-first approach with responsive breakpoints
- Support for mobile, tablet, and desktop viewports
- Touch-friendly controls and adequate tap targets
- Responsive navigation patterns

### Accessibility (a11y)
- Semantic HTML structure
- Proper heading hierarchy (h1, h2, h3, etc.)
- ARIA labels and roles where appropriate
- Keyboard navigation support
- Sufficient color contrast ratios
- Focus indicators for interactive elements

### User Experience (UX)
- Clear visual hierarchy and information architecture
- Consistent design patterns throughout the application
- Loading states and skeleton screens for better perceived performance
- Form validation with clear error messaging
- Confirmation dialogs for destructive actions (deletion)
- Success feedback for user actions

### Navigation
- Intuitive navigation with clear breadcrumbs
- Consistent header/navigation across pages
- Proper handling of authentication state in navigation
- Back button support and browser history management

### Forms
- Input validation with immediate feedback
- Clear labeling of form fields
- Appropriate input types for different data (email, password, etc.)
- Loading states during form submission
- Error handling and recovery

### Error Handling
- Graceful error states and recovery options
- User-friendly error messages
- Proper 404 and 500 error pages
- Network error handling with retry mechanisms

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure for both frontend and backend

### Backend Setup

- [X] T001 Create backend project structure per plan.md in `backend/src/`
- [X] T002 [P] Create `backend/pyproject.toml` with Python 3.13+ and dependencies (fastapi, sqlmodel, python-jose, psycopg, uvicorn)
- [X] T003 [P] Create `backend/.env` template with DATABASE_URL, BETTER_AUTH_SECRET, JWT_ALGORITHM, ENVIRONMENT
- [X] T004 [P] Create `backend/src/main.py` FastAPI entry point with startup event

### Frontend Setup

- [X] T005 Run `npx create-next-app@latest . --typescript --tailwind --eslint --app --src-dir --import-alias "@/*" --no-turbopack` to initialize Next.js 16+ project in `frontend/`
- [X] T006 [P] Install Better Auth dependencies: `cd frontend && npm install better-auth`
- [X] T007 [P] Create `frontend/.env.local` template with NEXT_PUBLIC_API_URL, BETTER_AUTH_SECRET, DATABASE_URL

### Root Configuration

- [X] T008 [P] Create `docker-compose.yml` for local development orchestration

**Phase 1 Checkpoint**: Project structure ready with all dependencies configured

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**CRITICAL**: No user story work can begin until this phase is complete

### Database Infrastructure

- [X] T009 Create `backend/src/app/database.py` with SQLModel engine configuration for Neon PostgreSQL
- [X] T010 [P] Create `backend/src/app/config.py` environment validation and settings class

### Authentication Framework (Backend)

- [X] T011 Create `backend/src/app/middleware/__init__.py` middleware package
- [X] T012 Create `backend/src/app/middleware/auth.py` JWTBearer class for token verification using python-jose
- [X] T013 [P] Create `backend/src/app/schemas/error.py` ErrorResponse schema for structured JSON errors

### Authentication Framework (Frontend)

- [X] T014 Create `frontend/src/lib/auth-client.ts` Better Auth client with jwtClient() plugin
- [X] T015 [P] Create `frontend/src/lib/config.ts` environment validation for frontend config

### API Routes (Frontend)

- [X] T016 Create `frontend/src/app/api/tasks/route.ts` Next.js API route for task CRUD operations (GET, POST)
- [X] T017 [P] Create `frontend/src/types/task.ts` TypeScript types for Task entities

### Base Models

- [X] T018 Create `backend/src/app/models/__init__.py` models package
- [X] T019 [P] Create `backend/src/app/models/user.py` User model reference (managed by Better Auth)
- [X] T020 [P] Create `backend/src/app/models/task.py` Task SQLModel with all indexes per data-model.md

### Base Schemas

- [X] T021 Create `backend/src/app/schemas/__init__.py` schemas package
- [X] T022 Create `backend/src/app/schemas/task.py` Pydantic schemas (CreateTaskInput, UpdateTaskInput, TaskResponse)

### Router Structure

- [X] T023 Create `backend/src/app/routers/__init__.py` routers package
- [X] T024 [P] Create `backend/src/app/routers/tasks.py` Task router with CRUD endpoints (placeholder stubs)

### Application Initialization

- [X] T025 Update `backend/src/main.py` to include all routers and call init_db() on startup
- [X] T026 [P] Create `frontend/src/app/layout.tsx` root layout with auth providers
- [X] T027 Create `frontend/src/middleware.ts` Next.js middleware for route protection

**Phase 2 Checkpoint**: Foundation ready - JWT authentication, database connection, and base models are complete. User story implementation can now begin.

---

## Phase 3: User Story 1 - User Authentication (Priority: P1) :mvp:

**Goal**: Users can create accounts, sign in, and sign out. Route protection ensures unauthenticated users are redirected.

**Independent Test**: Sign up with valid credentials, sign out, sign back in, verify session persists and subsequent API calls work with JWT token.

**Skills**: `better-auth-specialist`, `auth-security-specialist`

### Frontend Authentication UI

- [X] T028 [P] [US1] Create `frontend/src/app/(auth)/sign-in/page.tsx` sign-in page with email/password form
- [X] T029 [P] [US1] Create `frontend/src/app/(auth)/sign-up/page.tsx` sign-up page with email/password form
- [X] T030 [US1] Create `frontend/src/components/AuthForm.tsx` reusable authentication form component
- [X] T031 [US1] Create `frontend/src/components/Header.tsx` header with user menu and sign-out button

### Frontend Auth Integration

- [X] T032 [US1] Implement sign-up handler in `frontend/src/lib/auth-client.ts` using better-auth signUp.email()
- [X] T033 [US1] Implement sign-in handler in `frontend/src/lib/auth-client.ts` using better-auth signIn.email()
- [X] T034 [US1] Implement sign-out handler in `frontend/src/lib/auth-client.ts` using better-auth signOut()
- [X] T035 [US1] Update `frontend/src/middleware.ts` to protect /tasks routes and redirect to /sign-in
- [X] T036 [US1] Update `frontend/src/app/(auth)/sign-in/page.tsx` to redirect authenticated users to /tasks
- [X] T037 [US1] Update `frontend/src/app/(auth)/sign-up/page.tsx` to redirect authenticated users to /tasks

### Frontend API Integration

- [X] T038 [US1] Update Next.js API routes to get JWT token from Better Auth using authClient.token()
- [X] T039 [US1] Add 401 handling in Next.js API routes to redirect to /sign-in on token expiration

### Backend JWT Verification

- [X] T040 [US1] Implement JWT token decoding in `backend/src/app/middleware/auth.py` with exp validation
- [X] T041 [US1] Update `backend/src/app/middleware/auth.py` to extract user_id from JWT claims

**Phase 3 Checkpoint**: User can sign up, sign in, and sign out. Unauthenticated access to /tasks redirects to sign-in. JWT tokens are validated on all backend requests.

---

## Phase 4: User Story 2 - Create Tasks (Priority: P1) :mvp:

**Goal**: Authenticated users can create new tasks with a title and optional description.

**Independent Test**: Sign in, click "Add Task", enter title and description, verify task appears in user's task list with correct data.

**Skills**: `data-ownership-enforcer`, `api-contract-steward`

### Backend Task Service

- [X] T042 [US2] Create `backend/src/app/services/__init__.py` services package
- [X] T043 [US2] Create `backend/src/app/services/task_service.py` with create_task() function (uses user_id from JWT, not request body)

### Backend Task Endpoints

- [X] T044 [US2] Implement POST `/{user_id}/tasks` endpoint in `backend/src/app/routers/tasks.py`
- [X] T045 [US2] Add request validation in POST endpoint using CreateTaskInput schema
- [X] T046 [US2] Add ownership verification: reject if user_id in path != user_id in JWT token
- [X] T047 [US2] Add error handling for validation errors (400) and ownership violations (403)

### Frontend Task Types

- [X] T048 [US2] Create `frontend/src/types/api.ts` with CreateTaskInput interface

### Frontend Task Components

- [X] T049 [P] [US2] Create `frontend/src/components/TaskForm.tsx` form with title (required) and description (optional)
- [X] T050 [P] [US2] Create `frontend/src/app/tasks/new/page.tsx` new task page using TaskForm

### Frontend API Integration

- [X] T051 [US2] Update `frontend/src/app/api/tasks/route.ts` with POST handler for createTask
- [X] T052 [US2] Implement create task submission in `frontend/src/components/TaskForm.tsx` using Next.js fetch to API route
- [X] T053 [US2] Add form validation: title required (1-200 chars), description optional (max 1000 chars)

**Phase 4 Checkpoint**: User can create tasks with title and optional description. Tasks are owned by authenticated user. Validation errors shown for invalid input.

---

## Phase 5: User Story 3 - View Tasks (Priority: P1) :mvp:

**Goal**: Authenticated users can view their tasks with title, description, and completion status.

**Independent Test**: Sign in, verify only authenticated user's tasks are displayed, not other users' tasks. Empty state shown when no tasks exist.

**Skills**: `data-ownership-enforcer`, `api-contract-steward`

### Backend Task List Endpoint

- [X] T054 [US3] Implement GET `/{user_id}/tasks` endpoint in `backend/src/app/routers/tasks.py`
- [X] T055 [US3] Add query to return only tasks where task.user_id == auth_user["user_id"]
- [X] T056 [US3] Implement empty list response with guidance message for no tasks

### Backend Single Task Endpoint

- [X] T057 [US3] Implement GET `/{user_id}/tasks/{id}` endpoint in `backend/src/app/routers/tasks.py`
- [X] T058 [US3] Add ownership verification: return 404 (not 403) if task belongs to different user

### Frontend Task List

- [X] T059 [P] [US3] Create `frontend/src/components/TaskList.tsx` task list component
- [X] T060 [P] [US3] Create `frontend/src/components/TaskItem.tsx` individual task display component
- [X] T061 [US3] Create `frontend/src/app/tasks/page.tsx` task list page showing all user's tasks

### Frontend API Integration

- [X] T062 [US3] Update `frontend/src/app/api/tasks/route.ts` with GET handler for getTasks
- [X] T063 [US3] Update `frontend/src/app/api/tasks/[id]/route.ts` with GET handler for getTask
- [X] T064 [US3] Implement task fetching in `frontend/src/app/tasks/page.tsx` using React Suspense

**Phase 5 Checkpoint**: User can view all their tasks. Only owned tasks shown (no data leakage). Empty state displayed when no tasks exist.

---

## Phase 6: User Story 4 - Update Tasks (Priority: P2)

**Goal**: Authenticated users can edit existing task title and description.

**Independent Test**: Sign in, edit existing task's title and description, verify changes are saved and reflected in task list.

**Skills**: `data-ownership-enforcer`, `api-contract-steward`

### Backend Update Endpoint

- [X] T065 [US4] Implement PUT `/{user_id}/tasks/{id}` endpoint in `backend/src/app/routers/tasks.py`
- [X] T066 [US4] Add request validation using UpdateTaskInput schema (optional title/description)
- [X] T067 [US4] Add ownership verification: return 404 if task not found OR belongs to different user
- [X] T068 [US4] Add immutable field check: prevent changing user_id on update

### Backend Update Service

- [X] T069 [US4] Implement update_task() function in `backend/src/app/services/task_service.py`

### Frontend Edit Page

- [X] T070 [P] [US4] Create `frontend/src/app/tasks/[id]/page.tsx` task detail page
- [X] T071 [P] [US4] Create `frontend/src/app/tasks/[id]/edit/page.tsx` edit task page with pre-filled TaskForm

### Frontend API Integration

- [X] T072 [US4] Update `frontend/src/app/api/tasks/[id]/route.ts` with PUT handler for updateTask
- [X] T073 [US4] Update `frontend/src/components/TaskForm.tsx` to support edit mode with pre-filled values
- [X] T074 [US4] Update `frontend/src/components/TaskItem.tsx` to include edit button linking to edit page

**Phase 6 Checkpoint**: User can edit task title and description. Changes persist and display in task list. Editing other user's tasks returns 404.

---

## Phase 7: User Story 5 - Delete Tasks (Priority: P2)

**Goal**: Authenticated users can delete their tasks with confirmation.

**Independent Test**: Sign in, delete existing task, verify task is removed from list and cannot be accessed again.

**Skills**: `data-ownership-enforcer`, `api-contract-steward`

### Backend Delete Endpoint

- [X] T075 [US5] Implement DELETE `/{user_id}/tasks/{id}` endpoint in `backend/src/app/routers/tasks.py`
- [X] T076 [US5] Add ownership verification: return 404 if task not found OR belongs to different user
- [X] T077 [US5] Implement permanent deletion (no soft delete in Phase 2)

### Backend Delete Service

- [X] T078 [US5] Implement delete_task() function in `backend/src/app/services/task_service.py`

### Frontend Delete Confirmation

- [X] T079 [P] [US5] Create `frontend/src/components/DeleteConfirmation.tsx` confirmation dialog component
- [X] T080 [P] [US5] Update `frontend/src/components/TaskItem.tsx` to include delete button with confirmation

### Frontend API Integration

- [X] T081 [US5] Update `frontend/src/app/api/tasks/[id]/route.ts` with DELETE handler for deleteTask
- [X] T082 [US5] Implement delete handler in `frontend/src/components/TaskItem.tsx` with confirmation dialog

**Phase 7 Checkpoint**: User can delete tasks with confirmation. Deleted tasks removed from list. Deleting other user's tasks returns 404.

---

## Phase 8: User Story 6 - Toggle Task Completion (Priority: P2)

**Goal**: Authenticated users can mark tasks as complete or incomplete to track progress.

**Independent Test**: Sign in, toggle task completion status, verify status changes and persists.

**Skills**: `data-ownership-enforcer`, `api-contract-steward`

### Backend Toggle Endpoint

- [X] T083 [US6] Implement PATCH `/{user_id}/tasks/{id}/complete` endpoint in `backend/src/app/routers/tasks.py`
- [X] T084 [US6] Toggle completion status: if completed=true then set to false, and vice versa
- [X] T085 [US6] Add ownership verification: return 404 if task not found OR belongs to different user

### Backend Toggle Service

- [X] T086 [US6] Implement toggle_complete() function in `backend/src/app/services/task_service.py`

### Frontend Toggle UI

- [X] T087 [US6] Update `frontend/src/components/TaskItem.tsx` with completion checkbox/toggle button
- [X] T088 [US6] Update `frontend/src/components/TaskItem.tsx` with visual indication for completed tasks (strikethrough/styled)

### Frontend API Integration

- [ ] T089 [US6] Update `frontend/src/app/api/tasks/[id]/complete/route.ts` with PATCH handler for toggleComplete
- [ ] T090 [US6] Implement toggle handler in `frontend/src/components/TaskItem.tsx`

**Phase 8 Checkpoint**: User can toggle task completion. Status changes persist. Visual feedback shows completed vs incomplete tasks.

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

### Error Handling & Logging

- [X] T091 [P] Add structured logging across all backend endpoints in `backend/src/app/routers/tasks.py`
- [X] T092 [P] Add error handling middleware in `backend/src/main.py` for unhandled exceptions

### UI Polish

- [X] T093 [P] Add `frontend/src/app/globals.css` global styles for consistent styling
- [X] T094 [P] Create `frontend/src/components/ui/Button.tsx` reusable button component
- [X] T095 [P] Create `frontend/src/components/ui/Input.tsx` reusable input component
- [X] T096 [P] Create `frontend/src/components/ui/Card.tsx` reusable card component for task items

### Responsive Design

- [X] T097 [P] Ensure all pages render correctly on mobile, tablet, and desktop viewports
- [X] T098 [P] Add responsive styles to `frontend/src/app/tasks/page.tsx` and task components

### Performance

- [X] T099 Add loading states to all frontend pages using Next.js loading.tsx
- [X] T100 [P] Add error boundaries with `frontend/src/app/error.tsx` for graceful error handling

### Documentation

- [X] T101 Update `README.md` with full-stack setup and usage instructions
- [X] T102 Verify `quickstart.md` instructions match implemented code

### Validation & Security

- [X] T103 Add title length validation (max 200 chars) on backend
- [X] T104 Add description length validation (max 1000 chars) on backend
- [X] T105 Verify 100% user data isolation: all endpoints filter by user_id from JWT only

**Final Checkpoint**: All user stories complete and functional. Application ready for testing against quickstart.md scenarios.

---

## Dependencies & Execution Order

### Phase Dependencies

| Phase | Depends On | Blocks |
|-------|------------|--------|
| Phase 1: Setup | None | Phase 2 |
| Phase 2: Foundational | Phase 1 | All User Stories |
| Phase 3: User Story 1 | Phase 2 | US1 only |
| Phase 4: User Story 2 | Phase 2 | US2 only |
| Phase 5: User Story 3 | Phase 2 | US3 only |
| Phase 6: User Story 4 | Phase 2 | US4 only |
| Phase 7: User Story 5 | Phase 2 | US5 only |
| Phase 8: User Story 6 | Phase 2 | US6 only |
| Phase 9: Polish | All Phases 3-8 | Release |

### User Story Dependencies

| User Story | Priority | Dependencies | Independent Test |
|------------|----------|--------------|------------------|
| US1: Authentication | P1 | Phase 2 | Sign up → Sign out → Sign in → Verify session |
| US2: Create Tasks | P1 | Phase 2 + US1 | Create task → Verify appears in list |
| US3: View Tasks | P1 | Phase 2 + US1 + US2 | View tasks → Verify owned tasks only |
| US4: Update Tasks | P2 | Phase 2 + US1 + US2 + US3 | Edit task → Verify changes persist |
| US5: Delete Tasks | P2 | Phase 2 + US1 + US2 + US3 | Delete task → Verify removed from list |
| US6: Toggle Complete | P2 | Phase 2 + US1 + US2 + US3 | Toggle status → Verify visual change |

### Within Each User Story

- Models (T018-T020) before services (T042-T043, T069, etc.)
- Services before endpoints (T044-T047, T054-T058, etc.)
- Backend endpoints before frontend integration
- Core implementation before error handling polish

---

## Parallel Execution Examples

### User Story 1 Can Run in Parallel

```bash
# All authentication UI components
Task: T028 - Create sign-in page
Task: T029 - Create sign-up page
Task: T030 - Create AuthForm component
Task: T031 - Create Header component
```

### User Story 2 Can Run in Parallel

```bash
# Backend service and endpoint
Task: T042 - Create task_service.py
Task: T044 - Implement POST tasks endpoint

# Frontend form and API
Task: T049 - Create TaskForm component
Task: T051 - Add createTask to Next.js API route
```

### Foundational Tasks Can Run in Parallel

```bash
# All [P] marked tasks in Phase 2 can execute simultaneously
Task: T010 - Create config.py
Task: T012 - Create auth middleware
Task: T014 - Create auth-client.ts
Task: T016 - Create Next.js API route for tasks
Task: T019 - Create user model
Task: T020 - Create task model
```

---

## Implementation Strategy

### MVP First (User Story 1-3 Only)

1. Complete Phase 1: Setup (T001-T008)
2. Complete Phase 2: Foundational (T009-T027)
3. Complete Phase 3: User Story 1 (T028-T041)
4. Complete Phase 4: User Story 2 (T042-T053)
5. Complete Phase 5: User Story 3 (T054-T064)
6. **STOP and VALIDATE**: Test authentication + create + view workflows
7. Deploy/demo MVP

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (Authentication!)
3. Add User Story 2 → Test independently → Deploy/Demo (Create Tasks!)
4. Add User Story 3 → Test independently → Deploy/Demo (View Tasks!)
5. Add User Story 4 → Test independently → Deploy/Demo (Edit Tasks!)
6. Add User Story 5 → Test independently → Deploy/Demo (Delete Tasks!)
7. Add User Story 6 → Test independently → Deploy/Demo (Toggle Complete!)
8. Polish → Final Release

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together (1-2 days)
2. Once Foundational is done:
   - Developer A: User Story 1 (Authentication)
   - Developer B: User Story 2 (Create Tasks)
   - Developer C: User Story 3 (View Tasks)
3. Stories complete and integrate independently

---

## Task Summary

| Phase | Task Count | Description |
|-------|------------|-------------|
| Phase 1: Setup | 8 | Project structure, dependencies, configuration |
| Phase 2: Foundational | 19 | Database, auth framework, base models, schemas |
| Phase 3: US1: Authentication | 14 | Sign up, sign in, sign out, route protection |
| Phase 4: US2: Create Tasks | 12 | Task creation endpoint, form, validation |
| Phase 5: US3: View Tasks | 11 | Task list endpoint, list and detail pages |
| Phase 6: US4: Update Tasks | 10 | Task edit endpoint, edit page, update API |
| Phase 7: US5: Delete Tasks | 8 | Task delete endpoint, confirmation dialog |
| Phase 8: US6: Toggle Complete | 8 | Toggle endpoint, visual indicator, toggle API |
| Phase 9: Polish | 15 | Error handling, UI polish, responsive design |
| **Total** | **105** | |

**Parallelizable Tasks**: Tasks marked with [P] can execute in parallel within their phases

**MVP Scope**: Phases 1-5 (Tasks T001-T064) deliver core authentication and task CRUD functionality
