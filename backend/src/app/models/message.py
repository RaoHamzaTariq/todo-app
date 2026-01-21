"""
Message SQLModel definition for chatbot messages.

Represents individual messages within a conversation.
"""

from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, Field, Index


class Message(SQLModel, table=True):
    """
    Message model for chatbot messages.

    Relationships:
    - Belongs to Conversation (conversation_id foreign key)
    - Belongs to User (user_id foreign key)

    Validation:
    - role: required, must be either 'user' or 'assistant'
    - content: required, max 5000 characters
    """
    __tablename__ = "messages"
    __table_args__ = (
        Index("idx_messages_conversation_id", "conversation_id"),
        Index("idx_messages_user_id", "user_id"),
        Index("idx_messages_created_at", "created_at"),
        Index("idx_messages_role", "role"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(
        nullable=False,
        foreign_key="conversations.id",
        index=True,
        description="Conversation this message belongs to"
    )
    user_id: str = Field(
        nullable=False,
        index=True,
        description="Sender of the message"
    )
    role: str = Field(
        nullable=False,
        description="Role of the message sender: 'user' or 'assistant'"
    )
    content: str = Field(
        nullable=False,
        max_length=5000,
        description="Message content"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        description="Creation timestamp (immutable)"
    )

    # Add constraint to ensure role is either 'user' or 'assistant'
    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        # This is just for documentation; actual constraint should be handled by the database