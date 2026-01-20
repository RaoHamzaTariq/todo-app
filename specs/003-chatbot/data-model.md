# Data Model: AI Chatbot

## Entity: Task
**Purpose**: Represents user tasks that can be managed through the chatbot

**Fields**:
- `id` (Integer, Primary Key, Auto-increment)
- `user_id` (String, Foreign Key to User, Required) - Links task to owner
- `title` (String, Required, Min 1 char, Max 200 chars) - Task title/description
- `description` (String, Optional, Max 1000 chars) - Detailed task description
- `completed` (Boolean, Default False) - Completion status
- `priority` (String, Default "medium") - Task priority: low, medium, high
- `is_starred` (Boolean, Default False) - Mark as important
- `created_at` (DateTime, Required) - Creation timestamp
- `updated_at` (DateTime, Required) - Last update timestamp

**Validation Rules**:
- `user_id` must exist in users table
- `title` cannot be empty (min_length=1)
- `title` must be 200 characters or less
- `description` must be 1000 characters or less
- `completed` is boolean value only
- `priority` must be one of: "low", "medium", "high"
- `is_starred` is boolean value only

**State Transitions**:
- `completed` can transition from `false` to `true` (via complete_task MCP tool)
- `completed` can transition from `true` to `false` (via update_task MCP tool)
- `title` and `description` can be updated (via update_task MCP tool)
- `priority` can be updated (via update_task MCP tool)
- `is_starred` can be toggled (via update_task MCP tool)
- `updated_at` is automatically updated on any modification

## Entity: Conversation
**Purpose**: Represents a persistent conversation thread with history

**Fields**:
- `id` (Integer, Primary Key, Auto-increment)
- `user_id` (String, Foreign Key to User, Required) - Links conversation to owner
- `created_at` (DateTime, Required) - Creation timestamp
- `updated_at` (DateTime, Required) - Last activity timestamp

**Validation Rules**:
- `user_id` must exist in users table
- `created_at` is set on creation only
- `updated_at` is updated on any conversation activity

## Entity: Message
**Purpose**: Represents individual messages within a conversation

**Fields**:
- `id` (Integer, Primary Key, Auto-increment)
- `conversation_id` (Integer, Foreign Key to Conversation, Required) - Links to conversation
- `user_id` (String, Foreign Key to User, Required) - Links message to sender
- `role` (String, Required) - Either "user" or "assistant"
- `content` (String, Required, Max 5000 chars) - Message content
- `created_at` (DateTime, Required) - Creation timestamp

**Validation Rules**:
- `conversation_id` must exist in conversations table
- `user_id` must exist in users table
- `role` must be either "user" or "assistant"
- `content` cannot be empty
- `content` must be less than 5001 characters

**Relationships**:
- One Conversation to Many Messages (One-to-Many)
- One User to Many Conversations (One-to-Many)
- One User to Many Messages (One-to-Many)

## Constraints & Indexes

**Indexes**:
- `idx_tasks_user_id` on Task(user_id) - For efficient user task queries
- `idx_tasks_completed` on Task(completed) - For efficient status queries
- `idx_conversations_user_id` on Conversation(user_id) - For efficient user conversation queries
- `idx_messages_conversation_id` on Message(conversation_id) - For efficient conversation history retrieval
- `idx_messages_created_at` on Message(created_at) - For chronological ordering

**Foreign Key Constraints**:
- Task.user_id references User.id (CASCADE DELETE)
- Conversation.user_id references User.id (CASCADE DELETE)
- Message.conversation_id references Conversation.id (CASCADE DELETE)
- Message.user_id references User.id (CASCADE DELETE)

## Data Integrity Rules

1. **Ownership Validation**: All operations must validate that user_id matches the resource owner
2. **Timestamp Management**: created_at is set once on creation, updated_at is updated on any modification
3. **Referential Integrity**: All foreign key relationships are enforced at database level
4. **Soft Deletes**: Consider soft deletes for audit trail (using deleted_at field) if required for compliance