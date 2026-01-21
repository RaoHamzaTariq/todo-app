"""
OpenAI Agent integration with MCP server following the sample code pattern.

Implements the proper integration between OpenAI Agents SDK and MCP tools
as demonstrated in the sample code.
"""

import asyncio
import os
from typing import Dict, Any, Optional
from agents import Agent, OpenAIChatCompletionsModel, Runner,RunConfig
from agents.mcp import MCPServerStdio,MCPServerStreamableHttp,MCPServerStreamableHttpParams
from openai import AsyncOpenAI
from dotenv import load_dotenv
load_dotenv()


class OpenAIAgentMCPIntegration:
    """
    Integration class for connecting OpenAI Agents SDK with MCP server.

    Implements the integration pattern from the sample code with proper
    error handling and resource management.
    """

    def __init__(self, api_key: Optional[str] = os.getenv("OPENAI_API_KEY"), base_url: Optional[str] = os.getenv("OPENAI_BASE_URL"), model_name: str = "moonshotai/kimi-k2-instruct"):
        """
        Initialize the OpenAI Agent MCP Integration.

        Args:
            api_key: API key (defaults to environment)
            base_url: Base URL for API (optional)
            model_name: Name of the model to use
        """
        # Set up OpenAI client
        kwargs = {}
        if api_key:
            kwargs["api_key"] = api_key
        else:
            # Try to get from environment,
            kwargs["api_key"] = os.getenv("OPENAI_API_KEY")

        if base_url:
            kwargs["base_url"] = base_url

        self.client = AsyncOpenAI(**kwargs)
        self.model = OpenAIChatCompletionsModel(model=model_name, openai_client=self.client)
        self.config = RunConfig(model=self.model,model_provider=self.client,tracing_disabled=True)
        self.mcp_url = os.getenv("MCP_SERVER_URL")

    async def process_with_agent(self, user_id: str, query: str) -> Dict[str, Any]:
        """
        Process a query using OpenAI Agent with MCP tools integration.

        Args:
            user_id: The ID of the user making the request
            query: The natural language query from the user

        Returns:
            Dictionary containing the agent's response
        """
        try:
            # Create MCP server using stdio approach from sample code with extended timeout for production
            mcp_params = MCPServerStreamableHttpParams(url=self.mcp_url)
            async with MCPServerStreamableHttp(params=mcp_params, name="MySharedMCPServerClient") as mcp_server_client:
            # async with MCPServerStdio(
            #     name="TodoTaskMCP",
            #     client_session_timeout_seconds=60,  # Increased timeout to 60 seconds for production
            #     params={
            #         "command": "python",
            #         "args": ["-m", "src.app.mcp.server"],
            #     },
            # ) as server:
                # # List available tools for debugging
                # tools = await server.list_tools()
                # print(f"Available tools: {tools}")

                # Create agent with instructions and MCP server integration
                agent = Agent(
                    name="TodoAssistant",
                    instructions=f"""You are a helpful task management assistant for user {user_id}.
                    Help users manage their tasks by creating, listing, updating, completing, and deleting tasks.
                    Use the available tools to perform these operations.
                    Always confirm important actions like deletions before proceeding.
                    Be concise but friendly in your responses.""",
                    mcp_servers=[mcp_server_client],
                    model=self.model
                )

                # Process the query using the agent with extended timeout
                result = await asyncio.wait_for(
                    Runner.run(agent, query, run_config=self.config),
                    timeout=60.0  # 60-second timeout for agent processing in production
                )
                print(result.final_output)
                return {
                    "response": result.final_output,
                    "success": True,
                    "user_id": user_id,
                    "query": query
                }

        except asyncio.TimeoutError:
            return {
                "response": "I'm sorry, I encountered a timeout while processing your request. The response took too long to generate.",
                "success": False,
                "error": "Processing timeout",
                "user_id": user_id,
                "query": query
            }
        except Exception as e:
            return {
                "response": f"I'm sorry, I encountered an error processing your request: {str(e)}",
                "success": False,
                "error": str(e),
                "user_id": user_id,
                "query": query
            }


# Global integration instance
_todo_agent_integration = None


def get_agent_integration(api_key: Optional[str] = None, base_url: Optional[str] = None) -> OpenAIAgentMCPIntegration:
    """
    Get the singleton instance of the OpenAI Agent MCP Integration.

    Args:
        api_key: OpenAI API key (optional)
        base_url: Base URL for OpenAI-compatible API (optional)

    Returns:
        OpenAIAgentMCPIntegration instance
    """
    global _todo_agent_integration
    if _todo_agent_integration is None:
        _todo_agent_integration = OpenAIAgentMCPIntegration(api_key, base_url)
    return _todo_agent_integration


async def process_user_query(user_id: str, query: str, api_key: Optional[str] = None) -> Dict[str, Any]:
    """
    Convenience function to process a user query with agent integration.

    Args:
        user_id: The ID of the user making the request
        query: The natural language query from the user
        api_key: API key (optional)

    Returns:
        Dictionary containing the agent's response
    """
    integration = get_agent_integration(api_key=api_key)
    return await integration.process_with_agent(user_id, query)