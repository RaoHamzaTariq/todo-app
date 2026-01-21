"""
MCP server for task operations using FastMCP.

Implements the task management tools that can be called by the OpenAI agent.
Based on the FastMCP quickstart example pattern.
"""

from mcp.server.fastmcp import FastMCP
import asyncio
from .tools import register_mcp_tools


# Create an MCP server
mcp = FastMCP(
    name="todo-task-mcp",
    # Note: Not using stateless_http here since we're using stdio
)

# Register all tools
mcp = register_mcp_tools(mcp)


# Add a health check tool following MCP Builder patterns
@mcp.tool()
async def health_check() -> str:
    """Check the health status of the MCP server"""
    return "MCP server is running and healthy"


# Run the server over stdio
if __name__ == "__main__":
    # This starts the MCP server reading/writing JSON messages over stdin/stdout
    asyncio.run(mcp.run_stdio_async())