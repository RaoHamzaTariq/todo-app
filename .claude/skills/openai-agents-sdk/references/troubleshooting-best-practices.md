# OpenAI Agents SDK - Troubleshooting and Best Practices

## Common Issues and Solutions

### 1. Tool Not Being Called
**Problem**: Agent ignores available tools
**Solution**:
- Ensure the agent's instructions clearly indicate when to use the tool
- Verify the tool description matches the agent's needs
- Check that the tool parameters align with what the agent expects

### 2. Session Context Not Persisting
**Problem**: Agent doesn't remember previous interactions
**Solution**:
- Ensure the same session object is passed to each Runner.run() call
- Verify session is not being recreated between calls
- Check session implementation supports the required persistence

### 3. Guardrail Not Triggering
**Problem**: Invalid inputs are not blocked by guardrails
**Solution**:
- Verify the guardrail function returns proper GuardrailFunctionOutput
- Check that tripwire_triggered is set to True for invalid inputs
- Ensure guardrail is properly attached to the agent

### 4. Handoff Not Working
**Problem**: Agent doesn't hand off to another agent
**Solution**:
- Confirm handoff agents are properly defined in the handoffs list
- Verify the main agent's instructions include when to hand off
- Check that handoff_description is clear for the routing agent

## Performance Optimization

### 1. Minimize Context Length
```python
# Good: Limit history length in session
session = SQLiteSession(
    session_id="session_123",
    db_path="db.sqlite",
    max_history_length=20  # Limit conversation length
)

# Avoid: Unlimited history that grows indefinitely
```

### 2. Efficient Tool Design
```python
# Good: Use structured output for predictable data
from pydantic import BaseModel

class SearchResults(BaseModel):
    results: list[str]
    query: str
    num_results: int

@function_tool
def search(query: str) -> SearchResults:
    # Implementation
    pass
```

### 3. Proper Async Handling
```python
# Good: Use asyncio.gather for concurrent operations
async def process_multiple_inputs(inputs):
    tasks = [Runner.run(agent, inp) for inp in inputs]
    results = await asyncio.gather(*tasks)
    return results

# Avoid: Sequential processing when concurrency is possible
```

## Best Practices

### 1. Agent Design
- Give each agent a clear, specific role
- Write precise instructions that match the agent's capabilities
- Use distinct names that reflect the agent's function
- Define appropriate tools for the agent's responsibilities

### 2. Tool Design
- Use type hints for all parameters and return values
- Provide clear, concise descriptions for parameters
- Return structured data using Pydantic models when possible
- Handle errors gracefully within tools

### 3. Error Handling
```python
from agents.exceptions import InputGuardrailTripwireTriggered

async def safe_execution():
    try:
        result = await Runner.run(agent, input_data, session=session)
        return result.final_output
    except InputGuardrailTripwireTriggered as e:
        return f"Request was blocked: {str(e)}"
    except Exception as e:
        return f"An error occurred: {str(e)}"
```

### 4. Testing Strategy
```python
# Example test for multi-agent workflow
import pytest

@pytest.mark.asyncio
async def test_agent_handoff():
    # Setup agents
    agent_a = Agent(name="A", instructions="Hand off to B", handoffs=[agent_b])
    agent_b = Agent(name="B", instructions="Respond with 'received'")

    # Execute and verify handoff
    result = await Runner.run(agent_a, "trigger handoff")
    assert "received" in result.final_output
```

## Security Considerations

### 1. Input Validation
Always use guardrails for user-provided inputs that will be used in system operations:

```python
@function_tool
def execute_command(command: str) -> str:
    # Dangerous - don't allow arbitrary command execution
    pass

# Better: Whitelist allowed commands
ALLOWED_COMMANDS = ["status", "health", "version"]

@function_tool
def execute_allowed_command(cmd: str) -> str:
    if cmd not in ALLOWED_COMMANDS:
        raise ValueError(f"Command '{cmd}' not allowed")
    # Execute the command safely
    pass
```

### 2. Data Access Controls
When building tools that access data:

```python
@function_tool
def get_user_data(ctx: RunContextWrapper, user_id: str) -> dict:
    # Verify the requesting user has access to this data
    current_user = ctx.get_current_user()
    if current_user.id != user_id and not current_user.is_admin:
        raise PermissionError("Access denied")
    # Return user data
    pass
```

## Debugging and Tracing

### Using Built-in Tracing
Enable tracing to visualize agent flows:

```python
import os
os.environ["AGENTS_TRACE_ENABLED"] = "1"  # Enable tracing

# The SDK will provide visualization of agent interactions
```

### Inspecting Results
Access detailed information from Runner results:

```python
result = await Runner.run(agent, input_data)

# Access individual conversation items
for item in result.new_items:
    print(f"{item.role}: {item.content}")

# Access final output
print(result.final_output)

# Access intermediate steps
for step in result.steps:
    print(f"Step: {step.type}, Status: {step.status}")
```