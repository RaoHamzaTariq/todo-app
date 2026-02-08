# Running the Todo Chatbot Application Locally

## Prerequisites

1. **Install Docker and Docker Compose**
2. **Install Python 3.13+**
3. **Install Node.js 18+**
4. **Install uv** (the Python package manager used in this project)
5. **Install Dapr** (Distributed Application Runtime)

## Project Architecture

The Todo Chatbot application consists of two main components with integrated MCP functionality:
- **Frontend**: Next.js application providing the user interface
- **Backend**: FastAPI application handling business logic, data persistence, and MCP (Model Context Protocol) functionality
- **Event Services**: Python services for reminders, recurring tasks, audit logs, and notifications
- **MCP Server**: Integrated within the backend for AI agent integration

The MCP (Model Context Protocol) functionality is integrated directly into the Python backend, eliminating the need for a separate server.

## Step-by-Step Setup

### 1. Clone the repository (if you haven't already)
```bash
git clone <repository-url>
cd todo-app
```

### 2. Install Dapr
```bash
# On Windows
powershell -Command "iwr -useb https://raw.githubusercontent.com/dapr/cli/master/install/install.ps1 | iex"

# Or follow the official installation guide at https://docs.dapr.io/getting-started/install-dapr-cli/
```

### 3. Initialize Dapr runtime
```bash
dapr init
```

### 4. Install uv (Python package manager)
```bash
# On Windows
winget install uv

# Or using pip
pip install uv
```

### 5. Set up the backend
```bash
cd backend
uv sync
```

### 6. Set up the frontend
```bash
cd ../frontend
npm install
```

### 7. Configure Supabase (instead of PostgreSQL)
1. Create a Supabase account at https://supabase.com/
2. Create a new project
3. Get your connection string from Project Settings > Database
4. Set the DATABASE_URL environment variable:
```bash
# In the backend directory
echo DATABASE_URL=your_supabase_connection_string > .env
```

### 8. Start the required services using Docker Compose (for Kafka and other dependencies)
From the project root directory:
```bash
docker-compose up -d kafka zookeeper
```

### 9. Start the backend service with Dapr (includes MCP functionality)
In a new terminal, navigate to the backend directory:
```bash
cd backend
dapr run --app-id backend --app-port 8000 --dapr-http-port 3500 -- uv run uvicorn src.main:app --reload --port 8000
```

### 10. Start the event services with Dapr
For each event service, open a new terminal and run:

**Reminder Service:**
```bash
cd event-services/reminder-service
dapr run --app-id reminder-service --app-port 8002 --dapr-http-port 3502 -- python src/main.py
```

**Recurring Task Service:**
```bash
cd event-services/recurring-task-service
dapr run --app-id recurring-task-service --app-port 8003 --dapr-http-port 3503 -- python src/main.py
```

**Audit Log Service:**
```bash
cd event-services/audit-log-service
dapr run --app-id audit-log-service --app-port 8004 --dapr-http-port 3504 -- python src/main.py
```

**Notification Service:**
```bash
cd event-services/notification-service
dapr run --app-id notification-service --app-port 8005 --dapr-http-port 3505 -- python src/main.py
```

### 11. Start the frontend service
In another terminal, navigate to the frontend directory:
```bash
cd frontend
npm run dev
```

### 12. Access the application
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Backend API docs: http://localhost:8000/docs
- Dapr Dashboard: http://localhost:8080 (if enabled)
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
- `DATABASE_URL`: Connection string for Supabase database (e.g., `postgresql://[user]:[password]@[host]:[port]/[database]`)
- `DAPR_HTTP_ENDPOINT`: Dapr sidecar endpoint (usually `http://localhost:3500`)
- `KAFKA_BROKER`: Kafka broker address (e.g., `localhost:9092`)
- `ENVIRONMENT`: Current environment (development, staging, production)

#### Frontend Service
- `NEXT_PUBLIC_API_URL`: URL for the backend API (usually `http://localhost:8000`)
- `NEXT_PUBLIC_SUPABASE_URL`: Your Supabase project URL
- `NEXT_PUBLIC_SUPABASE_ANON_KEY`: Your Supabase anonymous key

## Detailed Usage Instructions

### 1. Starting the Application
1. Ensure Docker is running
2. Ensure Dapr is initialized (`dapr init`)
3. Start all services in the correct order:
   - Kafka/Zookeeper (via Docker Compose)
   - Backend with Dapr
   - Event services with Dapr
   - Frontend

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

### 4. Dapr Integration
1. Services communicate via Dapr's service invocation
2. State management is handled by Dapr (connected to Supabase)
3. Pub/Sub is implemented via Dapr (using Kafka as the message broker)

### 5. Development Mode
- Use `--reload` flag for backend to enable hot reloading
- Use `npm run dev` for frontend to enable hot reloading
- The application will automatically reload when code changes are detected

### 6. Debugging
- Check logs in each terminal where services are running
- Use browser developer tools for frontend issues
- Check Docker container logs with `docker logs <container-name>`
- Use Dapr CLI to check service status: `dapr status -k`

## Troubleshooting Tips

1. **Database Connection Issues**: Verify your Supabase connection string is correct and accessible
2. **Kafka Connection Issues**: Verify Kafka and Zookeeper are running in Docker
3. **Dapr Issues**: Make sure Dapr is properly initialized:
   ```bash
   dapr init
   dapr status -k  # Check if Dapr is running
   ```
4. **Service Communication**: Verify Dapr sidecars are running and services can communicate
5. **Environment Variables**: Check if there are any `.env` files that need to be configured with Supabase credentials
6. **Port Conflicts**: Make sure ports 3000 (frontend), 8000 (backend), and Dapr ports (3500+) are available
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

The application should now be running locally with all services connected via Dapr and using Supabase as the database. You can access the frontend at http://localhost:3000 and start using the Todo Chatbot application.