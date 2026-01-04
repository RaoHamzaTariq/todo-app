# UI Components

## Component Library

### Core Components

#### Button

Primary and secondary action buttons.

**Props:**
- `variant`: "primary" | "secondary" | "danger"
- `size`: "sm" | "md" | "lg"
- `disabled`: boolean
- `onClick`: () => void
- `children`: ReactNode

**Usage:**
```tsx
<Button variant="primary" onClick={handleSubmit}>
  Save Task
</Button>
```

---

#### Input

Text input field with label and error handling.

**Props:**
- `label`: string
- `name`: string
- `type`: "text" | "email" | "password"
- `value`: string
- `onChange`: (e) => void
- `error`: string | null
- `placeholder`: string
- `required`: boolean

**Usage:**
```tsx
<Input
  label="Task Title"
  name="title"
  value={formData.title}
  onChange={handleChange}
  required
/>
```

---

#### Textarea

Multi-line text input for descriptions.

**Props:**
- Same as Input
- `rows`: number (default: 3)
- `maxLength`: number

---

#### Checkbox

Checkbox for task completion toggle.

**Props:**
- `checked`: boolean
- `onChange`: (checked) => void
- `label`: string
- `disabled`: boolean

---

#### Card

Container for grouping related content.

**Props:**
- `children`: ReactNode
- `className`: string (optional)
- `padding`: "none" | "sm" | "md" | "lg"

---

### Task Components

#### TaskList

Container for displaying multiple tasks.

**Props:**
- `tasks`: Task[]
- `onToggleComplete`: (id) => void
- `onDelete`: (id) => void
- `onEdit`: (task) => void
- `loading`: boolean

**Usage:**
```tsx
<TaskList
  tasks={tasks}
  onToggleComplete={handleToggle}
  onDelete={handleDelete}
  onEdit={handleEdit}
/>
```

---

#### TaskItem

Individual task display with actions.

**Props:**
- `task`: Task
- `onToggleComplete`: () => void
- `onDelete`: () => void
- `onEdit`: () => void
- `isEditing`: boolean

**Features:**
- Checkbox for completion
- Edit and delete buttons
- Strikethrough when completed
- Hover actions

---

#### TaskForm

Form for creating and editing tasks.

**Props:**
- `task?`: Task (optional, for edit mode)
- `onSubmit`: (data) => void
- `onCancel`: () => void
- `loading`: boolean

**Fields:**
- Title (required)
- Description (optional)

---

### Auth Components

#### AuthForm

Authentication form for sign in/sign up.

**Props:**
- `mode`: "signin" | "signup"
- `onSubmit`: (data) => void
- `loading`: boolean
- `error`: string | null

**Fields:**
- Email (required, validated)
- Password (required, min 8 chars)

---

#### AuthProvider

Context provider for authentication state.

**Provides:**
- `session`: Session | null
- `signIn`: (email, password) => Promise<void>
- `signUp`: (email, password) => Promise<void>
- `signOut`: () => Promise<void>

---

### Layout Components

#### Header

Navigation header with user info and actions.

**Features:**
- App title/logo
- User avatar (if signed in)
- Sign out button
- Responsive design

---

#### Layout

Main page wrapper with header and content.

**Props:**
- `children`: ReactNode
- `showHeader`: boolean

---

## Styling Guidelines

- Use Tailwind CSS classes
- Follow color scheme from globals.css
- Maintain consistent spacing (4px grid)
- Use semantic colors:
  - Primary: brand color
  - Success: green tones
  - Danger: red tones
  - Warning: yellow/orange tones

## Related Specifications

- Task CRUD: `@specs/features/task-crud.md`
- Pages: `@specs/ui/pages.md`
