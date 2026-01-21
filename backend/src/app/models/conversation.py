"""
Conversation SQLModel definition for chatbot conversations.

Represents a persistent conversation thread with history.
"""

from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, Field, Index


class Conversation(SQLModel, table=True):
    """
    Conversation model for chatbot conversations.

    Relationships:
    - Belongs to User (user_id foreign key)
    - Has many Messages (conversation_id foreign key)

    Validation:
    - user_id: required, links conversation to owner
    """
    __tablename__ = "conversations"
    __table_args__ = (
        Index("idx_conversations_user_id", "user_id"),
        Index("idx_conversations_updated_at", "updated_at"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(
        nullable=False,
        index=True,
        description="Owner of the conversation (immutable)"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        description="Creation timestamp (immutable)"
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        description="Last activity timestamp"
    )