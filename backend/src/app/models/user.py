"""
Better Auth User model reference.

This model represents the user table created by Better Auth.
The backend uses this only for SQLAlchemy relationship definitions
and type hints. The actual user table is managed by Better Auth.
"""

from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    """
    Better Auth User model reference for type hints and foreign key relationships.

    Note: This table is managed by Better Auth and should not be modified by the backend.
    The backend uses this only for SQLAlchemy relationship definitions and type hints.
    """
    __tablename__ = "user"  # Better Auth creates this as "user" not "users"

    id: str = Field(primary_key=True)  # Better Auth user ID
    name: str = Field(nullable=False)  # Better Auth name field
    email: str = Field(unique=True, nullable=False)  # Better Auth email field
    emailVerified: bool = Field(default=False, nullable=False)  # Better Auth field name
    image: Optional[str] = Field(default=None)  # Better Auth image field
    createdAt: datetime = Field(default_factory=datetime.utcnow, nullable=False)  # Better Auth field
    updatedAt: datetime = Field(default_factory=datetime.utcnow, nullable=False)  # Better Auth field
