---
name: openai-agents-sdk
description: Comprehensive framework for building multi-agent workflows with OpenAI Agents SDK, including agents, handoffs, guardrails, sessions, and tools. Use when Claude needs to work with OpenAI's Agents SDK for creating agentic AI applications with specialized agents, coordinated workflows, and production-ready features.
---

# OpenAI Agents SDK

This skill provides comprehensive guidance for building multi-agent workflows using the OpenAI Agents SDK.

## What is OpenAI Agents SDK

The OpenAI Agents SDK is a lightweight yet powerful framework for building multi-agent workflows in Python. It's a production-ready upgrade of OpenAI's previous Swarm experimentation. The SDK provides a small set of powerful primitives:

- **Agents**: LLMs equipped with instructions and tools
- **Handoffs**: Allow agents to delegate to other agents for specific tasks
- **Guardrails**: Enable validation of agent inputs and outputs
- **Sessions**: Automatically maintain conversation history across agent runs
- **Tracing**: Built-in visualization and debugging for agentic flows

## Installation

```bash
pip install openai-agents
```

## Core Concepts

### Basic Agent

Create a simple agent with instructions:

```python
from agents import Agent, Runner

agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant"
)

result = Runner.run_sync(agent, "Write a haiku about recursion in programming.")
print(result.final_output)
```

### Async Execution

For more complex workflows, use async execution:

```python
import asyncio
from agents import Agent, Runner

agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant that responds in haikus."
)

async def main():
    result = await Runner.run(agent, "Explain machine learning.")
    print(result.final_output)

asyncio.run(main())
```

## Advanced Features

### Function Tools

Turn any Python function into a tool with automatic schema generation:

```python
from agents import Agent, Runner, function_tool
from pydantic import BaseModel, Field
from typing import Annotated

# Define structured output
class Weather(BaseModel):
    city: str = Field(description="The city name")
    temperature_range: str = Field(description="Temperature in Celsius")
    conditions: str = Field(description="Weather conditions")

# Create function tool
@function_tool
def get_weather(city: Annotated[str, "The city to get weather for"]) -> Weather:
    """Get current weather information for a specified city."""
    # In production, this would call a real weather API
    return Weather(
        city=city,
        temperature_range="14-20C",
        conditions="Sunny with wind."
    )

# Attach tools to agent
agent = Agent(
    name="Weather Assistant",
    instructions="You are a helpful weather assistant.",
    tools=[get_weather]
)

async def main():
    result = await Runner.run(agent, "What's the weather in Tokyo?")
    print(result.final_output)

asyncio.run(main())
```

### Multi-Agent Workflows with Handoffs

Create specialized agents and route requests between them:

```python
from agents import Agent, Runner
import asyncio

spanish_agent = Agent(
    name="Spanish agent",
    instructions="You only speak Spanish.",
)

english_agent = Agent(
    name="English agent",
    instructions="You only speak English",
)

triage_agent = Agent(
    name="Triage agent",
    instructions="Handoff to the appropriate agent based on the language of the request.",
    handoffs=[spanish_agent, english_agent],
)

async def main():
    result = await Runner.run(triage_agent, input="Hola, ¿cómo estás?")
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
```

### Input Guardrails

Validate user inputs before processing:

```python
from agents import Agent, InputGuardrail, GuardrailFunctionOutput, Runner
from agents.exceptions import InputGuardrailTripwireTriggered
from pydantic import BaseModel
import asyncio

class HomeworkOutput(BaseModel):
    is_homework: bool
    reasoning: str

guardrail_agent = Agent(
    name="Guardrail check",
    instructions="Check if the user is asking about homework.",
    output_type=HomeworkOutput,
)

math_tutor_agent = Agent(
    name="Math Tutor",
    handoff_description="Specialist agent for math questions",
    instructions="You provide help with math problems. Explain your reasoning at each step and include examples",
)

history_tutor_agent = Agent(
    name="History Tutor",
    handoff_description="Specialist agent for historical questions",
    instructions="You provide assistance with historical queries. Explain important events and context clearly.",
)

async def homework_guardrail(ctx, agent, input_data):
    result = await Runner.run(guardrail_agent, input_data, context=ctx.context)
    final_output = result.final_output_as(HomeworkOutput)
    return GuardrailFunctionOutput(
        output_info=final_output,
        tripwire_triggered=not final_output.is_homework,
    )

triage_agent = Agent(
    name="Triage Agent",
    instructions="You determine which agent to use based on the user's homework question",
    handoffs=[history_tutor_agent, math_tutor_agent],
    input_guardrails=[
        InputGuardrail(guardrail_function=homework_guardrail),
    ],
)

async def main():
    try:
        result = await Runner.run(triage_agent, "who was the first president of the united states?")
        print(result.final_output)
    except InputGuardrailTripwireTriggered as e:
        print("Guardrail blocked this input:", e)

if __name__ == "__main__":
    asyncio.run(main())
```

### Session Management

Maintain conversation history across multiple interactions:

```python
import asyncio
from agents import Agent, Runner, SQLiteSession

agent = Agent(
    name="Assistant",
    instructions="Reply very concisely."
)

async def main():
    # Create persistent session
    session = SQLiteSession("conversation_123", "conversations.db")

    # First turn
    result = await Runner.run(
        agent,
        "What city is the Golden Gate Bridge in?",
        session=session
    )
    print(result.final_output)  # San Francisco

    # Second turn - agent remembers context automatically
    result = await Runner.run(
        agent,
        "What state is it in?",
        session=session
    )
    print(result.final_output)  # California

    # Retrieve conversation history
    history = await session.get_items()
    print(f"Total items in session: {len(history)}")

asyncio.run(main())
```

## Session Types

The SDK supports different session implementations:

- `SQLiteSession`: File-based or in-memory storage
- `RedisSession`: Scalable, distributed deployments
- `OpenAIConversationsSession`: Uses OpenAI's Conversations API

## Best Practices

- Use async execution for complex workflows
- Implement guardrails for input validation
- Use sessions for maintaining context in multi-turn conversations
- Structure tool outputs with Pydantic models for type safety
- Leverage handoffs for routing between specialized agents

## When to Use This Skill

Use when Claude needs to:
1. Create multi-agent workflows
2. Build specialized agents with specific functions
3. Implement tool usage in agents
4. Manage conversation history with sessions
5. Add input/output validation with guardrails
6. Coordinate between multiple agents using handoffs