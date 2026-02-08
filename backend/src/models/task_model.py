"""
Task model for the Todo Chatbot application.
This model represents a user task with advanced features like priorities, tags, due dates, etc.
"""

from datetime import datetime
from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from pydantic import validator
from uuid import UUID, uuid4
import json

if TYPE_CHECKING:
    from .reminder_model import Reminder
    from .recurring_task_model import RecurringTask


class Tag(SQLModel, table=True):
    """Tag model for categorizing tasks."""
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(min_length=1, max_length=50, description="Tag name")
    user_id: str = Field(description="Owner of the tag")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")

    @validator("name")
    def validate_name(cls, v):
        """Validate that tag name is appropriate."""
        if not v or len(v.strip()) == 0:
            raise ValueError("Tag name cannot be empty")
        if len(v) > 50:
            raise ValueError("Tag name must be 50 characters or less")
        # Normalize the tag name (lowercase, no extra whitespace)
        return v.strip().lower()

    def to_dict(self) -> dict:
        """Convert tag to dictionary representation."""
        return {
            "id": self.id,
            "name": self.name,
            "user_id": self.user_id,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


class TaskBase(SQLModel):
    """Base class for Task model with common fields."""
    title: str = Field(min_length=1, max_length=255, description="Task title")
    description: Optional[str] = Field(default=None, max_length=1000, description="Task description")
    completed: bool = Field(default=False, description="Completion status")
    due_date: Optional[datetime] = Field(default=None, description="Due date for the task")
    priority: str = Field(default="medium", description="Priority level (low, medium, high)")
    tags: Optional[str] = Field(default=None, description="Comma-separated tags for the task")
    status: str = Field(default="pending", description="Task status (pending, in-progress, completed)")
    user_id: str = Field(description="Owner of the task")


class Task(TaskBase, table=True):
    """Task model representing a user task in the system."""
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp")

    # Relationships
    user: Optional["User"] = Relationship(back_populates="tasks")
    reminders: List["Reminder"] = Relationship(back_populates="task", sa_relationship_kwargs={"lazy": "select"})
    recurring_pattern: Optional["RecurringTask"] = Relationship(back_populates="task",
                                                              sa_relationship_kwargs={"uselist": False})

    # Validation rules
    @validator("priority")
    def validate_priority(cls, v):
        """Validate that priority is one of the allowed values."""
        allowed_priorities = ["low", "medium", "high"]
        if v not in allowed_priorities:
            raise ValueError(f"Priority must be one of {allowed_priorities}")
        return v.lower()

    @validator("status")
    def validate_status(cls, v):
        """Validate that status is one of the allowed values."""
        allowed_statuses = ["pending", "in-progress", "completed"]
        if v not in allowed_statuses:
            raise ValueError(f"Status must be one of {allowed_statuses}")
        return v.replace(" ", "-").lower()

    @validator("title")
    def validate_title(cls, v):
        """Validate task title length."""
        if not v or len(v.strip()) == 0:
            raise ValueError("Title cannot be empty")
        if len(v) > 255:
            raise ValueError("Title must be 255 characters or less")
        return v.strip()

    def add_tag(self, tag: str):
        """Add a tag to the task."""
        tag = tag.strip().lower()
        if not tag:
            return

        current_tags = self.get_tags()
        if tag not in current_tags:
            current_tags.append(tag)
            self.tags = ",".join(current_tags)

    def remove_tag(self, tag: str):
        """Remove a tag from the task."""
        tag = tag.strip().lower()
        if not tag:
            return

        current_tags = self.get_tags()
        if tag in current_tags:
            current_tags.remove(tag)
            self.tags = ",".join(current_tags)

    def get_tags(self) -> List[str]:
        """Get list of tags for the task."""
        if not self.tags:
            return []
        return [tag.strip() for tag in self.tags.split(",") if tag.strip()]

    def to_dict(self) -> dict:
        """Convert task to dictionary representation."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "description": self.description,
            "completed": self.completed,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "priority": self.priority,
            "tags": self.get_tags(),
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }


class User(SQLModel, table=True):
    """User model for multi-tenancy support."""
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    email: str = Field(unique=True, description="User's email address")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Account creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp")
    preferences: Optional[str] = Field(default=None, description="JSON string for user preferences")

    # Relationships
    tasks: List[Task] = Relationship(back_populates="user", sa_relationship_kwargs={"lazy": "select"})
    recurring_tasks: List["RecurringTask"] = Relationship(back_populates="user", sa_relationship_kwargs={"lazy": "select"})
    reminders: List["Reminder"] = Relationship(back_populates="user", sa_relationship_kwargs={"lazy": "select"})

    def get_preferences(self) -> dict:
        """Get user preferences as a dictionary."""
        if not self.preferences:
            return {}
        try:
            return json.loads(self.preferences)
        except json.JSONDecodeError:
            return {}

    def set_preferences(self, prefs: dict):
        """Set user preferences from a dictionary."""
        self.preferences = json.dumps(prefs)


# Forward references - these would be defined in their respective models
class Reminder(SQLModel, table=True):
    """Reminder model - defined here for relationship purposes."""
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(description="Owner of the reminder")
    task_id: int = Field(description="Associated task")
    reminder_datetime: datetime = Field(description="When to send the reminder")
    sent: bool = Field(default=False, description="Whether the reminder has been sent")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp")
    channel: str = Field(default="email", description="Channel to send reminder (email, push, sms)")

    # Relationships
    user: Optional[User] = Relationship(back_populates="reminders")
    task: Optional[Task] = Relationship(back_populates="reminders")

    @validator("channel")
    def validate_channel(cls, v):
        """Validate that channel is one of the allowed values."""
        allowed_channels = ["email", "push", "sms"]
        if v not in allowed_channels:
            raise ValueError(f"Channel must be one of {allowed_channels}")
        return v.lower()


class RecurringTask(SQLModel, table=True):
    """RecurringTask model - defined here for relationship purposes."""
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(description="Owner of the recurring task")
    title: str = Field(description="Title for the recurring task")
    description: Optional[str] = Field(default=None, description="Description for the recurring task")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp")
    frequency: str = Field(description="Frequency pattern (daily, weekly, monthly, yearly)")
    interval: int = Field(default=1, description="Interval multiplier for frequency")
    end_date: Optional[datetime] = Field(default=None, description="End date for recurrence (optional)")
    active: bool = Field(default=True, description="Whether the recurring pattern is active")

    # Relationships
    user: Optional[User] = Relationship(back_populates="recurring_tasks")
    task: Optional[Task] = Relationship(back_populates="recurring_pattern")

    @validator("frequency")
    def validate_frequency(cls, v):
        """Validate that frequency is one of the allowed values."""
        allowed_frequencies = ["daily", "weekly", "monthly", "yearly"]
        if v not in allowed_frequencies:
            raise ValueError(f"Frequency must be one of {allowed_frequencies}")
        return v.lower()