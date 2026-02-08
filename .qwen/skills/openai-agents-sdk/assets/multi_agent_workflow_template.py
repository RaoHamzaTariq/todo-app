"""
Multi-Agent Workflow Template

This template demonstrates how to create a multi-agent system with
handoffs, tools, and session management.
"""

from agents import Agent, Runner, function_tool, SQLiteSession
from pydantic import BaseModel, Field
from typing import Annotated
import asyncio
import os

# Set your OpenAI API key
# os.environ["OPENAI_API_KEY"] = "your-api-key-here"

class Task(BaseModel):
    """Structured output for task-related tools."""
    title: str = Field(description="The task title")
    description: str = Field(description="Detailed description of the task")
    priority: str = Field(description="Priority level: low, medium, high")

# Example tools
@function_tool
def create_task(title: Annotated[str, "The task title"],
                description: Annotated[str, "The task description"],
                priority: Annotated[str, "Priority: low, medium, high"] = "medium") -> Task:
    """Create a new task with title, description, and priority."""
    return Task(title=title, description=description, priority=priority)

@function_tool
def get_tasks() -> list[dict]:
    """Get all current tasks."""
    # In a real implementation, this would fetch from a database
    return [{"title": "Sample task", "description": "A sample task", "priority": "medium"}]

# Create specialized agents
def create_task_management_agent():
    """Agent specialized in task management."""
    return Agent(
        name="Task Manager",
        instructions="Manage user tasks by creating, listing, and organizing them. "
                   "Use the create_task and get_tasks tools as needed.",
        tools=[create_task, get_tasks]
    )

def create_general_assistant_agent():
    """General purpose assistant agent."""
    return Agent(
        name="General Assistant",
        instructions="Provide general assistance to the user. "
                   "If the user wants to manage tasks, hand off to the Task Manager."
    )

def create_triage_agent(task_manager_agent):
    """Agent that routes requests to appropriate specialists."""
    return Agent(
        name="Triage Agent",
        instructions="Determine if the user needs general assistance or task management. "
                   "Route task-related requests to the Task Manager.",
        handoffs=[task_manager_agent]
    )

async def run_multi_agent_workflow():
    """Run a multi-agent workflow with session management."""
    # Create agents
    task_manager = create_task_management_agent()
    triage_agent = create_triage_agent(task_manager)

    # Create a session to maintain conversation history
    session = SQLiteSession("multi_agent_demo", "demo_sessions.db")

    # Run initial request
    print("=== Initial Request ===")
    result = await Runner.run(
        triage_agent,
        "I need to create a task to finish the project report by Friday",
        session=session
    )
    print("Response:", result.final_output)

    # Follow-up request in same session
    print("\n=== Follow-up Request ===")
    result = await Runner.run(
        triage_agent,
        "What tasks do I have?",
        session=session
    )
    print("Response:", result.final_output)

if __name__ == "__main__":
    asyncio.run(run_multi_agent_workflow())