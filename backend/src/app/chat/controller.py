"""
Base chat controller with conversation history loading and OpenAI Agent initialization.

Implements the core chat functionality integrating OpenAI Agents SDK with MCP tools.
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any, Optional
from pydantic import BaseModel
from sqlmodel import Session
import asyncio
from ..database import get_session_context
from ..models.conversation import Conversation
from ..models.message import Message
from ..mcp.tools import register_mcp_tools
from ..mcp.server import get_server, initialize_openai_integration
from ..agent.agent import get_agent
from ..middleware.auth import verify_token


class ChatRequest(BaseModel):
    conversation_id: int
    message: str


class ChatResponse(BaseModel):
    conversation_id: int
    response: str
    tool_calls: Optional[list] = []


router = APIRouter(prefix="/api/{user_id}/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
async def process_chat_message(
    user_id: str,
    request: ChatRequest,
    token_data: dict = Depends(verify_token)
):
    """
    Process chat message and return AI response.

    Integrates OpenAI Agent with MCP tools for task operations.
    """
    # Verify user authorization
    if token_data.get("user_id") != user_id:
        raise HTTPException(status_code=403, detail="Unauthorized access to user data")

    try:
        # Load conversation history
        with get_session_context() as session:
            # Verify conversation exists and belongs to user
            conversation = session.get(Conversation, request.conversation_id)
            if not conversation or conversation.user_id != user_id:
                raise HTTPException(status_code=404, detail="Conversation not found")

        # Get the agent instance and process the query
        agent = get_agent()

        result = await agent.process_query(user_id, request.message)

        return ChatResponse(
            conversation_id=request.conversation_id,
            response=result.get("response", "No response generated"),
            tool_calls=[]  # The agent handles tool calls internally
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat message: {str(e)}")


@router.get("/{conversation_id}", response_model=dict)
async def get_conversation_history(
    user_id: str,
    conversation_id: int,
    token_data: dict = Depends(verify_token)
):
    """
    Get conversation history.

    Retrieves the full history of messages in a specific conversation.
    """
    # Verify user authorization
    if token_data.get("user_id") != user_id:
        raise HTTPException(status_code=403, detail="Unauthorized access to user data")

    try:
        with get_session_context() as session:
            # Verify conversation exists and belongs to user
            conversation = session.get(Conversation, conversation_id)
            if not conversation or conversation.user_id != user_id:
                raise HTTPException(status_code=404, detail="Conversation not found")

            # Retrieve messages for this conversation
            # In a real implementation: query messages from database
            messages = []  # This would come from the database

        return {
            "conversation_id": conversation_id,
            "messages": messages
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving conversation history: {str(e)}")


async def initialize_chat_agent():
    """
    Initialize the OpenAI Agent for chat operations.

    Sets up the agent with proper MCP tool integration.
    """
    print("Initializing OpenAI Agent for chat operations...")
    # Initialize MCP server integration
    await initialize_openai_integration()