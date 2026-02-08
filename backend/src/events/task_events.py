"""
Event schemas for task-related events in the Todo Chatbot event-driven architecture.
"""

from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field
import uuid


class EventType(str, Enum):
    TASK_CREATED = "task.created"
    TASK_UPDATED = "task.updated"
    TASK_COMPLETED = "task.completed"
    TASK_DELETED = "task.deleted"
    RECURRING_TASK_CREATED = "recurring-task.created"
    RECURRING_TASK_UPDATED = "recurring-task.updated"
    RECURRING_TASK_INSTANCE_CREATED = "recurring-task.instance-created"
    RECURRING_TASK_CANCELLED = "recurring-task.cancelled"
    REMINDER_SCHEDULED = "reminder.scheduled"
    REMINDER_TRIGGERED = "reminder.triggered"
    REMINDER_SENT = "reminder.sent"
    REMINDER_FAILED = "reminder.failed"
    USER_ACTION = "user.action"
    SYSTEM_EVENT = "system.event"
    SECURITY_EVENT = "security.event"


class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in-progress"
    COMPLETED = "completed"


class EventBase(BaseModel):
    """Base class for all events"""
    event_type: EventType
    event_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    user_id: str
    correlation_id: Optional[str] = None


class TaskCreatedEventData(BaseModel):
    task_id: int
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    priority: TaskPriority = TaskPriority.MEDIUM
    tags: Optional[List[str]] = []
    status: TaskStatus = TaskStatus.PENDING
    recurring_pattern_id: Optional[int] = None


class TaskCreatedEvent(EventBase):
    """Event published when a new task is created."""
    event_type: EventType = EventType.TASK_CREATED
    data: TaskCreatedEventData


class TaskUpdatedFieldChange(BaseModel):
    old_value: Any
    new_value: Any


class TaskUpdatedEventData(BaseModel):
    task_id: int
    changes: Dict[str, TaskUpdatedFieldChange] = {}
    updated_fields: List[str] = []


class TaskUpdatedEvent(EventBase):
    """Event published when a task is updated."""
    event_type: EventType = EventType.TASK_UPDATED
    data: TaskUpdatedEventData


class RecurringTaskCreatedEventData(BaseModel):
    recurring_task_id: int
    title: str
    description: Optional[str] = None
    frequency: str  # daily, weekly, monthly, yearly
    interval: int = 1
    end_date: Optional[datetime] = None
    active: bool = True


class RecurringTaskCreatedEvent(EventBase):
    """Event published when a recurring task pattern is created."""
    event_type: EventType = EventType.RECURRING_TASK_CREATED
    data: RecurringTaskCreatedEventData


class RecurringTaskInstanceCreatedEventData(BaseModel):
    original_recurring_task_id: int
    new_task_id: int
    due_date: datetime
    is_template: bool = False


class RecurringTaskInstanceCreatedEvent(EventBase):
    """Event published when a recurring task generates a new instance."""
    event_type: EventType = EventType.RECURRING_TASK_INSTANCE_CREATED
    data: RecurringTaskInstanceCreatedEventData


class ReminderScheduledEventData(BaseModel):
    reminder_id: int
    task_id: int
    scheduled_time: datetime
    channel: str  # email, push, sms
    trigger_condition: str  # before_due_date, specific_time


class ReminderScheduledEvent(EventBase):
    """Event published when a reminder is scheduled."""
    event_type: EventType = EventType.REMINDER_SCHEDULED
    data: ReminderScheduledEventData


class ReminderTriggeredEventData(BaseModel):
    reminder_id: int
    task_id: int
    delivery_time: datetime
    channel: str  # email, push, sms


class ReminderTriggeredEvent(EventBase):
    """Event published when a reminder is triggered."""
    event_type: EventType = EventType.REMINDER_TRIGGERED
    data: ReminderTriggeredEventData


class AuditEventData(BaseModel):
    action: str
    resource_id: str
    resource_type: str
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    metadata: Dict[str, Any] = {}


class AuditEvent(EventBase):
    """Event published for audit logging."""
    event_type: EventType
    data: AuditEventData


# Union type for all possible events
from typing import Union

AnyEvent = Union[
    TaskCreatedEvent,
    TaskUpdatedEvent,
    RecurringTaskCreatedEvent,
    RecurringTaskInstanceCreatedEvent,
    ReminderScheduledEvent,
    ReminderTriggeredEvent,
    AuditEvent
]