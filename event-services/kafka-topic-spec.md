# Kafka Topic Specifications for Todo Chatbot Event-Driven Architecture

## Overview
This document defines the Kafka topics and event schemas for the Todo Chatbot event-driven architecture. These topics enable decoupled communication between services and support the advanced features of recurring tasks, reminders, and audit logging.

## Kafka Topics

### 1. task-events
- **Purpose**: Main topic for all task-related events (creation, updates, completion, deletion)
- **Partitions**: 3
- **Replication Factor**: 1 (for development) / 3 (for production)
- **Retention**: 7 days
- **Cleanup Policy**: Delete

#### Event Types:
- `task.created` - When a new task is created
- `task.updated` - When a task is modified
- `task.completed` - When a task is marked as completed
- `task.deleted` - When a task is deleted

### 2. recurring-task-events
- **Purpose**: Events related to recurring task patterns and their instantiation
- **Partitions**: 3
- **Replication Factor**: 1 (for development) / 3 (for production)
- **Retention**: 7 days
- **Cleanup Policy**: Delete

#### Event Types:
- `recurring-task.created` - When a recurring task pattern is defined
- `recurring-task.updated` - When a recurring task pattern is modified
- `recurring-task.instance-created` - When a recurring task generates a new instance
- `recurring-task.cancelled` - When a recurring task pattern is cancelled

### 3. reminder-events
- **Purpose**: Events related to reminder scheduling and delivery
- **Partitions**: 3
- **Replication Factor**: 1 (for development) / 3 (for production)
- **Retention**: 7 days
- **Cleanup Policy**: Delete

#### Event Types:
- `reminder.scheduled` - When a reminder is scheduled
- `reminder.triggered` - When a reminder should be delivered
- `reminder.sent` - When a reminder has been successfully sent
- `reminder.failed` - When a reminder failed to be delivered

### 4. audit-log-events
- **Purpose**: Audit trail for all user actions and system events
- **Partitions**: 3
- **Replication Factor**: 1 (for development) / 3 (for production)
- **Retention**: 30 days
- **Cleanup Policy**: Delete

#### Event Types:
- `user.action` - Any action taken by a user
- `system.event` - System-level events and operations
- `security.event` - Security-related events

## Event Schema Definitions

### TaskCreatedEvent
```json
{
  "event_type": "task.created",
  "event_id": "uuid-string",
  "timestamp": "ISO-8601-datetime",
  "user_id": "user-identifier",
  "correlation_id": "request-correlation-id",
  "data": {
    "task_id": 123,
    "title": "Task title",
    "description": "Task description",
    "due_date": "ISO-8601-datetime",
    "priority": "high|medium|low",
    "tags": ["tag1", "tag2"],
    "status": "pending|in-progress|completed",
    "recurring_pattern_id": null  // Optional, if task is from recurring pattern
  }
}
```

### TaskUpdatedEvent
```json
{
  "event_type": "task.updated",
  "event_id": "uuid-string",
  "timestamp": "ISO-8601-datetime",
  "user_id": "user-identifier",
  "correlation_id": "request-correlation-id",
  "data": {
    "task_id": 123,
    "changes": {
      "field_name": {"old_value": "old", "new_value": "new"},
      "status": {"old_value": "pending", "new_value": "in-progress"}
    },
    "updated_fields": ["status", "due_date"]
  }
}
```

### RecurringTaskCreatedEvent
```json
{
  "event_type": "recurring-task.created",
  "event_id": "uuid-string",
  "timestamp": "ISO-8601-datetime",
  "user_id": "user-identifier",
  "correlation_id": "request-correlation-id",
  "data": {
    "recurring_task_id": 456,
    "title": "Recurring task title",
    "description": "Recurring task description",
    "frequency": "daily|weekly|monthly|yearly",
    "interval": 1,
    "end_date": "ISO-8601-datetime",  // Optional
    "active": true
  }
}
```

### RecurringTaskInstanceCreatedEvent
```json
{
  "event_type": "recurring-task.instance-created",
  "event_id": "uuid-string",
  "timestamp": "ISO-8601-datetime",
  "user_id": "user-identifier",
  "correlation_id": "request-correlation-id",
  "data": {
    "original_recurring_task_id": 456,
    "new_task_id": 789,
    "due_date": "ISO-8601-datetime",
    "is_template": false
  }
}
```

### ReminderScheduledEvent
```json
{
  "event_type": "reminder.scheduled",
  "event_id": "uuid-string",
  "timestamp": "ISO-8601-datetime",
  "user_id": "user-identifier",
  "correlation_id": "request-correlation-id",
  "data": {
    "reminder_id": 999,
    "task_id": 123,
    "scheduled_time": "ISO-8601-datetime",
    "channel": "email|push|sms",
    "trigger_condition": "before_due_date|specific_time"
  }
}
```

### ReminderTriggeredEvent
```json
{
  "event_type": "reminder.triggered",
  "event_id": "uuid-string",
  "timestamp": "ISO-8601-datetime",
  "user_id": "user-identifier",
  "correlation_id": "request-correlation-id",
  "data": {
    "reminder_id": 999,
    "task_id": 123,
    "delivery_time": "ISO-8601-datetime",
    "channel": "email|push|sms"
  }
}
```

### AuditEvent
```json
{
  "event_type": "user.action",
  "event_id": "uuid-string",
  "timestamp": "ISO-8601-datetime",
  "user_id": "user-identifier",
  "correlation_id": "request-correlation-id",
  "data": {
    "action": "task.created|task.updated|etc.",
    "resource_id": "id-of-resource",
    "resource_type": "task|recurring-task|reminder",
    "ip_address": "user-ip-address",
    "user_agent": "user-agent-string",
    "metadata": {}
  }
}
```

## Consumer Groups

### Backend Service
- `backend-consumer-group` - Consumes task events for state updates

### Reminder Service
- `reminder-service-consumer-group` - Consumes task and recurring events to schedule reminders

### Recurring Task Service
- `recurring-task-service-consumer-group` - Consumes recurring events to manage task generation

### Audit Log Service
- `audit-log-service-consumer-group` - Consumes all events for audit logging

### Notification Service
- `notification-service-consumer-group` - Consumes reminder events to send notifications