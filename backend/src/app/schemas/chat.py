"""
Chat-related Pydantic schemas for request/response validation.
"""

from pydantic import BaseModel
from typing import List
from datetime import datetime


class CreateConversationRequest(BaseModel):
    """Request model for creating a new conversation."""
    pass  # Currently no additional fields needed


class CreateConversationResponse(BaseModel):
    """Response model for creating a new conversation."""
    id: int
    user_id: str
    created_at: datetime
    updated_at: datetime


class CreateMessageRequest(BaseModel):
    """Request model for sending a message."""
    content: str


class CreateMessageResponse(BaseModel):
    """Response model for sending a message."""
    id: int
    conversation_id: int
    user_id: str
    role: str
    content: str
    created_at: datetime


class MessageResponse(BaseModel):
    """Response model for a message."""
    id: int
    conversation_id: int
    user_id: str
    role: str
    content: str
    created_at: datetime


class ConversationResponse(BaseModel):
    """Response model for a conversation."""
    id: int
    user_id: str
    created_at: datetime
    updated_at: datetime


class ListMessagesResponse(BaseModel):
    """Response model for listing messages."""
    messages: List[MessageResponse]


class ListConversationsResponse(BaseModel):
    """Response model for listing conversations."""
    conversations: List[ConversationResponse]