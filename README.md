# Todo App - Full Stack Application

A full-stack todo application featuring Next.js frontend with Better Auth authentication and FastAPI backend with PostgreSQL database.

## Features

- User authentication (sign up, sign in, sign out)
- Create, read, update, and delete tasks
- Toggle task completion status
- Task filtering and search
- Responsive design for all device sizes
- Secure user data isolation (each user can only access their own tasks)

## Tech Stack

- **Frontend**: Next.js 16+, React, TypeScript, Tailwind CSS
- **Authentication**: Better Auth
- **Backend**: FastAPI, Python 3.13+
- **Database**: PostgreSQL (Neon Serverless)
- **ORM**: SQLModel
- **Authentication**: JWT

## Prerequisites

- Node.js 18+
- Python 3.13+
- PostgreSQL database (or Neon Serverless account)

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd todo-app
```

### 2. Backend Setup

Navigate to the backend directory and install dependencies:

```bash
cd backend
uv install
```

Create a `.env` file with your database configuration:

```bash
DATABASE_URL=postgresql+psycopg://username:password@host:port/database
BETTER_AUTH_SECRET=your-super-secret-jwt-token-with-at-least-32-characters-long
JWT_ALGORITHM=HS256
ENVIRONMENT=development
```

Start the backend server:

```bash
uv run uvicorn src.main:app --reload --port 8000
```

### 3. Frontend Setup

In a new terminal, navigate to the frontend directory:

```bash
cd frontend
npm install
```

Create a `.env.local` file with the following configuration:

```bash
NEXT_PUBLIC_API_URL=http://localhost:3000
BACKEND_API_URL=http://localhost:8000
BETTER_AUTH_SECRET=your-super-secret-jwt-token-with-at-least-32-characters-long
DATABASE_URL=postgresql+psycopg://username:password@host:port/database
```

Start the frontend development server:

```bash
npm run dev
```

### 4. Access the Application

Open your browser and navigate to `http://localhost:3000`.

## Project Structure

```
todo-app/
├── backend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── main.py              # FastAPI app entry point
│   │   │   ├── database.py          # Database connection
│   │   │   ├── config.py            # Environment configuration
│   │   │   ├── middleware/          # Authentication middleware
│   │   │   ├── models/              # SQLModel database models
│   │   │   ├── schemas/             # Pydantic schemas
│   │   │   ├── services/            # Business logic
│   │   │   └── routers/             # API route handlers
│   │   └── scripts/                 # Migration scripts
├── frontend/
│   ├── src/
│   │   ├── app/                     # Next.js app router pages
│   │   ├── components/              # Reusable React components
│   │   ├── lib/                     # Utility functions
│   │   └── types/                   # TypeScript type definitions
│   ├── public/                      # Static assets
│   └── ...
└── specs/                          # Design specifications
```

## Available Scripts

### Backend
- `uv run uvicorn src.main:app --reload --port 8000` - Start development server
- `uv run pytest` - Run tests

### Frontend
- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Lint code

## API Endpoints

The backend provides the following API endpoints:

- `GET /api/{user_id}/tasks` - Get all tasks for a user
- `POST /api/{user_id}/tasks` - Create a new task
- `GET /api/{user_id}/tasks/{id}` - Get a specific task
- `PUT /api/{user_id}/tasks/{id}` - Update a task
- `DELETE /api/{user_id}/tasks/{id}` - Delete a task
- `PATCH /api/{user_id}/tasks/{id}/complete` - Toggle task completion status

All endpoints require authentication via JWT token in the Authorization header.

## Authentication Flow

1. Users sign up or sign in via the frontend
2. Better Auth handles user registration and session management
3. When making API requests, the frontend exchanges the Better Auth session for a JWT token
4. This JWT token is sent to the backend to authenticate requests
5. The backend verifies the JWT and ensures users can only access their own data

## Data Model

Each task contains:
- `id`: Unique identifier
- `user_id`: Owner of the task (foreign key to user)
- `title`: Task title (required)
- `description`: Optional task description
- `completed`: Boolean indicating completion status
- `priority`: Task priority (low, medium, high)
- `is_starred`: Boolean indicating if task is starred
- `created_at`: Timestamp when task was created
- `updated_at`: Timestamp when task was last updated

## Security Features

- JWT-based authentication
- User data isolation (users can only access their own tasks)
- Input validation
- Protection against common web vulnerabilities

## Development

This project follows a modular architecture with clear separation between frontend and backend. When adding new features:

1. Define the API contract in the backend
2. Implement backend business logic
3. Create frontend components to interact with the API
4. Test thoroughly to ensure security and functionality
