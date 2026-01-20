"""
Basic OpenAI Agent Template

This is a starter template for creating a simple OpenAI agent.
"""

from agents import Agent, Runner
import asyncio
import os

# Set your OpenAI API key
# os.environ["OPENAI_API_KEY"] = "your-api-key-here"

def create_basic_agent():
    """Create a basic agent with simple instructions."""
    agent = Agent(
        name="Basic Assistant",
        instructions="You are a helpful assistant. Respond to user queries in a clear and concise manner."
    )
    return agent

def run_basic_query():
    """Run a basic query with the agent."""
    agent = create_basic_agent()

    # Synchronous execution
    result = Runner.run_sync(agent, "Hello! Tell me about yourself.")
    print("Response:", result.final_output)

async def run_async_query():
    """Run an asynchronous query with the agent."""
    agent = create_basic_agent()

    result = await Runner.run(agent, "What can you help me with?")
    print("Async Response:", result.final_output)

if __name__ == "__main__":
    run_basic_query()
    asyncio.run(run_async_query())