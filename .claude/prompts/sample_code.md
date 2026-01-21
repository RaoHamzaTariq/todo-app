This is the Sample Code of MCP Server Creation with proper tools and their integeration with OpenAI Agents SDK

## MCP Server Logic Code (server.py)
```python
"""FastMCP quickstart example.

Run from the repository root:
    uv run examples/snippets/servers/fastmcp_quickstart.py
"""

from mcp.server.fastmcp import FastMCP
import asyncio

# Create an MCP server
mcp = FastMCP(
    name="Demo",
    # stateless_http=True # When true we don't need handshake or initialize things.
)

# Add an addition tool
@mcp.tool()
async def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

@mcp.tool()
async def check_weather(city:str)->str:
    "Check the weather of the city"
    return f"Weather of {city} is Awesome!"


# Run the server over stdio
if __name__ == "__main__":
    # This starts the MCP server reading/writing JSON messages over stdin/stdout       
    asyncio.run(mcp.run_stdio_async())
```
## Agent Logic with mcp tools calls and integeration
```python
import asyncio
from agents import Agent, OpenAIChatCompletionsModel, Runner
from agents.mcp import MCPServerStdio
from openai import AsyncOpenAI
from dotenv import load_dotenv
load_dotenv()
import os

groq_api_key = os.getenv("GROQ_API_KEY")
client = AsyncOpenAI(
    api_key=groq_api_key,
    base_url="https://api.groq.com/openai/v1",
)
model=OpenAIChatCompletionsModel(model="moonshotai/kimi-k2-instruct", openai_client=client)


async def run_local_mcp():
    async with MCPServerStdio(
        name="SimpleAddMCP",
        params={
            "command": "python3",
            "args": ["-m","local_mcp"],
        },
    ) as server:
        print( await server.list_tools())
        agent = Agent(
            name="AI Agent",
            instructions="Help user to answer question using mcp tools",
            mcp_servers=[server],
            model=model
        )

        result = await Runner.run(agent, "Add 2 + 2 and Also tell me the weather of the karachi")
        print(result.final_output)

asyncio.run(run_local_mcp())

```