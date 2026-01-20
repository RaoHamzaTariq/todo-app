# MASTER SPEC & EXECUTION GUIDE

**Todo AI Chatbot – Custom UI, MCP, OpenAI Agents SDK**
*(Spec-Driven | Stateless | Hackathon II Compliant)*

---

## 0. ROLE & EXECUTION CONSTRAINTS (VERY IMPORTANT)

**You are an autonomous coding agent.**

### HARD RULES

* Follow **Spec-Driven Development**
* Workflow:
  **Write spec → Generate plan → Break into tasks → Implement**
* ❌ No manual coding shortcuts
* ❌ No client-side AI logic
* ❌ No server-side session state
* ✅ All state persisted in database
* ✅ All task mutations via MCP tools only

---

## 1. PROJECT GOAL

Convert an existing **Todo web application** into an **AI-powered chatbot** that allows users to manage todos via **natural language**, using:

* **Custom chatbot UI (Next.js, Tailwind, TypeScript)**
* **FastAPI backend**
* **OpenAI Agents SDK**
* **Official MCP SDK**
* **Neon Serverless PostgreSQL**
* **Stateless architecture**

---

## 2. FINAL ARCHITECTURE (MANDATORY)

```
Frontend (Next.js Chat UI)
        │
        ▼
POST /api/{user_id}/chat   ← Stateless
        │
        ▼
FastAPI Chat Controller
        │
        ├── Load conversation history from DB
        ├── Store user message
        ├── Run OpenAI Agent
        │        └── Calls MCP tools
        │                 └── DB operations
        ├── Store assistant message
        ▼
Return AI response + tool calls
```

---

## 3. TECHNOLOGY STACK (FIXED)

| Component    | Technology                        |
| ------------ | --------------------------------- |
| Frontend     | Next.js, TypeScript, Tailwind CSS |
| Backend      | FastAPI                           |
| AI Framework | OpenAI Agents SDK                 |
| MCP Server   | Official MCP SDK                  |
| ORM          | SQLModel                          |
| Database     | Neon Serverless PostgreSQL        |
| Auth         | Better Auth                       |

---

## 4. DATABASE MODELS (REQUIRED)

### Task

```text
id
user_id
title
description
completed
priority (low | medium | high, default: medium)
is_starred (boolean, default: false)
created_at
updated_at
```

### Conversation

```text
id
user_id
created_at
updated_at
```

### Message

```text
id
conversation_id
user_id
role (user | assistant)
content
created_at
```

**IMPORTANT**

* Server stores NO memory
* Conversation context rebuilt every request

---

## 5. MCP SERVER SPECIFICATION

### MCP Purpose

Expose **task operations as tools** for the AI agent.

### MCP TOOLS (MANDATORY)

#### add_task

```json
{
  "user_id": "string",
  "title": "string",
  "description": "string?",
  "priority": "low | medium | high?",
  "is_starred": "boolean?"
}
```

Returns:

```json
{
  "task_id": 1,
  "status": "created",
  "title": "Buy groceries"
}
```

---

#### list_tasks

```json
{
  "user_id": "string",
  "status": "all | pending | completed | starred"
}
```

---

#### complete_task

```json
{
  "user_id": "string",
  "task_id": 3
}
```

---

#### delete_task

```json
{
  "user_id": "string",
  "task_id": 2
}
```

---

#### update_task

```json
{
  "user_id": "string",
  "task_id": 1,
  "title": "string?",
  "description": "string?",
  "priority": "low | medium | high?",
  "is_starred": "boolean?",
  "completed": "boolean?"
}
```

---

### MCP RULES

* ❌ MCP tools must NOT store session state
* ❌ MCP tools must NOT call OpenAI
* ✅ MCP tools may access database
* ✅ MCP tools validate `user_id`

---

## 6. AI AGENT SPECIFICATION

### SYSTEM PROMPT

```text
You are a Todo Management AI Assistant.

Rules:
- You must use MCP tools to manage tasks
- Never modify tasks directly
- Always confirm actions in natural language
- Handle errors gracefully
- Ask for clarification when ambiguous

Behavior Mapping:
- add / remember / create → add_task
- list / show / see / starred → list_tasks
- done / complete → complete_task
- delete / remove → delete_task
- update / change / rename → update_task
- priority / high / low / medium → update_task
- star / unstar → update_task
```

---

### AGENT RULES

* MCP tools are the **only interface to tasks**
* Agent may chain multiple tools in one turn
* Agent output must be user-friendly

---

## 7. CHAT API (STATELESS)

### Endpoint

```
POST /api/{user_id}/chat
```

### Request

```json
{
  "conversation_id": 12,
  "message": "Add a task to buy groceries"
}
```

### Response

```json
{
  "conversation_id": 12,
  "response": "✅ I've added 'Buy groceries' to your tasks.",
  "tool_calls": [
    {
      "tool": "add_task",
      "task_id": 5
    }
  ]
}
```

---

## 8. CHAT REQUEST FLOW (STRICT ORDER)

1. Receive request
2. Fetch conversation history from DB
3. Append user message
4. Save user message to DB
5. Run agent with full history
6. Agent invokes MCP tool(s)
7. Save assistant message
8. Return response
9. Discard all runtime state

---

## 9. FRONTEND – CUSTOM CHAT UI

### Frontend Responsibilities

* Render chat messages
* Send user input
* Persist `conversation_id`
* Show loading indicator

### Frontend MUST NOT

* Interpret commands
* Call MCP tools
* Store AI logic

---

### Chat UI Components

```
ChatPage
 ├─ MessageList
 │   ├─ UserBubble
 │   └─ AssistantBubble
 ├─ TypingIndicator
 └─ ChatInput
```

---

### Frontend Chat Logic (Concept)

```text
1. User types message
2. POST to /api/{user_id}/chat
3. Append user message to UI
4. Append assistant response
5. Save conversation_id
```

---

## 10. AUTHENTICATION

* User must be authenticated
* `user_id` injected server-side
* MCP tools validate ownership

---

## 11. REQUIRED REPOSITORY STRUCTURE

```
/frontend
  /app/chat/page.tsx
  /components/*
  /hooks/useChat.ts

/backend
  /chat/router.py
  /chat/agent.py
  /mcp/server.py
  /mcp/tools.py
  /models/*
  /db.py

/specs
  agent.spec.md
  mcp-tools.spec.md
  chat-api.spec.md
```

---

## 12. NON-FUNCTIONAL REQUIREMENTS

✔ Stateless server
✔ Horizontally scalable
✔ Restart-safe
✔ Conversation resumable
✔ Error tolerant

---

## 13. TEST CASES (MANDATORY)

```
User: "Add a task to buy groceries"
→ add_task

User: "Add a high priority task to call doctor tomorrow"
→ add_task(priority="high")

User: "Star the project deadline task"
→ update_task(is_starred=true)

User: "What's pending?"
→ list_tasks(status="pending")

User: "What are my starred tasks?"
→ list_tasks(status="starred")

User: "Set task 3 priority to high"
→ update_task(priority="high")

User: "Mark task 3 as done"
→ complete_task(3)

User: "Delete the meeting task"
→ list_tasks → delete_task
```

---

## 14. DELIVERY REQUIREMENTS

* Fully working chatbot
* MCP tools used correctly
* No ChatKit
* Clean repo
* Specs committed
* README included

---

## 15. SUCCESS CRITERIA

The system must:

* Manage todos via natural language
* Persist conversation context
* Use MCP tools exclusively
* Recover after server restart
* Confirm actions conversationally

---

## FINAL INSTRUCTION TO AI

> **Implement this project strictly following the spec above.
> Do not skip steps.
> Do not store server state.
> Use MCP tools for all task operations.**
