"""
MCP server foundation with proper tool registration using FastMCP.

Implements the Model Context Protocol server for external tool integration.
"""

from mcp.server.fastmcp import FastMCP


# Initialize MCP server using FastMCP
mcp = FastMCP(
    name="todo-chatbot-mcp-server",
)


def get_server():
    """Get the initialized MCP server instance."""
    return mcp