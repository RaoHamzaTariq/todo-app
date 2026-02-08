"""
Task event model for the Todo Chatbot application.
This model represents events related to task operations for event-driven architecture.
"""

from datetime import datetime
from enum import Enum
from typing import Optional, Dict, Any
from sqlmodel import SQLModel, Field
from pydantic import validator
import json


class TaskEventType(str, Enum):
    """Enumeration of possible task event types."""
    TASK_CREATED = "task_created"
    TASK_UPDATED = "task_updated"
    TASK_DELETED = "task_deleted"
    TASK_COMPLETED = "task_completed"
    TASK_REOPENED = "task_reopened"
    REMINDER_SCHEDULED = "reminder_scheduled"
    REMINDER_SENT = "reminder_sent"
    RECURRING_TASK_CREATED = "recurring_task_created"
    RECURRING_TASK_UPDATED = "recurring_task_updated"


class TaskEvent(SQLModel, table=True):
    """Task event model representing events in the system for event-driven architecture."""

    id: Optional[int] = Field(default=None, primary_key=True)
    event_type: TaskEventType = Field(description="Type of the event")
    user_id: str = Field(description="ID of the user associated with the event")
    task_id: Optional[int] = Field(default=None, description="ID of the task associated with the event")
    related_entity_id: Optional[int] = Field(default=None, description="ID of any related entity (e.g., reminder, recurring task)")
    related_entity_type: Optional[str] = Field(default=None, description="Type of the related entity")
    payload: str = Field(description="JSON string containing event-specific data")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Timestamp when the event was created")
    processed: bool = Field(default=False, description="Whether the event has been processed")
    processed_at: Optional[datetime] = Field(default=None, description="Timestamp when the event was processed")
    error_message: Optional[str] = Field(default=None, description="Error message if processing failed")

    @validator("event_type")
    def validate_event_type(cls, v):
        """Validate that event type is one of the allowed values."""
        if v not in TaskEventType.__members__.values():
            raise ValueError(f"Event type must be one of {list(TaskEventType.__members__.values())}")
        return v

    def get_payload_data(self) -> Dict[str, Any]:
        """Deserialize the payload JSON string to a dictionary."""
        try:
            return json.loads(self.payload)
        except json.JSONDecodeError:
            return {}

    def set_payload_data(self, data: Dict[str, Any]):
        """Serialize the payload dictionary to a JSON string."""
        self.payload = json.dumps(data, default=str)

    def to_dict(self) -> dict:
        """Convert task event to dictionary representation."""
        return {
            "id": self.id,
            "event_type": self.event_type,
            "user_id": self.user_id,
            "task_id": self.task_id,
            "related_entity_id": self.related_entity_id,
            "related_entity_type": self.related_entity_type,
            "payload": self.get_payload_data(),
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "processed": self.processed,
            "processed_at": self.processed_at.isoformat() if self.processed_at else None,
            "error_message": self.error_message
        }


class TaskEventCreate(SQLModel):
    """Model for creating task events."""
    event_type: TaskEventType
    user_id: str
    task_id: Optional[int] = None
    related_entity_id: Optional[int] = None
    related_entity_type: Optional[str] = None
    payload: Dict[str, Any] = {}


class TaskEventUpdate(SQLModel):
    """Model for updating task events."""
    processed: Optional[bool] = None
    processed_at: Optional[datetime] = None
    error_message: Optional[str] = None