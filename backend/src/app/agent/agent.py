"""
OpenAI Agent configuration with MCP tools integration.

Configures the OpenAI Agent to work with MCP tools for task operations.
Implements the integration patterns required by OpenAI Agents SDK following the skill guidelines.
"""

import asyncio
from typing import Dict, Any, List, Optional
from agents import Agent, Runner
from ..mcp.server import get_server
from ..mcp.tools import register_mcp_tools


class TodoChatAgent:
    """
    OpenAI Agent configured for todo chat operations with MCP tools integration.

    This class encapsulates the OpenAI Agent configuration and provides
    methods for processing natural language queries using MCP tools.
    """

    def __init__(self):
        """
        Initialize the Todo Chat Agent following OpenAI Agents SDK patterns.
        """
        # Get the MCP server instance and register tools
        self.mcp = get_server()
        register_mcp_tools(self.mcp)

    async def process_query(self, user_id: str, query: str) -> Dict[str, Any]:
        """
        Process a natural language query using the OpenAI Agent with MCP server integration.

        Args:
            user_id: The ID of the user making the request
            query: The natural language query from the user

        Returns:
            Dictionary containing the agent's response
        """
        try:
            # Create the agent with instructions and tools
            # The tools are registered with the FastMCP server instance
            agent = Agent(
                name="Todo Assistant",
                instructions="You are a helpful task management assistant. Help users manage their tasks by creating, listing, updating, completing, and deleting tasks. Use the available tools to perform these operations. Always confirm important actions like deletions before proceeding. Be concise but friendly in your responses.",
                # The tools are automatically available through the registered MCP server
            )

            # Use the Runner to execute the agent with the query
            result = await Runner.run(agent, query)

            return {
                "response": result.final_output,
                "success": True
            }
        except Exception as e:
            return {
                "response": f"I'm sorry, I encountered an error processing your request: {str(e)}",
                "success": False,
                "error": str(e)
            }


# Global agent instance
_todo_agent = None


def get_agent() -> TodoChatAgent:
    """
    Get the singleton instance of the Todo Chat Agent.

    Returns:
        TodoChatAgent instance
    """
    global _todo_agent
    if _todo_agent is None:
        _todo_agent = TodoChatAgent()
    return _todo_agent