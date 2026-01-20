"""
Database connection and session management for SQLModel with Neon PostgreSQL.
"""

import os
from contextlib import contextmanager

from sqlmodel import create_engine, Session, SQLModel
from dotenv import load_dotenv
load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable not set")

# Create engine with serverless-optimized settings
engine = create_engine(
    DATABASE_URL,
    echo=False,  # Set to True for SQL query logging
    pool_pre_ping=True,  # Verify connections before use
    pool_recycle=3600,  # Recycle connections every hour
    connect_args={
        "options": "-c application_name=todo-app-backend"
    }
)


def get_session():
    """Dependency for database sessions."""
    session = Session(engine)
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


@contextmanager
def get_session_context():
    """Context manager for database sessions."""
    session = Session(engine)
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def init_db():
    """Initialize database tables."""
    # Import all models to register them
    # Note: Only importing Task, Conversation, and Message models as User table is managed by Better Auth
    from src.app.models.task import Task
    from src.app.models.conversation import Conversation
    from src.app.models.message import Message

    # Create all tables (Task, Conversation, Message tables; User table is managed by Better Auth)
    SQLModel.metadata.create_all(engine)
    print("Database tables created successfully")


def drop_db():
    """Drop all database tables (use with caution)."""
    SQLModel.metadata.drop_all(engine)
    print("Database tables dropped")
