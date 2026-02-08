"""
API models for recurring tasks in the Todo Chatbot application.
These Pydantic models define the input/output schemas for the recurring task API.
"""

from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class RecurringTaskCreate(BaseModel):
    """
    Model for creating a recurring task.
    Used as input for the create recurring task endpoint.
    """
    title: str
    description: Optional[str] = None
    frequency: str  # daily, weekly, monthly, yearly
    interval: int = 1
    end_date: Optional[datetime] = None
    active: bool = True


class RecurringTaskUpdate(BaseModel):
    """
    Model for updating a recurring task.
    Used as input for the update recurring task endpoint.
    """
    title: Optional[str] = None
    description: Optional[str] = None
    frequency: Optional[str] = None  # daily, weekly, monthly, yearly
    interval: Optional[int] = None
    end_date: Optional[datetime] = None
    active: Optional[bool] = None


class RecurringTaskPublic(BaseModel):
    """
    Public model for recurring task.
    Used as output for recurring task endpoints.
    """
    id: int
    user_id: str
    title: str
    description: Optional[str] = None
    frequency: str
    interval: int
    end_date: Optional[datetime] = None
    active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True