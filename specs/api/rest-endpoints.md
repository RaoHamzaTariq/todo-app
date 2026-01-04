# REST API Endpoints

## Base URL

- Development: `http://localhost:8000`
- Production: `https://api.example.com`

## Authentication

All endpoints require JWT token in header:
```
Authorization: Bearer <token>
```

Without valid token: Returns `401 Unauthorized`

## Endpoints

### GET /api/{user_id}/tasks

List all tasks for authenticated user.

**Path Parameters:**
- `user_id` (string): The authenticated user's ID

**Query Parameters:**
- `status` (optional): "all" | "pending" | "completed"
- `sort` (optional): "created_at" | "title" | "updated_at"

**Response:**
```json
{
  "tasks": [
    {
      "id": 1,
      "user_id": "user123",
      "title": "Buy groceries",
      "description": "Milk, eggs, bread",
      "completed": false,
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

**Status Codes:**
- 200: Success
- 401: Unauthorized
- 403: Forbidden (user_id mismatch)

---

### POST /api/{user_id}/tasks

Create a new task.

**Path Parameters:**
- `user_id` (string): The authenticated user's ID

**Request Body:**
```json
{
  "title": "Task title",
  "description": "Optional description"
}
```

**Response:**
```json
{
  "id": 2,
  "user_id": "user123",
  "title": "Task title",
  "description": "Optional description",
  "completed": false,
  "created_at": "2024-01-15T11:00:00Z",
  "updated_at": "2024-01-15T11:00:00Z"
}
```

**Status Codes:**
- 201: Created
- 400: Validation error
- 401: Unauthorized
- 403: Forbidden

---

### GET /api/{user_id}/tasks/{id}

Get a specific task by ID.

**Path Parameters:**
- `user_id` (string): The authenticated user's ID
- `id` (integer): Task ID

**Response:**
```json
{
  "id": 1,
  "user_id": "user123",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

**Status Codes:**
- 200: Success
- 401: Unauthorized
- 403: Forbidden
- 404: Not found

---

### PUT /api/{user_id}/tasks/{id}

Update an existing task.

**Path Parameters:**
- `user_id` (string): The authenticated user's ID
- `id` (integer): Task ID

**Request Body:**
```json
{
  "title": "Updated title",
  "description": "Updated description",
  "completed": true
}
```

**Response:**
```json
{
  "id": 1,
  "user_id": "user123",
  "title": "Updated title",
  "description": "Updated description",
  "completed": true,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T12:00:00Z"
}
```

**Status Codes:**
- 200: Success
- 400: Validation error
- 401: Unauthorized
- 403: Forbidden
- 404: Not found

---

### DELETE /api/{user_id}/tasks/{id}

Delete a task.

**Path Parameters:**
- `user_id` (string): The authenticated user's ID
- `id` (integer): Task ID

**Response:** No content (204)

**Status Codes:**
- 204: Success (no content)
- 401: Unauthorized
- 403: Forbidden
- 404: Not found

---

### PATCH /api/{user_id}/tasks/{id}/complete

Toggle task completion status.

**Path Parameters:**
- `user_id` (string): The authenticated user's ID
- `id` (integer): Task ID

**Response:**
```json
{
  "id": 1,
  "user_id": "user123",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": true,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T12:00:00Z"
}
```

**Status Codes:**
- 200: Success
- 401: Unauthorized
- 403: Forbidden
- 404: Not found

## Error Response Format

All errors return:
```json
{
  "detail": "Error message"
}
```
