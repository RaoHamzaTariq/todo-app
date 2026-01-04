# Pages

## Page Structure

```
src/app/
├── layout.tsx          # Root layout with providers
├── page.tsx            # Home / Dashboard
├── globals.css         # Global styles
├── api/
│   └── auth/
│       └── [...auth]/
│           └── route.ts    # Better Auth API routes
```

## Pages

### Home / Dashboard (`/`)

**Route:** `/`

**Access:** Authenticated users only

**Features:**
- Welcome message with user name
- Task summary (total, pending, completed)
- Quick add task button
- Recent tasks list
- Link to view all tasks

**Behavior:**
- Redirects to `/sign-in` if not authenticated
- Shows loading state while fetching data

---

### Sign In (`/sign-in`)

**Route:** `/sign-in`

**Access:** Unauthenticated users only

**Features:**
- Email and password fields
- "Remember me" option
- Sign in button
- Link to sign up page
- Error messages for invalid credentials

**Behavior:**
- Redirects to `/` on successful sign in
- Shows loading state during authentication

---

### Sign Up (`/sign-up`)

**Route:** `/sign-up`

**Access:** Unauthenticated users only

**Features:**
- Email and password fields
- Confirm password field
- Sign up button
- Link to sign in page
- Validation errors for existing email

**Behavior:**
- Redirects to `/sign-in` on successful registration
- Shows loading state during registration

---

### Tasks List (`/tasks`)

**Route:** `/tasks`

**Access:** Authenticated users only

**Features:**
- List of all tasks for current user
- Filter tabs: All | Pending | Completed
- Sort options: Created | Title | Updated
- Search bar (by title)
- "Add Task" button
- Empty state when no tasks

**Components:**
- `@specs/ui/components.md#TaskList`
- Filter controls
- Search input
- Add task button

---

### Task Detail (`/tasks/:id`)

**Route:** `/tasks/[id]`

**Access:** Authenticated users only

**Features:**
- Task details (title, description, status)
- Edit button
- Delete button
- Back to tasks link

**Components:**
- `@specs/ui/components.md#TaskItem` (read-only mode)

---

### Create Task (`/tasks/new`)

**Route:** `/tasks/new`

**Access:** Authenticated users only

**Features:**
- Task form (title, description)
- Create button
- Cancel button
- Validation errors

**Components:**
- `@specs/ui/components.md#TaskForm`

---

### Edit Task (`/tasks/:id/edit`)

**Route:** `/tasks/[id]/edit`

**Access:** Authenticated users only

**Features:**
- Pre-filled task form
- Save changes button
- Cancel button
- Validation errors

**Components:**
- `@specs/ui/components.md#TaskForm` (edit mode)

---

## Navigation Flow

```
Unauthenticated:
  / → /sign-in
  /sign-in → / (on success) or /sign-up
  /sign-up → /sign-in (on success)

Authenticated:
  / → /tasks
  /tasks → /tasks/new | /tasks/:id | /tasks/:id/edit
  /tasks/:id → /tasks/:id/edit | delete action
```

## Shared Layout

### Header

- App logo (links to `/tasks`)
- User name/avatar
- Sign out button

### Footer

- Simple copyright
- Links (optional)

## Error Pages

### 401 Unauthorized

- "Please sign in to access this page"
- Link to `/sign-in`

### 404 Not Found

- "Page not found"
- Link back to `/tasks`

### 500 Error

- "Something went wrong"
- Retry button

## Related Specifications

- Components: `@specs/ui/components.md`
- Task CRUD: `@specs/features/task-crud.md`
- Authentication: `@specs/features/authentication.md`
