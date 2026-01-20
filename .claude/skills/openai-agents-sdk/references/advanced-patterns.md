# OpenAI Agents SDK - Advanced Patterns

## Multi-Agent Architecture Patterns

### Supervisor Pattern
A supervisor agent manages and coordinates multiple worker agents:

```python
from agents import Agent, Runner
import asyncio

researcher_agent = Agent(
    name="Researcher",
    instructions="You research topics and provide factual information."
)

writer_agent = Agent(
    name="Writer",
    instructions="You write well-structured content based on research."
)

supervisor_agent = Agent(
    name="Supervisor",
    instructions="Coordinate between researcher and writer agents to produce high-quality content.",
    handoffs=[researcher_agent, writer_agent]
)
```

### Sequential Handoff Pattern
Agents process requests in sequence:

```python
from agents import Agent, Runner, realtime_handoff
import asyncio

validation_agent = Agent(
    name="Validator",
    instructions="Validate user inputs and check for compliance."
)

processing_agent = Agent(
    name="Processor",
    instructions="Process validated inputs and perform computations."
)

reporting_agent = Agent(
    name="Reporter",
    instructions="Generate reports based on processed data."
)

orchestrator_agent = Agent(
    name="Orchestrator",
    instructions="Route requests through validation, processing, and reporting stages.",
    handoffs=[validation_agent, processing_agent, reporting_agent]
)
```

## Complex Tool Usage

### Async Tools
For tools that make network requests or perform I/O operations:

```python
from agents import function_tool
import aiohttp
import asyncio

@function_tool
async def fetch_web_data(url: str) -> dict:
    """Fetch data from a web API."""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

# Attach to agent
web_agent = Agent(
    name="Web Data Agent",
    instructions="Fetch and analyze data from web APIs.",
    tools=[fetch_web_data]
)
```

### Context-Aware Tools
Tools that can access the current run context:

```python
from agents import function_tool, RunContextWrapper
from typing import Any

@function_tool
def log_user_action(
    ctx: RunContextWrapper[Any],
    action: str,
    details: str = ""
) -> str:
    """Log user actions for analytics."""
    session_id = getattr(ctx, 'session_id', 'unknown')
    # In practice, you'd log to a database or logging service
    print(f"[{session_id}] User performed: {action} ({details})")
    return f"Logged action: {action}"

contextual_agent = Agent(
    name="Contextual Agent",
    instructions="Provide personalized assistance based on user context.",
    tools=[log_user_action]
)
```

## Session Management Strategies

### Memory-Conscious Sessions
For applications where you want to control how much history to retain:

```python
from agents import SQLiteSession

# Create a session that keeps only the last 10 interactions
session = SQLiteSession(
    session_id="user_123_conversation",
    db_path="conversations.db",
    max_history_length=10  # Only keep last 10 exchanges
)
```

### Cross-Session State
For maintaining persistent user preferences or data:

```python
class UserProfile:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.preferences = {}
        self.history_summary = ""

# Store in session context
session = SQLiteSession("session_123", "db.sqlite")
session.set_context("user_profile", UserProfile("user_123"))
```