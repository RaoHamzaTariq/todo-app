# Quickstart Guide: Phase 2 Full-Stack Todo Application

**Date**: 2026-01-04
**Phase**: 1 (Design & Contracts)
**Plan Reference**: [plan.md](./plan.md)

## Overview

This guide provides step-by-step instructions to set up and run the Phase 2 full-stack todo application locally.

**Architecture**:
- **Frontend**: Next.js 16+ (port 3000)
- **Backend**: FastAPI (port 8000)
- **Database**: Neon Serverless PostgreSQL

---

## Prerequisites

### Required Software

| Software | Version | Installation |
|----------|---------|--------------|
| Node.js | 18.x or 20.x | https://nodejs.org/ |
| Python | 3.13+ | https://python.org/ |
| uv (Python package manager) | Latest | `pip install uv` |
| Git | Latest | https://git-scm.com/ |

### Required Accounts

- **Neon PostgreSQL**: Create account at https://neon.tech/
  - Create a new project
  - Note the connection string

---

## Setup Instructions

### 1. Clone Repository

```bash
git clone <repository-url>
cd todo-app
git checkout 002-phase2-fullstack
```

### 2. Backend Setup

#### 2.1 Navigate to Backend Directory

```bash
cd backend
```

#### 2.2 Install Dependencies

**Option A: Using uv (recommended)**
```bash
uv sync
```

**Option B: Using pip**
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

#### 2.3 Configure Environment Variables

Create `.env` file in `backend/` directory:

```env
# Database
DATABASE_URL=postgresql+psycopg://username:password@ep-xyz-123456.us-east-1.neon.tech/todo_db?sslmode=require

# Authentication (must match frontend secret)
BETTER_AUTH_SECRET=your-256-bit-secret-key-here

# JWT Configuration
JWT_ALGORITHM=HS256

# Environment
ENVIRONMENT=development
```

**Generate BETTER_AUTH_SECRET**:
```bash
# On Linux/Mac
openssl rand -hex 32

# On Windows (PowerShell)
[Convert]::ToBase64String((1..32 | ForEach-Object { Get-Random -Minimum 0 -Maximum 256 }))
```

#### 2.4 Initialize Database

```bash
# Run database initialization
python -m src.main

# Or using uvicorn directly
uvicorn src.main:app --reload --port 8000
```

The database tables will be created automatically on first startup.

#### 2.5 Verify Backend

```bash
# Backend should be running on http://localhost:8000
curl http://localhost:8000/docs

# You should see the FastAPI Swagger UI
```

---

### 3. Frontend Setup

#### 3.1 Navigate to Frontend Directory

```bash
cd ../frontend  # From repo root: cd frontend
```

#### 3.2 Install Dependencies

```bash
npm install
```

#### 3.3 Configure Environment Variables

Create `.env.local` file in `frontend/` directory:

```env
# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000

# Authentication (must match backend secret)
BETTER_AUTH_SECRET=your-256-bit-secret-key-here

# Database (same as backend for Better Auth)
DATABASE_URL=postgresql+psycopg://username:password@ep-xyz-123456.us-east-1.neon.tech/todo_db?sslmode=require
```

**Important**: Use the **same** `BETTER_AUTH_SECRET` in both frontend and backend.

#### 3.4 Start Frontend Development Server

```bash
npm run dev
```

Frontend should be running on http://localhost:3000

#### 3.5 Verify Frontend

Open browser and navigate to: http://localhost:3000

You should see the todo application landing page.

---

## Running the Application

### Start Both Services

**Terminal 1 - Backend**:
```bash
cd backend
uvicorn src.main:app --reload --port 8000
```

**Terminal 2 - Frontend**:
```bash
cd frontend
npm run dev
```

### Using Docker Compose (Alternative)

```bash
# From repository root
docker-compose up
```

This starts both frontend and backend services.

---

## Testing the Application

### 1. Sign Up

1. Navigate to http://localhost:3000/sign-up
2. Enter email and password (min 8 characters)
3. Click "Sign Up"
4. You should be redirected to the dashboard

### 2. Create a Task

1. After signing in, you'll see the task list page
2. Click "Add Task" button
3. Enter task title (required) and description (optional)
4. Click "Create"
5. Task should appear in your list

### 3. Manage Tasks

- **View Tasks**: All your tasks displayed on dashboard
- **Edit Task**: Click task → Edit → Update title/description
- **Complete Task**: Click checkbox to toggle completion
- **Delete Task**: Click task → Delete → Confirm

### 4. Sign Out

1. Click user menu in header
2. Click "Sign Out"
3. You should be redirected to sign-in page

---

## API Testing

### Using curl

```bash
# 1. Sign up (creates user)
curl -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'

# 2. Sign in (get JWT token)
TOKEN=$(curl -X POST http://localhost:8000/api/auth/signin \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}' \
  | jq -r '.token')

# 3. Create task
curl -X POST http://localhost:8000/api/USER_ID/tasks \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"Test task","description":"Description"}'

# 4. List tasks
curl -X GET http://localhost:8000/api/USER_ID/tasks \
  -H "Authorization: Bearer $TOKEN"
```

**Note**: Replace `USER_ID` with the actual user ID from sign-in response.

### Using Swagger UI

1. Navigate to http://localhost:8000/docs
2. Click "Authorize" button
3. Enter Bearer token: `Bearer <JWT_TOKEN>`
4. Try endpoints interactively

---

## Troubleshooting

### Backend Issues

**Error: "DATABASE_URL environment variable not set"**
- Solution: Ensure `.env` file exists in `backend/` with valid `DATABASE_URL`

**Error: "BETTER_AUTH_SECRET environment variable not set"**
- Solution: Add `BETTER_AUTH_SECRET` to both `backend/.env` and `frontend/.env.local`

**Error: "Connection to database failed"**
- Solution: Verify Neon PostgreSQL connection string is correct
- Check Neon project is active and accessible

**Error: "Port 8000 already in use"**
- Solution: Kill process on port 8000 or use different port: `uvicorn src.main:app --reload --port 8001`

### Frontend Issues

**Error: "NEXT_PUBLIC_API_URL is not defined"**
- Solution: Create `frontend/.env.local` with `NEXT_PUBLIC_API_URL=http://localhost:8000`

**Error: "Failed to fetch from API"**
- Solution: Ensure backend is running on port 8000
- Check browser console for CORS errors

**Error: "Invalid token" or "401 Unauthorized"**
- Solution: Ensure `BETTER_AUTH_SECRET` matches in frontend and backend
- Try signing out and signing in again

**Error: "Port 3000 already in use"**
- Solution: Kill process on port 3000 or use different port: `npm run dev -- -p 3001`

### Database Issues

**Error: "Table does not exist"**
- Solution: Restart backend server to trigger table creation
- Or manually run: `python -c "from src.app.database import init_db; init_db()"`

**Error: "Foreign key constraint violation"**
- Solution: Ensure users table exists (created by Better Auth)
- Check Better Auth is properly configured in frontend

---

## Development Workflow

### 1. Feature Development

```bash
# Create feature branch
git checkout -b feature/my-feature

# Make changes
# ...

# Commit with SDD reference
git commit -m "feat: implement feature X

# SDD: Implements Task ID: T-XXX"
```

### 2. Running Tests

**Backend Tests**:
```bash
cd backend
pytest tests/
```

**Frontend Tests**:
```bash
cd frontend
npm test
```

### 3. Code Quality

**Backend Linting**:
```bash
cd backend
ruff check .
mypy src/
```

**Frontend Linting**:
```bash
cd frontend
npm run lint
```

---

## Next Steps

After setup is complete:

1. **Explore the API**: Use Swagger UI to test all endpoints
2. **Review Data Model**: See `data-model.md` for entity details
3. **Check API Contracts**: See `contracts/openapi.yaml` for full API spec
4. **Run Tests**: Execute test suites for both frontend and backend
5. **Start Implementation**: Follow tasks from `tasks.md` (generated by `/sp.tasks`)

---

## Configuration Reference

### Backend Environment Variables

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| DATABASE_URL | Yes | Neon PostgreSQL connection string | `postgresql+psycopg://...` |
| BETTER_AUTH_SECRET | Yes | JWT signing secret (256-bit) | `abc123...` |
| JWT_ALGORITHM | No | JWT algorithm (default: HS256) | `HS256` |
| ENVIRONMENT | No | Environment name (default: development) | `development` |

### Frontend Environment Variables

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| NEXT_PUBLIC_API_URL | Yes | Backend API base URL | `http://localhost:8000` |
| BETTER_AUTH_SECRET | Yes | JWT signing secret (must match backend) | `abc123...` |
| DATABASE_URL | Yes | PostgreSQL connection (for Better Auth) | `postgresql+psycopg://...` |

---

## Additional Resources

- **API Documentation**: http://localhost:8000/docs (Swagger UI)
- **ReDoc**: http://localhost:8000/redoc (Alternative API docs)
- **Plan Document**: [plan.md](./plan.md)
- **Data Model**: [data-model.md](./data-model.md)
- **Research Findings**: [research.md](./research.md)
- **OpenAPI Spec**: [contracts/openapi.yaml](./contracts/openapi.yaml)

---

**Setup Status**: Ready for implementation (pending `/sp.tasks` generation)
