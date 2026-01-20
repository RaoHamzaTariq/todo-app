# Quickstart Guide: AI Chatbot

## Prerequisites

- Python 3.13+
- Node.js 18+ / npm 8+
- Neon PostgreSQL account
- OpenAI API key
- uv package manager (for Python dependencies)

## Environment Setup

1. **Clone the repository**
   ```bash
   git clone <repo-url>
   cd todo-app
   ```

2. **Install Python dependencies**
   ```bash
   uv sync  # or use pip install -r requirements.txt
   ```

3. **Install Node.js dependencies**
   ```bash
   cd frontend
   npm install
   ```

4. **Configure environment variables**

   Create `.env` files in both backend and frontend:

   **Backend (.env)**:
   ```
   DATABASE_URL="postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname?sslmode=require"
   OPENAI_API_KEY="sk-..."
   BETTER_AUTH_SECRET="your-secret-key"
   ```

   **Frontend (.env.local)**:
   ```
   NEXT_PUBLIC_BETTER_AUTH_URL="http://localhost:8000"
   ```

## Database Setup

1. **Run migrations**
   ```bash
   cd backend
   python -m alembic upgrade head
   ```

2. **Verify database connection**
   ```bash
   python -c "from backend.db import engine; print('DB connected')"
   ```

## Running the Application

1. **Start the MCP server**
   ```bash
   cd backend
   python -m mcp.server
   ```

2. **Start the backend API**
   ```bash
   cd backend
   uvicorn main:app --reload --port 8000
   ```

3. **Start the frontend**
   ```bash
   cd frontend
   npm run dev
   ```

## Testing the Chatbot

1. **Access the chat interface**
   - Navigate to `http://localhost:3000/chat`
   - Log in with your credentials

2. **Try sample commands**
   ```
   - "Add a task to buy groceries"
   - "Add a high priority task to call doctor tomorrow"
   - "Star the project deadline task"
   - "What are my tasks?"
   - "What are my starred tasks?"
   - "Mark task 1 as complete"
   - "Delete the meeting task"
   - "Update task 2 to 'Call doctor tomorrow'"
   - "Set task 3 priority to high"
   ```

## Development Workflow

1. **Making changes to MCP tools**
   - Modify files in `backend/mcp/tools.py`
   - Restart MCP server to see changes

2. **Updating the chat agent**
   - Modify files in `backend/chat/agent.py`
   - Restart backend to see changes

3. **Updating the UI**
   - Modify files in `frontend/components/chat/`
   - Changes hot-reload automatically

## Running Tests

1. **Backend tests**
   ```bash
   cd backend
   pytest tests/backend/
   ```

2. **Frontend tests**
   ```bash
   cd frontend
   npm test
   ```

## API Endpoints

- `POST /api/{user_id}/chat` - Main chat endpoint
- `GET /api/{user_id}/chat/{conversation_id}` - Get conversation history
- MCP server runs on port 8080 by default

## Troubleshooting

1. **Database connection issues**
   - Verify DATABASE_URL is correct
   - Check Neon PostgreSQL connection settings

2. **MCP tools not responding**
   - Ensure MCP server is running
   - Check that the agent can connect to MCP tools

3. **Authentication issues**
   - Verify BETTER_AUTH_SECRET matches between frontend and backend
   - Check JWT token validity

4. **Chat not responding**
   - Verify OpenAI API key is valid
   - Check that agent is properly configured