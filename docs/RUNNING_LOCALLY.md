# Running the Todo Chatbot Application Locally

## Prerequisites

1. **Install Docker and Docker Compose**
2. **Install Python 3.13+**
3. **Install Node.js 18+**
4. **Install uv** (the Python package manager used in this project)

## Project Architecture

The Todo Chatbot application consists of two main components with integrated MCP functionality:
- **Frontend**: Next.js application providing the user interface
- **Backend**: FastAPI application handling business logic, data persistence, and MCP (Model Context Protocol) functionality

The MCP (Model Context Protocol) functionality is integrated directly into the Python backend, eliminating the need for a separate server.

## Step-by-Step Setup

### 1. Clone the repository (if you haven't already)
```bash
git clone <repository-url>
cd todo-app
```

### 2. Install uv (Python package manager)
```bash
# On Windows
winget install uv

# Or using pip
pip install uv
```

### 3. Set up the backend
```bash
cd backend
uv sync
```

### 4. Set up the frontend
```bash
cd ../frontend
npm install
```

### 5. Start the required services using Docker Compose
From the project root directory:
```bash
docker-compose up -d
```

### 6. Start the backend service (includes MCP functionality)
In a new terminal, navigate to the backend directory:
```bash
cd backend
uv run python -m src.main
# Or if using FastAPI directly:
uv run uvicorn src.main:app --reload --port 8000
```

### 7. Start the frontend service
In another terminal, navigate to the frontend directory:
```bash
cd frontend
npm run dev
```

### 8. Start the event services (optional but recommended)
For each event service, open a new terminal and run:

**Reminder Service:**
```bash
cd event-services/reminder-service
# Install dependencies if needed
pip install -r requirements.txt  # or use uv
python src/main.py
```

**Recurring Task Service:**
```bash
cd event-services/recurring-task-service
# Install dependencies if needed
pip install -r requirements.txt  # or use uv
python src/main.py
```

**Audit Log Service:**
```bash
cd event-services/audit-log-service
# Install dependencies if needed
pip install -r requirements.txt  # or use uv
python src/main.py
```

**Notification Service:**
```bash
cd event-services/notification-service
# Install dependencies if needed
pip install -r requirements.txt  # or use uv
python src/main.py
```

### 9. Access the application
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Backend API docs: http://localhost:8000/docs
- MCP functionality: Integrated within the backend service

## Alternative: Using the Scripts

There might be a startup script in the project. Check for:
```bash
# Look for any startup scripts
ls -la *.sh
# Or check if there's a complete startup script
./complete_phase1.sh  # This might exist based on the file structure
```

## Configuration

### Environment Variables

The application uses several environment variables for configuration:

#### Backend Service
- `DATABASE_URL`: Connection string for PostgreSQL database
- `DAPR_HTTP_ENDPOINT`: Dapr sidecar endpoint (usually `http://localhost:3500`)
- `KAFKA_BROKER`: Kafka broker address
- `ENVIRONMENT`: Current environment (development, staging, production)

#### Frontend Service
- `NEXT_PUBLIC_API_URL`: URL for the backend API (usually `http://localhost:8000`)

## Detailed Usage Instructions

### 1. Starting the Application
1. Ensure Docker is running
2. Start all services in the correct order:
   - Backend (includes MCP functionality)
   - Frontend
   - Event services (optional)

### 2. Using the Application
1. Access the frontend at http://localhost:3000
2. Create an account or log in
3. Start creating tasks with various features:
   - Regular tasks
   - Recurring tasks
   - Tasks with due dates and reminders
   - Tasks with priorities and tags

### 3. AI Agent Integration
1. The MCP tools are integrated directly into the backend
2. AI agents can connect to the backend to perform task operations
3. All MCP functionality is available through the same backend service

### 4. Development Mode
- Use `--reload` flag for backend to enable hot reloading
- Use `npm run dev` for frontend to enable hot reloading
- The application will automatically reload when code changes are detected

### 5. Debugging
- Check logs in each terminal where services are running
- Use browser developer tools for frontend issues
- Check Docker container logs with `docker logs <container-name>`

## Troubleshooting Tips

1. **Database Connection Issues**: Make sure PostgreSQL is running in Docker
2. **Kafka Connection Issues**: Verify Kafka and Zookeeper are running in Docker
3. **Backend Startup Issues**: Ensure Python 3.13+ and all dependencies are properly installed
4. **Dapr Issues**: If using Dapr locally, make sure it's initialized:
   ```bash
   dapr init
   ```

5. **Environment Variables**: Check if there are any `.env` files that need to be configured
6. **Port Conflicts**: Make sure ports 3000 (frontend) and 8000 (backend) are available
7. **Dependency Issues**: Ensure all dependencies are properly installed for each service

## Quick Start Command (if available)

Look for a `package.json` file in the root or frontend directory that might have a start script:
```bash
npm start
# or
npm run start:dev
```

Or check for a unified startup script:
```bash
./start-all.sh  # or similar
```

The application should now be running locally with all services connected. You can access the frontend at http://localhost:3000 and start using the Todo Chatbot application.