# OpenAI Agents SDK - Use Cases and Applications

## Customer Support System

A multi-agent system for handling customer inquiries:

```python
from agents import Agent, Runner, function_tool
import asyncio

# Tools for customer support
@function_tool
def lookup_order(order_id: str) -> dict:
    """Look up order information by order ID."""
    # In practice, this would query a database
    return {"order_id": order_id, "status": "shipped", "estimated_delivery": "2024-01-15"}

@function_tool
def escalate_issue(issue: str) -> str:
    """Escalate an issue to a human agent."""
    # Logic to escalate to human support
    return f"Issue escalated: {issue}"

# Customer support agents
billing_agent = Agent(
    name="Billing Support",
    instructions="Handle billing-related questions and issues.",
    tools=[lookup_order]
)

technical_agent = Agent(
    name="Technical Support",
    instructions="Handle technical questions and troubleshoot issues.",
    tools=[escalate_issue]
)

customer_service_agent = Agent(
    name="Customer Service",
    instructions="Greet customers and route their inquiries to the appropriate specialist.",
    handoffs=[billing_agent, technical_agent]
)
```

## Research Assistant System

A system for conducting research and compiling reports:

```python
from agents import Agent, Runner, function_tool
from pydantic import BaseModel
import asyncio

class ResearchResult(BaseModel):
    topic: str
    findings: list[str]
    sources: list[str]
    conclusion: str

@function_tool
def search_web(query: str) -> list[dict]:
    """Search the web for information on a topic."""
    # In practice, this would call a search API
    return [{"title": "Sample Result", "url": "http://example.com", "summary": "Sample summary"}]

@function_tool
def analyze_data(data: list[dict]) -> dict:
    """Analyze provided data and extract insights."""
    # Analysis logic here
    return {"trends": ["trend1", "trend2"], "anomalies": []}

researcher_agent = Agent(
    name="Researcher",
    instructions="Find information on the requested topic using web search and analyze the results.",
    tools=[search_web, analyze_data]
)

writer_agent = Agent(
    name="Writer",
    instructions="Create a comprehensive report based on research findings."
)

research_supervisor = Agent(
    name="Research Supervisor",
    instructions="Coordinate between researcher and writer to produce a research report.",
    handoffs=[researcher_agent, writer_agent]
)
```

## Educational Tutor System

A multi-subject tutoring system with specialized agents:

```python
from agents import Agent, Runner, InputGuardrail, GuardrailFunctionOutput
from pydantic import BaseModel
import asyncio

class SubjectCheck(BaseModel):
    subject: str
    is_academic: bool
    confidence: float

# Subject-specific tutors
math_tutor = Agent(
    name="Math Tutor",
    instructions="Help students with math problems. Show step-by-step solutions.",
    handoff_description="Specialist for mathematics questions"
)

science_tutor = Agent(
    name="Science Tutor",
    instructions="Explain science concepts and help with science problems.",
    handoff_description="Specialist for science questions"
)

english_tutor = Agent(
    name="English Tutor",
    instructions="Help with grammar, writing, and literature analysis.",
    handoff_description="Specialist for English/writing questions"
)

# Academic guardrail
subject_check_agent = Agent(
    name="Subject Checker",
    instructions="Determine if the query is related to academic subjects.",
    output_type=SubjectCheck
)

async def academic_guardrail(ctx, agent, input_data):
    result = await Runner.run(subject_check_agent, input_data, context=ctx.context)
    final_output = result.final_output_as(SubjectCheck)

    return GuardrailFunctionOutput(
        output_info=final_output,
        tripwire_triggered=not final_output.is_academic,
    )

triage_agent = Agent(
    name="Academic Triage",
    instructions="Determine which subject tutor the student needs help from.",
    handoffs=[math_tutor, science_tutor, english_tutor],
    input_guardrails=[
        InputGuardrail(guardrail_function=academic_guardrail)
    ]
)
```

## Business Process Automation

An agent system for automating business processes:

```python
from agents import Agent, Runner, function_tool, SQLiteSession
from pydantic import BaseModel
import asyncio

class ApprovalResult(BaseModel):
    approved: bool
    reason: str
    approver: str

@function_tool
def check_budget(division: str, amount: float) -> bool:
    """Check if requested amount is within budget for division."""
    # Budget checking logic
    return amount < 10000  # Simplified

@function_tool
def send_approval_request(manager_email: str, details: str) -> str:
    """Send approval request to manager."""
    # Email sending logic
    return f"Approval request sent to {manager_email}"

@function_tool
def record_decision(approval_id: str, approved: bool, reason: str) -> str:
    """Record approval decision in system."""
    # Database recording logic
    return f"Decision recorded: {approval_id}"

request_handler = Agent(
    name="Request Handler",
    instructions="Process business requests and determine if they need approval.",
    tools=[check_budget, send_approval_request, record_decision]
)

approval_workflow = Agent(
    name="Approval Workflow",
    instructions="Manage the business approval workflow.",
    tools=[check_budget, send_approval_request, record_decision]
)
```

## Content Creation Pipeline

A system for creating, reviewing, and publishing content:

```python
from agents import Agent, Runner, function_tool
import asyncio

@function_tool
def fact_check(content: str) -> dict:
    """Check facts in the content."""
    # Fact-checking logic
    return {"accuracy_score": 0.95, "issues": []}

@function_tool
def check_tone(content: str) -> str:
    """Analyze the tone of the content."""
    # Tone analysis logic
    return "professional"

@function_tool
def publish_content(content: str, platform: str) -> str:
    """Publish content to specified platform."""
    # Publishing logic
    return f"Published to {platform}"

draft_writer = Agent(
    name="Draft Writer",
    instructions="Create initial drafts based on user requirements."
)

editor_agent = Agent(
    name="Editor",
    instructions="Review drafts for accuracy, tone, and quality.",
    tools=[fact_check, check_tone]
)

publisher_agent = Agent(
    name="Publisher",
    instructions="Publish approved content to the appropriate platforms.",
    tools=[publish_content]
)

content_manager = Agent(
    name="Content Manager",
    instructions="Manage the content creation pipeline from draft to publication.",
    handoffs=[draft_writer, editor_agent, publisher_agent]
)
```

## Key Design Principles for Use Cases

1. **Modularity**: Design agents to have focused responsibilities
2. **Composability**: Create agents that can work together in different combinations
3. **State Management**: Use sessions for maintaining context across interactions
4. **Safety**: Implement guardrails for validating inputs and outputs
5. **Observability**: Use tracing to monitor and debug agent interactions
6. **Scalability**: Design with session management and tool efficiency in mind