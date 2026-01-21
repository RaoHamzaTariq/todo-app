"""
OpenAI Agent configuration with MCP tools integration.

Configures the OpenAI Agent to work with MCP tools for task operations.
Implements the integration patterns required by OpenAI Agents SDK following the skill guidelines.
"""

from typing import Dict, Any
from .integration import get_agent_integration


class TodoChatAgent:
    """
    OpenAI Agent configured for todo chat operations with MCP tools integration.

    This class encapsulates the OpenAI Agent configuration and provides
    methods for processing natural language queries using MCP tools.
    """

    def __init__(self, api_key: str = None):
        """
        Initialize the Todo Chat Agent following OpenAI Agents SDK patterns.

        Args:
            api_key: OpenAI API key (optional, will use environment if not provided)
        """
        self.integration = get_agent_integration(api_key=api_key)

    async def process_query(self, user_id: str, query: str) -> Dict[str, Any]:
        """
        Process a natural language query using the OpenAI Agent with MCP server integration.

        Args:
            user_id: The ID of the user making the request
            query: The natural language query from the user

        Returns:
            Dictionary containing the agent's response
        """
        return await self.integration.process_with_agent(user_id, query)


# Global agent instance
_todo_agent = None


def get_agent(api_key: str = None) -> TodoChatAgent:
    """
    Get the singleton instance of the Todo Chat Agent.

    Args:
        api_key: OpenAI API key (optional, will use environment if not provided)

    Returns:
        TodoChatAgent instance
    """
    global _todo_agent
    if _todo_agent is None:
        _todo_agent = TodoChatAgent(api_key=api_key)
    return _todo_agent