"""
MCP server for task operations using FastMCP.

Implements the task management tools that can be called by the OpenAI agent.
Based on the FastMCP quickstart example pattern.
"""

import os
from mcp.server.fastmcp import FastMCP
import asyncio
from .tools import register_mcp_tools
from mcp.server.transport_security import TransportSecuritySettings

RENDER_HOST = os.environ.get("RENDER_EXTERNAL_HOSTNAME", "*.onrender.com")

# Create an MCP server
mcp = FastMCP(
    name="todo-task-mcp",
    # Note: Not using stateless_http here since we're using stdio
    stateless_http=True,
    transport_security=TransportSecuritySettings(
        enable_dns_rebinding_protection=True,
        allowed_hosts=[RENDER_HOST, "localhost", "127.0.0.1"]
    )
)

# Register all tools
mcp = register_mcp_tools(mcp)


# Add a health check tool following MCP Builder patterns
@mcp.tool()
async def health_check() -> str:
    """Check the health status of the MCP server"""
    return "MCP server is running and healthy"

mcp_server = mcp.streamable_http_app()


