"""
Chat API endpoints with JWT authentication and conversation management.

Provides endpoints for managing chat conversations and messages with proper user isolation.
"""

import asyncio
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from datetime import datetime

from src.app.database import get_session
from src.app.middleware.auth import jwt_bearer
from src.app.models.conversation import Conversation
from src.app.models.message import Message
from src.app.schemas.error import ErrorResponse
from src.app.agent.agent import get_agent
from src.app.services.task_service import TaskService


router = APIRouter(prefix="/api", tags=["chat"])


def verify_user_id_match(path_user_id: str, auth_user_id: str) -> None:
    """
    Verify that the user_id in the path matches the authenticated user's ID.

    This prevents users from accessing or modifying other users' data.

    Args:
        path_user_id: user_id from the URL path
        auth_user_id: user_id extracted from JWT token

    Raises:
        HTTPException: 403 if IDs don't match
    """
    if path_user_id != auth_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: user ID mismatch"
        )


class ChatService:
    """
    Service class for handling chat operations including conversation and message management.
    """

    def __init__(self, session: Session):
        self.session = session

    def create_conversation(self, user_id: str) -> Conversation:
        """
        Create a new conversation for a user.

        Args:
            user_id: ID of the user creating the conversation

        Returns:
            Created Conversation object
        """
        conversation = Conversation(
            user_id=user_id,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        self.session.add(conversation)
        self.session.commit()
        self.session.refresh(conversation)
        return conversation

    def get_conversation(self, conversation_id: int, user_id: str) -> Optional[Conversation]:
        """
        Get a specific conversation by ID for a user.

        Args:
            conversation_id: ID of the conversation
            user_id: ID of the user who owns the conversation

        Returns:
            Conversation object if found and owned by user, None otherwise
        """
        statement = select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id
        )
        return self.session.exec(statement).first()

    def get_user_conversations(self, user_id: str) -> List[Conversation]:
        """
        Get all conversations for a user.

        Args:
            user_id: ID of the user

        Returns:
            List of Conversation objects
        """
        statement = select(Conversation).where(Conversation.user_id == user_id).order_by(Conversation.updated_at.desc())
        return self.session.exec(statement).all()

    def create_message(self, conversation_id: int, user_id: str, role: str, content: str) -> Message:
        """
        Create a new message in a conversation.

        Args:
            conversation_id: ID of the conversation
            user_id: ID of the user creating the message
            role: Role of the message sender ('user' or 'assistant')
            content: Content of the message

        Returns:
            Created Message object
        """
        # Verify conversation belongs to user
        conversation = self.get_conversation(conversation_id, user_id)
        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found or access denied"
            )

        message = Message(
            conversation_id=conversation_id,
            user_id=user_id,
            role=role,
            content=content,
            created_at=datetime.utcnow()
        )
        self.session.add(message)

        # Update conversation's updated_at timestamp
        conversation.updated_at = datetime.utcnow()
        self.session.add(conversation)

        self.session.commit()
        self.session.refresh(message)
        return message

    def get_conversation_messages(self, conversation_id: int, user_id: str) -> List[Message]:
        """
        Get all messages for a conversation.

        Args:
            conversation_id: ID of the conversation
            user_id: ID of the user who owns the conversation

        Returns:
            List of Message objects
        """
        conversation = self.get_conversation(conversation_id, user_id)
        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found or access denied"
            )

        statement = select(Message).where(Message.conversation_id == conversation_id).order_by(Message.created_at.asc())
        return self.session.exec(statement).all()


from src.app.schemas.chat import (
    CreateConversationRequest,
    CreateConversationResponse,
    CreateMessageRequest,
    CreateMessageResponse,
    MessageResponse,
    ConversationResponse,
    ListMessagesResponse,
    ListConversationsResponse,
)


@router.post(
    "/{user_id}/conversations",
    response_model=CreateConversationResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        401: {"model": ErrorResponse, "description": "Invalid or missing token"},
        403: {"model": ErrorResponse, "description": "User ID mismatch"},
    }
)
async def create_conversation(
    user_id: str,
    request: CreateConversationRequest,
    auth_user: dict = Depends(jwt_bearer),
    session: Session = Depends(get_session),
):
    """
    Create a new conversation for the authenticated user.

    The conversation is assigned to the user_id from the JWT token (not from request body).
    This ensures strict user data isolation.
    """
    # Verify ownership
    verify_user_id_match(user_id, auth_user["user_id"])

    # Create conversation using user_id from JWT
    chat_service = ChatService(session)
    conversation = chat_service.create_conversation(auth_user["user_id"])

    return CreateConversationResponse(
        id=conversation.id,
        user_id=conversation.user_id,
        created_at=conversation.created_at,
        updated_at=conversation.updated_at
    )


@router.get(
    "/{user_id}/conversations",
    response_model=ListConversationsResponse,
    responses={
        401: {"model": ErrorResponse, "description": "Invalid or missing token"},
        403: {"model": ErrorResponse, "description": "User ID mismatch"},
    }
)
async def list_conversations(
    user_id: str,
    auth_user: dict = Depends(jwt_bearer),
    session: Session = Depends(get_session),
):
    """
    List all conversations for the authenticated user.

    Returns only conversations owned by the authenticated user (user isolation).
    Results are ordered by most recent activity.
    """
    # Verify ownership
    verify_user_id_match(user_id, auth_user["user_id"])

    # Get conversations for this user
    chat_service = ChatService(session)
    conversations = chat_service.get_user_conversations(auth_user["user_id"])

    return ListConversationsResponse(
        conversations=[
            ConversationResponse(
                id=c.id,
                user_id=c.user_id,
                created_at=c.created_at,
                updated_at=c.updated_at
            ) for c in conversations
        ]
    )


@router.get(
    "/{user_id}/conversations/{conversation_id}",
    response_model=ConversationResponse,
    responses={
        401: {"model": ErrorResponse, "description": "Invalid or missing token"},
        403: {"model": ErrorResponse, "description": "User ID mismatch"},
        404: {"model": ErrorResponse, "description": "Conversation not found"},
    }
)
async def get_conversation(
    user_id: str,
    conversation_id: int,
    auth_user: dict = Depends(jwt_bearer),
    session: Session = Depends(get_session),
):
    """
    Get a specific conversation by ID.

    Returns 404 if conversation doesn't exist or belongs to a different user.
    This prevents information disclosure about conversation existence.
    """
    # Verify ownership
    verify_user_id_match(user_id, auth_user["user_id"])

    # Get conversation with ownership check
    chat_service = ChatService(session)
    conversation = chat_service.get_conversation(conversation_id, auth_user["user_id"])

    if conversation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )

    return ConversationResponse(
        id=conversation.id,
        user_id=conversation.user_id,
        created_at=conversation.created_at,
        updated_at=conversation.updated_at
    )


@router.post(
    "/{user_id}/conversations/{conversation_id}/messages",
    response_model=CreateMessageResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        401: {"model": ErrorResponse, "description": "Invalid or missing token"},
        403: {"model": ErrorResponse, "description": "User ID mismatch"},
        404: {"model": ErrorResponse, "description": "Conversation not found"},
        422: {"model": ErrorResponse, "description": "Validation error"},
    }
)
async def send_message(
    user_id: str,
    conversation_id: int,
    request: CreateMessageRequest,
    auth_user: dict = Depends(jwt_bearer),
    session: Session = Depends(get_session),
):
    """
    Send a message in a conversation and get a response from the chatbot.

    Creates a user message and generates an assistant response using the AI agent.
    Both messages are saved to the conversation history.
    """
    # Verify ownership
    verify_user_id_match(user_id, auth_user["user_id"])

    # Create user message
    chat_service = ChatService(session)

    # Create the user's message
    user_message = chat_service.create_message(
        conversation_id=conversation_id,
        user_id=auth_user["user_id"],
        role="user",
        content=request.content
    )

    # Get agent response with timeout handling
    try:
        agent = get_agent()

        # Wrap the agent call with a timeout to prevent indefinite hanging
        agent_response = await asyncio.wait_for(
            agent.process_query(auth_user["user_id"], request.content),
            timeout=30.0  # 30-second timeout for agent processing
        )

        # Create the assistant's response message
        assistant_message = chat_service.create_message(
            conversation_id=conversation_id,
            user_id=auth_user["user_id"],  # Same user_id since it's part of the conversation
            role="assistant",
            content=agent_response.get("response", "I couldn't process that request.")
        )

        return assistant_message

    except asyncio.TimeoutError:
        print(f"Timeout error processing agent query for user {auth_user['user_id']}")
        error_message = chat_service.create_message(
            conversation_id=conversation_id,
            user_id=auth_user["user_id"],
            role="assistant",
            content="I'm sorry, I encountered a timeout while processing your request. The response took too long to generate."
        )
        return error_message

    except Exception as e:
        # Log the error and return a generic response
        print(f"Error processing agent query: {e}")
        error_message = chat_service.create_message(
            conversation_id=conversation_id,
            user_id=auth_user["user_id"],
            role="assistant",
            content=f"I'm sorry, I encountered an error processing your request: {str(e)[:200]}..."  # Limit length
        )

        return error_message


@router.get(
    "/{user_id}/conversations/{conversation_id}/messages",
    response_model=ListMessagesResponse,
    responses={
        401: {"model": ErrorResponse, "description": "Invalid or missing token"},
        403: {"model": ErrorResponse, "description": "User ID mismatch"},
        404: {"model": ErrorResponse, "description": "Conversation not found"},
    }
)
async def list_messages(
    user_id: str,
    conversation_id: int,
    auth_user: dict = Depends(jwt_bearer),
    session: Session = Depends(get_session),
):
    """
    List all messages in a conversation.

    Returns 404 if conversation doesn't exist or belongs to a different user.
    Messages are ordered chronologically (oldest first).
    """
    # Verify ownership
    verify_user_id_match(user_id, auth_user["user_id"])

    # Get messages with ownership check
    chat_service = ChatService(session)
    messages = chat_service.get_conversation_messages(conversation_id, auth_user["user_id"])

    return ListMessagesResponse(
        messages=[
            MessageResponse(
                id=m.id,
                conversation_id=m.conversation_id,
                user_id=m.user_id,
                role=m.role,
                content=m.content,
                created_at=m.created_at
            ) for m in messages
        ]
    )