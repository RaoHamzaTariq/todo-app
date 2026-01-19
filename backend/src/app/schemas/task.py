"""
Pydantic schemas for Task API request/response validation.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class CreateTaskInput(BaseModel):
    """Schema for creating a new task."""

    title: str = Field(
        min_length=1,
        max_length=200,
        description="Task title (required)"
    )
    description: Optional[str] = Field(
        default=None,
        max_length=1000,
        description="Task description (optional)"
    )
    priority: str = Field(default="medium", description="Task priority")
    starred: bool = Field(default=False, description="Is task starred")

    @field_validator("title")
    @classmethod
    def title_not_empty(cls, v: str) -> str:
        """Ensure title is not empty or whitespace only."""
        if not v or not v.strip():
            raise ValueError("Title cannot be empty or whitespace")
        return v.strip()


class UpdateTaskInput(BaseModel):
    """Schema for updating an existing task."""

    title: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=200,
        description="Task title (optional)"
    )
    description: Optional[str] = Field(
        default=None,
        max_length=1000,
        description="Task description (optional)"
    )
    completed: Optional[bool] = None
    priority: Optional[str] = None
    starred: Optional[bool] = None

    @field_validator("title")
    @classmethod
    def title_not_empty(cls, v: Optional[str]) -> Optional[str]:
        """Ensure title is not empty or whitespace if provided."""
        if v is not None and (not v or not v.strip()):
            raise ValueError("Title cannot be empty or whitespace")
        return v.strip() if v else v


class TaskResponse(BaseModel):
    """Schema for task API responses."""

    id: int
    user_id: str
    title: str
    description: Optional[str]
    completed: bool
    priority: str
    starred: bool = Field(alias="is_starred") # Map DB is_starred to response starred
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Enable ORM mode for SQLModel compatibility
        populate_by_name = True # Allow populating by alias


class TaskListResponse(BaseModel):
    """Schema for list tasks endpoint response."""

    tasks: list[TaskResponse]
