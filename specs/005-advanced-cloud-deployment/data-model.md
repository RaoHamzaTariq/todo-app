# Data Model: Phase V - Advanced Cloud Deployment of Todo Chatbot

## Overview
This document defines the data models for the Phase V implementation of the Todo Chatbot, including advanced features such as recurring tasks, due dates, reminders, priorities, and tags. The models are designed to support event-driven architecture with proper data ownership and security controls.

## Core Entities

### Task
The primary entity representing a user task with advanced features.

```python
class Task(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: str = Field(description="Owner of the task")
    title: str = Field(description="Task title")
    description: str | None = Field(default=None, description="Task description")
    completed: bool = Field(default=False, description="Completion status")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp")
    due_date: datetime | None = Field(default=None, description="Due date for the task")
    priority: str = Field(default="medium", description="Priority level (low, medium, high)")
    tags: str | None = Field(default=None, description="Comma-separated tags for the task")
    status: str = Field(default="pending", description="Task status (pending, in-progress, completed)")

    # Relationships
    user: User | None = Relationship(back_populates="tasks")
    reminders: List["Reminder"] = Relationship(back_populates="task")
    recurring_pattern: "RecurringTask" | None = Relationship(back_populates="task")

    # Validation rules
    @validator("priority")
    def validate_priority(cls, v):
        if v not in ["low", "medium", "high"]:
            raise ValueError("Priority must be low, medium, or high")
        return v

    @validator("status")
    def validate_status(cls, v):
        if v not in ["pending", "in-progress", "completed"]:
            raise ValueError("Status must be pending, in-progress, or completed")
        return v
```

### User
The user entity with multi-tenancy support for data isolation.

```python
class User(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    email: str = Field(unique=True, description="User's email address")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Account creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp")
    preferences: str | None = Field(default=None, description="JSON string for user preferences")

    # Relationships
    tasks: List[Task] = Relationship(back_populates="user")
    recurring_tasks: List["RecurringTask"] = Relationship(back_populates="user")
    reminders: List["Reminder"] = Relationship(back_populates="user")
```

### RecurringTask
Entity representing recurring task patterns.

```python
class RecurringTask(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: str = Field(description="Owner of the recurring task")
    title: str = Field(description="Title for the recurring task")
    description: str | None = Field(default=None, description="Description for the recurring task")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp")
    frequency: str = Field(description="Frequency pattern (daily, weekly, monthly, yearly)")
    interval: int = Field(default=1, description="Interval multiplier for frequency")
    end_date: datetime | None = Field(default=None, description="End date for recurrence (optional)")
    active: bool = Field(default=True, description="Whether the recurring pattern is active")

    # Relationships
    user: User | None = Relationship(back_populates="recurring_tasks")
    task: Task | None = Relationship(back_populates="recurring_pattern")

    # Validation rules
    @validator("frequency")
    def validate_frequency(cls, v):
        if v not in ["daily", "weekly", "monthly", "yearly"]:
            raise ValueError("Frequency must be daily, weekly, monthly, or yearly")
        return v
```

### Reminder
Entity for task reminders with configurable timing.

```python
class Reminder(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: str = Field(description="Owner of the reminder")
    task_id: int = Field(description="Associated task")
    reminder_datetime: datetime = Field(description="When to send the reminder")
    sent: bool = Field(default=False, description="Whether the reminder has been sent")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp")
    channel: str = Field(default="email", description="Channel to send reminder (email, push, sms)")

    # Relationships
    user: User | None = Relationship(back_populates="reminders")
    task: Task | None = Relationship(back_populates="reminders")

    # Validation rules
    @validator("channel")
    def validate_channel(cls, v):
        if v not in ["email", "push", "sms"]:
            raise ValueError("Channel must be email, push, or sms")
        return v
```

### TaskEvent
Immutable record for audit logging of task operations.

```python
class TaskEvent(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: str = Field(description="User who triggered the event")
    task_id: int | None = Field(default=None, description="Associated task (null for new tasks)")
    event_type: str = Field(description="Type of event (created, updated, deleted, completed)")
    event_data: str = Field(description="JSON string with event details")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Event timestamp")

    # Validation rules
    @validator("event_type")
    def validate_event_type(cls, v):
        if v not in ["created", "updated", "deleted", "completed", "recurring-created"]:
            raise ValueError("Event type must be created, updated, deleted, completed, or recurring-created")
        return v
```

## Event Schemas

### TaskCreatedEvent
Event published when a new task is created.

```json
{
  "event_type": "task.created",
  "event_id": "uuid-string",
  "timestamp": "ISO-8601-datetime",
  "user_id": "user-identifier",
  "task_id": 123,
  "data": {
    "title": "Task title",
    "description": "Task description",
    "due_date": "ISO-8601-datetime",
    "priority": "high|medium|low",
    "tags": ["tag1", "tag2"],
    "status": "pending|in-progress|completed"
  }
}
```

### TaskUpdatedEvent
Event published when a task is updated.

```json
{
  "event_type": "task.updated",
  "event_id": "uuid-string",
  "timestamp": "ISO-8601-datetime",
  "user_id": "user-identifier",
  "task_id": 123,
  "data": {
    "changes": {
      "field_name": {"old_value": "old", "new_value": "new"},
      "status": {"old_value": "pending", "new_value": "in-progress"}
    },
    "updated_fields": ["status", "due_date"]
  }
}
```

### ReminderScheduledEvent
Event published when a reminder is scheduled.

```json
{
  "event_type": "reminder.scheduled",
  "event_id": "uuid-string",
  "timestamp": "ISO-8601-datetime",
  "user_id": "user-identifier",
  "task_id": 123,
  "data": {
    "reminder_id": 456,
    "scheduled_time": "ISO-8601-datetime",
    "channel": "email|push|sms",
    "trigger_condition": "before_due_date|specific_time"
  }
}
```

### RecurringTaskCreatedEvent
Event published when a recurring task generates a new instance.

```json
{
  "event_type": "recurring-task.instance-created",
  "event_id": "uuid-string",
  "timestamp": "ISO-8601-datetime",
  "user_id": "user-identifier",
  "original_task_id": 123,
  "instance_task_id": 789,
  "data": {
    "frequency": "weekly",
    "next_occurrence": "ISO-8601-datetime",
    "is_template": false
  }
}
```

## State Transition Diagrams

### Task Status Transitions
```
pending → in-progress → completed
   ↓                           ↑
   ←---------------------------
```

### Reminder Lifecycle
```
scheduled → sent → processed
   ↓
failed → retry → sent
```

## Validation Rules

### Data Integrity
- All tasks must have a valid user_id for ownership
- Task titles must be between 1 and 255 characters
- Due dates must be in the future for pending tasks
- Priority values limited to: low, medium, high
- Status values limited to: pending, in-progress, completed

### Security Constraints
- Users can only access their own tasks and related data
- TaskEvent records are immutable after creation
- User_id must match JWT token claims for all operations
- Cross-user data access is strictly prohibited

### Business Logic Constraints
- Recurring tasks cannot be marked as completed (instances can be)
- Reminders cannot be scheduled after the task due date
- A task can have multiple reminders
- Tags are normalized to lowercase and unique within a task