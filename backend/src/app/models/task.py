"""
Task SQLModel definition for todo items.

Supports full CRUD operations with strict ownership enforcement.
All tasks are owned by a specific user (user_id foreign key).
"""

from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, Field, Index


class Task(SQLModel, table=True):
    """
    Task model for todo items.

    Relationships:
    - Belongs to User (user_id foreign key)

    Validation:
    - title: required, 1-200 characters
    - description: optional, max 1000 characters
    - user_id: required, immutable after creation
    """
    __tablename__ = "tasks"
    __table_args__ = (
        Index("idx_tasks_user_id", "user_id"),
        Index("idx_tasks_completed", "completed"),
        Index("idx_tasks_user_completed", "user_id", "completed"),
        Index("idx_tasks_created_at", "created_at"),
        Index("idx_tasks_title", "title"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(
        nullable=False,
        index=True,
        description="Owner of the task (immutable)"
    )
    title: str = Field(
        min_length=1,
        max_length=200,
        nullable=False,
        description="Task title (required)"
    )
    description: Optional[str] = Field(
        default=None,
        max_length=1000,
        description="Optional task description"
    )
    completed: bool = Field(
        default=False,
        nullable=False,
        description="Completion status"
    )
    priority: str = Field(
        default="medium",
        nullable=False,
        description="Task priority: low, medium, high"
    )
    is_starred: bool = Field(
        default=False,
        nullable=False,
        description="Mark as important",
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        description="Creation timestamp (immutable)"
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        description="Last modification timestamp"
    )
