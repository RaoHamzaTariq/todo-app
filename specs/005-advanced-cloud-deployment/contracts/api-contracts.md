# API Contracts: Phase V - Advanced Cloud Deployment of Todo Chatbot

## Overview
This document defines the API contracts for the Phase V Todo Chatbot with advanced features. These contracts outline the endpoints, request/response formats, and error handling patterns for all public API surfaces.

## Task Management Endpoints

### Create Task with Advanced Features
```
POST /api/{user_id}/tasks/
```

**Request Body:**
```json
{
  "title": "string (required, 1-255 chars)",
  "description": "string (optional)",
  "due_date": "ISO 8601 datetime string (optional)",
  "priority": "enum (low, medium, high) default: medium",
  "tags": "array of strings (optional, max 10 tags)",
  "status": "enum (pending, in-progress, completed) default: pending"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": "integer",
    "user_id": "string",
    "title": "string",
    "description": "string or null",
    "completed": "boolean",
    "created_at": "ISO 8601 datetime",
    "updated_at": "ISO 8601 datetime",
    "due_date": "ISO 8601 datetime or null",
    "priority": "string",
    "tags": "string or null",
    "status": "string"
  }
}
```

**Error Responses:**
- 400: Invalid input data
- 401: Unauthorized (invalid JWT)
- 403: Forbidden (attempting to create for different user)

---

### Get Tasks with Filters
```
GET /api/{user_id}/tasks/?status={status}&priority={priority}&due_after={date}&due_before={date}&tags={tag1,tag2}
```

**Query Parameters:**
- `status`: optional, enum (pending, in-progress, completed, all)
- `priority`: optional, enum (low, medium, high)
- `due_after`: optional, ISO 8601 date
- `due_before`: optional, ISO 8601 date
- `tags`: optional, comma-separated list of tags
- `sort_by`: optional, enum (due_date, priority, created_at, title)
- `order`: optional, enum (asc, desc) default: asc
- `page`: optional, integer default: 1
- `limit`: optional, integer default: 20

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": "integer",
      "user_id": "string",
      "title": "string",
      "description": "string or null",
      "completed": "boolean",
      "created_at": "ISO 8601 datetime",
      "updated_at": "ISO 8601 datetime",
      "due_date": "ISO 8601 datetime or null",
      "priority": "string",
      "tags": "string or null",
      "status": "string"
    }
  ],
  "pagination": {
    "page": "integer",
    "limit": "integer",
    "total": "integer",
    "pages": "integer"
  }
}
```

---

### Update Task
```
PUT /api/{user_id}/tasks/{task_id}
```

**Request Body:**
```json
{
  "title": "string (optional, 1-255 chars)",
  "description": "string (optional)",
  "due_date": "ISO 8601 datetime string (optional)",
  "priority": "enum (low, medium, high) (optional)",
  "tags": "array of strings (optional, max 10 tags)",
  "status": "enum (pending, in-progress, completed) (optional)"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": "integer",
    "user_id": "string",
    "title": "string",
    "description": "string or null",
    "completed": "boolean",
    "created_at": "ISO 8601 datetime",
    "updated_at": "ISO 8601 datetime",
    "due_date": "ISO 8601 datetime or null",
    "priority": "string",
    "tags": "string or null",
    "status": "string"
  }
}
```

## Recurring Task Endpoints

### Create Recurring Task
```
POST /api/{user_id}/tasks/recurring
```

**Request Body:**
```json
{
  "title": "string (required, 1-255 chars)",
  "description": "string (optional)",
  "frequency": "enum (daily, weekly, monthly, yearly) (required)",
  "interval": "integer (optional, default: 1)",
  "end_date": "ISO 8601 datetime string (optional)",
  "due_date_template": "ISO 8601 time string (optional)",
  "priority": "enum (low, medium, high) (optional, default: medium)",
  "tags": "array of strings (optional, max 10 tags)"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": "integer",
    "user_id": "string",
    "title": "string",
    "description": "string or null",
    "created_at": "ISO 8601 datetime",
    "updated_at": "ISO 8601 datetime",
    "frequency": "string",
    "interval": "integer",
    "end_date": "ISO 8601 datetime or null",
    "active": "boolean",
    "due_date_template": "string or null",
    "priority": "string",
    "tags": "string or null"
  }
}
```

---

### Get Recurring Tasks
```
GET /api/{user_id}/tasks/recurring
```

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": "integer",
      "user_id": "string",
      "title": "string",
      "description": "string or null",
      "created_at": "ISO 8601 datetime",
      "updated_at": "ISO 8601 datetime",
      "frequency": "string",
      "interval": "integer",
      "end_date": "ISO 8601 datetime or null",
      "active": "boolean",
      "due_date_template": "string or null",
      "priority": "string",
      "tags": "string or null"
    }
  ]
}
```

---

### Update Recurring Task
```
PUT /api/{user_id}/tasks/recurring/{recurring_task_id}
```

**Request Body:**
```json
{
  "title": "string (optional)",
  "description": "string (optional)",
  "frequency": "enum (daily, weekly, monthly, yearly) (optional)",
  "interval": "integer (optional)",
  "end_date": "ISO 8601 datetime string (optional)",
  "active": "boolean (optional)"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": "integer",
    "user_id": "string",
    "title": "string",
    "description": "string or null",
    "created_at": "ISO 8601 datetime",
    "updated_at": "ISO 8601 datetime",
    "frequency": "string",
    "interval": "integer",
    "end_date": "ISO 8601 datetime or null",
    "active": "boolean"
  }
}
```

## Reminder Endpoints

### Schedule Reminder
```
POST /api/{user_id}/reminders
```

**Request Body:**
```json
{
  "task_id": "integer (required)",
  "reminder_datetime": "ISO 8601 datetime string (required)",
  "channel": "enum (email, push, sms) (optional, default: email)"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": "integer",
    "user_id": "string",
    "task_id": "integer",
    "reminder_datetime": "ISO 8601 datetime",
    "sent": "boolean",
    "created_at": "ISO 8601 datetime",
    "updated_at": "ISO 8601 datetime",
    "channel": "string"
  }
}
```

---

### Get User Reminders
```
GET /api/{user_id}/reminders?status=scheduled,sent&after={date}&before={date}
```

**Query Parameters:**
- `status`: optional, enum (scheduled, sent, all)
- `after`: optional, ISO 8601 date
- `before`: optional, ISO 8601 date

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": "integer",
      "user_id": "string",
      "task_id": "integer",
      "reminder_datetime": "ISO 8601 datetime",
      "sent": "boolean",
      "created_at": "ISO 8601 datetime",
      "updated_at": "ISO 8601 datetime",
      "channel": "string"
    }
  ]
}
```

---

### Cancel Reminder
```
DELETE /api/{user_id}/reminders/{reminder_id}
```

**Response:**
```json
{
  "success": true,
  "message": "Reminder canceled successfully"
}
```

## Search and Filtering Endpoints

### Advanced Search
```
GET /api/{user_id}/tasks/search?q={query}&tags={tags}&priority={priority}&status={status}&due_after={date}&due_before={date}
```

**Query Parameters:**
- `q`: required, search query string
- `tags`: optional, comma-separated list of tags to include
- `exclude_tags`: optional, comma-separated list of tags to exclude
- `priority`: optional, enum (low, medium, high)
- `status`: optional, enum (pending, in-progress, completed)
- `due_after`: optional, ISO 8601 date
- `due_before`: optional, ISO 8601 date
- `sort_by`: optional, enum (relevance, due_date, priority, created_at)
- `order`: optional, enum (asc, desc) default: desc
- `page`: optional, integer default: 1
- `limit`: optional, integer default: 20

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": "integer",
      "user_id": "string",
      "title": "string",
      "description": "string or null",
      "completed": "boolean",
      "created_at": "ISO 8601 datetime",
      "updated_at": "ISO 8601 datetime",
      "due_date": "ISO 8601 datetime or null",
      "priority": "string",
      "tags": "string or null",
      "status": "string"
    }
  ],
  "pagination": {
    "page": "integer",
    "limit": "integer",
    "total": "integer",
    "pages": "integer"
  },
  "meta": {
    "query": "string",
    "search_time_ms": "integer"
  }
}
```

## Event Stream Endpoints

### Get Task Event Stream
```
GET /api/{user_id}/events/task-stream?task_id={task_id}&since={timestamp}&limit={limit}
```

**Query Parameters:**
- `task_id`: optional, specific task to get events for
- `since`: optional, ISO 8601 timestamp to get events after
- `limit`: optional, integer default: 100
- `types`: optional, comma-separated list of event types

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": "integer",
      "user_id": "string",
      "task_id": "integer or null",
      "event_type": "string",
      "event_data": "json object",
      "created_at": "ISO 8601 datetime"
    }
  ]
}
```

## Error Response Format

All error responses follow this structure:
```json
{
  "success": false,
  "error": {
    "code": "string",
    "message": "string",
    "details": "object or array (optional)"
  }
}
```

### Common Error Codes
- `INVALID_INPUT`: Request data doesn't match validation rules
- `UNAUTHORIZED`: Missing or invalid authentication
- `FORBIDDEN`: User doesn't have permission for this action
- `RESOURCE_NOT_FOUND`: Requested resource doesn't exist
- `INTERNAL_ERROR`: Unexpected server error
- `RATE_LIMIT_EXCEEDED`: Too many requests from this user
- `VALIDATION_ERROR`: Specific validation failure details

## Authentication and Headers

### Required Headers
- `Authorization: Bearer {jwt_token}` for all authenticated endpoints
- `Content-Type: application/json` for POST/PUT/PATCH requests

### Common Response Headers
- `X-Request-ID`: Unique ID for request tracking
- `X-Rate-Limit-Remaining`: Requests remaining in current window
- `X-Rate-Limit-Reset`: Timestamp when rate limit resets

## Rate Limiting

All endpoints are subject to rate limiting:
- Global: 1000 requests per minute per IP
- Per-user: 500 requests per minute per authenticated user
- Per-endpoint: 100 requests per minute per authenticated user