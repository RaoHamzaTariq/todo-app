"""
Reminder model for the Todo Chatbot application.
This model represents task reminders with configurable timing.
"""

from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from pydantic import validator
from uuid import uuid4


class ReminderBase(SQLModel):
    """Base class for Reminder model with common fields."""
    user_id: str = Field(description="Owner of the reminder")
    task_id: int = Field(description="Associated task")
    reminder_datetime: datetime = Field(description="When to send the reminder")
    channel: str = Field(default="email", description="Channel to send reminder (email, push, sms)")


class Reminder(ReminderBase, table=True):
    """Reminder model representing a task reminder."""
    id: Optional[int] = Field(default=None, primary_key=True)
    sent: bool = Field(default=False, description="Whether the reminder has been sent")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp")

    # Relationships
    user: Optional["User"] = Relationship(back_populates="reminders")
    task: Optional["Task"] = Relationship(back_populates="reminders")

    # Validation rules
    @validator("channel")
    def validate_channel(cls, v):
        """Validate that channel is one of the allowed values."""
        allowed_channels = ["email", "push", "sms"]
        if v not in allowed_channels:
            raise ValueError(f"Channel must be one of {allowed_channels}")
        return v.lower()

    @validator("reminder_datetime")
    def validate_reminder_datetime(cls, v):
        """Validate that reminder datetime is not in the past."""
        if v < datetime.utcnow():
            raise ValueError("Reminder datetime cannot be in the past")
        return v

    @validator("task_id")
    def validate_task_id(cls, v):
        """Validate that task_id is a positive integer."""
        if v <= 0:
            raise ValueError("Task ID must be a positive integer")
        return v

    def is_overdue(self) -> bool:
        """Check if this reminder is overdue."""
        return not self.sent and self.reminder_datetime < datetime.utcnow()

    def should_send_now(self, buffer_minutes: int = 5) -> bool:
        """Check if this reminder should be sent now (within buffer time)."""
        if self.sent:
            return False

        now = datetime.utcnow()
        buffer = now + timedelta(minutes=buffer_minutes)

        return self.reminder_datetime <= buffer


from datetime import timedelta

    def to_dict(self) -> dict:
        """Convert reminder to dictionary representation."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "task_id": self.task_id,
            "reminder_datetime": self.reminder_datetime.isoformat(),
            "sent": self.sent,
            "channel": self.channel,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }


# Import needed to avoid circular dependencies
try:
    from .task_model import User, Task
except ImportError:
    # In case we're in a different context
    pass


# Import timedelta for the should_send_now method
from datetime import timedelta