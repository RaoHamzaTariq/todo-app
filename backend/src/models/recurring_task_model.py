"""
RecurringTask model for the Todo Chatbot application.
This model represents recurring task patterns that generate task instances.
"""

from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from pydantic import validator
from uuid import uuid4


class RecurringTaskBase(SQLModel):
    """Base class for RecurringTask model with common fields."""
    title: str = Field(min_length=1, max_length=255, description="Title for the recurring task")
    description: Optional[str] = Field(default=None, max_length=1000, description="Description for the recurring task")
    user_id: str = Field(description="Owner of the recurring task")
    frequency: str = Field(description="Frequency pattern (daily, weekly, monthly, yearly)")
    interval: int = Field(default=1, description="Interval multiplier for frequency")
    end_date: Optional[datetime] = Field(default=None, description="End date for recurrence (optional)")
    active: bool = Field(default=True, description="Whether the recurring pattern is active")


class RecurringTask(RecurringTaskBase, table=True):
    """RecurringTask model representing a recurring task pattern."""
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp")

    # Relationships
    user: Optional["User"] = Relationship(back_populates="recurring_tasks")
    task: Optional["Task"] = Relationship(back_populates="recurring_pattern",
                                       sa_relationship_kwargs={"uselist": False})

    # Validation rules
    @validator("frequency")
    def validate_frequency(cls, v):
        """Validate that frequency is one of the allowed values."""
        allowed_frequencies = ["daily", "weekly", "monthly", "yearly"]
        if v not in allowed_frequencies:
            raise ValueError(f"Frequency must be one of {allowed_frequencies}")
        return v.lower()

    @validator("interval")
    def validate_interval(cls, v):
        """Validate that interval is a positive integer."""
        if v <= 0:
            raise ValueError("Interval must be a positive integer")
        return v

    @validator("title")
    def validate_title(cls, v):
        """Validate recurring task title length."""
        if not v or len(v.strip()) == 0:
            raise ValueError("Title cannot be empty")
        if len(v) > 255:
            raise ValueError("Title must be 255 characters or less")
        return v.strip()

    @validator("end_date")
    def validate_end_date(cls, v, values):
        """Validate that end date is not in the past."""
        if v and v < datetime.utcnow():
            raise ValueError("End date cannot be in the past")
        return v

    def is_active_on_date(self, check_date: datetime) -> bool:
        """Check if this recurring task is active on a specific date."""
        if not self.active:
            return False

        if self.end_date and check_date > self.end_date:
            return False

        return True

    def calculate_next_occurrence(self, from_date: datetime) -> Optional[datetime]:
        """Calculate the next occurrence based on the frequency and interval."""
        if not self.is_active_on_date(from_date):
            return None

        # Calculate next occurrence based on frequency
        if self.frequency == "daily":
            next_date = from_date.date()
            # Add the interval
            import datetime as dt_module
            next_date = next_date + dt_module.timedelta(days=self.interval)
            # Combine date and time
            next_datetime = datetime.combine(next_date, from_date.time())

        elif self.frequency == "weekly":
            next_date = from_date.date()
            import datetime as dt_module
            next_date = next_date + dt_module.timedelta(weeks=self.interval)
            next_datetime = datetime.combine(next_date, from_date.time())

        elif self.frequency == "monthly":
            # Monthly calculation is more complex
            next_datetime = self._calculate_next_monthly_occurrence(from_date)

        elif self.frequency == "yearly":
            next_datetime = from_date.replace(year=from_date.year + self.interval)

        else:
            # Should not happen due to validation, but just in case
            return None

        # Check if the calculated date is still within the end_date limit
        if self.end_date and next_datetime > self.end_date:
            return None

        return next_datetime

    def _calculate_next_monthly_occurrence(self, from_date: datetime) -> datetime:
        """Helper to calculate the next monthly occurrence."""
        import calendar
        year = from_date.year
        month = from_date.month + self.interval

        # Adjust year if month > 12
        while month > 12:
            year += 1
            month -= 12

        # Handle day overflow (e.g., Jan 31 + 1 month -> Feb 28/29)
        max_day = calendar.monthrange(year, month)[1]
        day = min(from_date.day, max_day)

        return datetime(year, month, day, from_date.hour, from_date.minute, from_date.second)

    def to_dict(self) -> dict:
        """Convert recurring task to dictionary representation."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "description": self.description,
            "frequency": self.frequency,
            "interval": self.interval,
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "active": self.active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }


# Need to import User here to avoid circular imports
# The User model would typically be defined in a separate user_model.py file
# For this implementation, we'll use a forward reference approach
try:
    from .task_model import User, Task
except ImportError:
    # In case we're in a different context
    pass