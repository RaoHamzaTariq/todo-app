"""
API models for reminders in the Todo Chatbot application.
These Pydantic models define the input/output schemas for the reminder API.
"""

from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ReminderCreate(BaseModel):
    """
    Model for creating a reminder.
    Used as input for the create reminder endpoint.
    """
    task_id: int
    reminder_datetime: datetime
    channel: str = "email"  # Default to email


class ReminderUpdate(BaseModel):
    """
    Model for updating a reminder.
    Used as input for the update reminder endpoint.
    """
    reminder_datetime: Optional[datetime] = None
    channel: Optional[str] = None


class ReminderPublic(BaseModel):
    """
    Public model for reminder.
    Used as output for reminder endpoints.
    """
    id: int
    user_id: str
    task_id: int
    reminder_datetime: datetime
    sent: bool
    channel: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True