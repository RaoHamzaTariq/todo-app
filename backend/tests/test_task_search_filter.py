"""
Test suite for task search and filtering functionality in the Todo Chatbot application.
Tests the advanced search, filtering, and sorting capabilities of the task system.
"""

import pytest
from datetime import datetime, timedelta
from sqlmodel import Session, select
from fastapi.testclient import TestClient

from src.models.task_model import Task, User
from src.services.task_service import TaskService
from src.main import app


@pytest.fixture
def client():
    """Create a test client for the API."""
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def db_session():
    """Create a database session for testing."""
    # In a real scenario, you'd want to use a test database
    # For now, we'll assume a session can be created
    from src.core.database import engine
    with Session(engine) as session:
        yield session


@pytest.fixture
def sample_user(db_session):
    """Create a sample user for testing."""
    user = User(
        email="test@example.com",
        preferences='{"theme": "light"}'
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def sample_tasks(db_session, sample_user):
    """Create sample tasks for testing search and filtering."""
    service = TaskService(db_session)

    # Create various tasks with different properties
    task1 = service.create_task(
        user_id=sample_user.id,
        title="Complete project proposal",
        description="Finish the project proposal document for client review",
        priority="high",
        tags="work,important,deadline",
        status="pending"
    )

    task2 = service.create_task(
        user_id=sample_user.id,
        title="Buy groceries",
        description="Milk, eggs, bread, fruits",
        priority="medium",
        tags="personal,shopping",
        status="pending"
    )

    task3 = service.create_task(
        user_id=sample_user.id,
        title="Team meeting",
        description="Weekly team sync meeting",
        priority="medium",
        tags="work,meeting",
        status="completed",
        completed=True
    )

    task4 = service.create_task(
        user_id=sample_user.id,
        title="Read new book",
        description="Start reading the new novel",
        priority="low",
        tags="personal,reading",
        status="in-progress"
    )

    # Add due dates to some tasks
    task1.due_date = datetime.utcnow() + timedelta(days=2)
    task2.due_date = datetime.utcnow() + timedelta(days=1)

    db_session.add(task1)
    db_session.add(task2)
    db_session.commit()

    return [task1, task2, task3, task4]


def test_task_search_by_title(db_session, sample_user, sample_tasks):
    """Test searching tasks by title."""
    service = TaskService(db_session)

    # Search for tasks containing "project"
    results = service.search_tasks(
        user_id=sample_user.id,
        search_query="project"
    )

    assert len(results) == 1
    assert "project" in results[0].title.lower()


def test_task_search_by_description(db_session, sample_user, sample_tasks):
    """Test searching tasks by description."""
    service = TaskService(db_session)

    # Search for tasks containing "groceries"
    results = service.search_tasks(
        user_id=sample_user.id,
        search_query="groceries"
    )

    assert len(results) == 1
    assert "groceries" in results[0].description.lower()


def test_task_filter_by_priority(db_session, sample_user, sample_tasks):
    """Test filtering tasks by priority."""
    service = TaskService(db_session)

    # Get all high priority tasks
    results = service.search_tasks(
        user_id=sample_user.id,
        priority="high"
    )

    assert len(results) == 1
    assert results[0].priority == "high"

    # Get all medium priority tasks
    results = service.search_tasks(
        user_id=sample_user.id,
        priority="medium"
    )

    assert len(results) == 2
    for task in results:
        assert task.priority == "medium"


def test_task_filter_by_status(db_session, sample_user, sample_tasks):
    """Test filtering tasks by status."""
    service = TaskService(db_session)

    # Get all completed tasks
    results = service.search_tasks(
        user_id=sample_user.id,
        status="completed"
    )

    assert len(results) == 1
    assert results[0].status == "completed"

    # Get all pending tasks
    results = service.search_tasks(
        user_id=sample_user.id,
        status="pending"
    )

    assert len(results) == 2
    for task in results:
        assert task.status == "pending"


def test_task_filter_by_tag(db_session, sample_user, sample_tasks):
    """Test filtering tasks by tag."""
    service = TaskService(db_session)

    # Get all tasks with "work" tag
    results = service.search_tasks(
        user_id=sample_user.id,
        tag="work"
    )

    assert len(results) == 2
    for task in results:
        assert "work" in task.tags.lower()


def test_task_filter_by_completion_status(db_session, sample_user, sample_tasks):
    """Test filtering tasks by completion status."""
    service = TaskService(db_session)

    # Get all completed tasks
    results = service.search_tasks(
        user_id=sample_user.id,
        completed=True
    )

    assert len(results) == 1
    assert results[0].completed is True

    # Get all incomplete tasks
    results = service.search_tasks(
        user_id=sample_user.id,
        completed=False
    )

    assert len(results) == 3
    for task in results:
        assert task.completed is False


def test_task_sort_by_created_at(db_session, sample_user, sample_tasks):
    """Test sorting tasks by creation date."""
    service = TaskService(db_session)

    # Get tasks sorted by created_at descending (newest first)
    results_desc = service.search_tasks(
        user_id=sample_user.id,
        sort_by="created_at",
        order="desc"
    )

    # Check that tasks are in descending order of creation time
    for i in range(len(results_desc) - 1):
        assert results_desc[i].created_at >= results_desc[i + 1].created_at

    # Get tasks sorted by created_at ascending (oldest first)
    results_asc = service.search_tasks(
        user_id=sample_user.id,
        sort_by="created_at",
        order="asc"
    )

    # Check that tasks are in ascending order of creation time
    for i in range(len(results_asc) - 1):
        assert results_asc[i].created_at <= results_asc[i + 1].created_at


def test_task_sort_by_priority(db_session, sample_user, sample_tasks):
    """Test sorting tasks by priority."""
    service = TaskService(db_session)

    # Get tasks sorted by priority (assuming high > medium > low)
    results = service.search_tasks(
        user_id=sample_user.id,
        sort_by="priority",
        order="desc"
    )

    # With descending order, high priority should come first
    if len(results) > 1:
        # We expect high priority items to appear first
        priorities_order = [task.priority for task in results]
        # High priority tasks should appear before medium/low priority tasks
        high_indices = [i for i, p in enumerate(priorities_order) if p == "high"]
        med_low_indices = [i for i, p in enumerate(priorities_order) if p in ["medium", "low"]]

        if high_indices and med_low_indices:
            assert min(high_indices) < min(med_low_indices)


def test_combined_filters(db_session, sample_user, sample_tasks):
    """Test combining multiple filters."""
    service = TaskService(db_session)

    # Combine priority and status filters
    results = service.search_tasks(
        user_id=sample_user.id,
        priority="medium",
        status="pending"
    )

    assert len(results) == 1
    assert results[0].priority == "medium"
    assert results[0].status == "pending"


def test_search_with_filters(db_session, sample_user, sample_tasks):
    """Test searching with additional filters."""
    service = TaskService(db_session)

    # Search for tasks with "team" in title AND priority high
    results = service.search_tasks(
        user_id=sample_user.id,
        search_query="team",
        priority="high"
    )

    # Since "team" task is completed and has medium priority, this should return empty
    # Let's try searching for "meeting" with medium priority
    results = service.search_tasks(
        user_id=sample_user.id,
        search_query="meeting",
        priority="medium"
    )

    assert len(results) == 1
    assert "meeting" in results[0].title.lower()
    assert results[0].priority == "medium"


def test_get_tasks_by_user_with_filters(db_session, sample_user, sample_tasks):
    """Test the get_tasks_by_user method with filters."""
    service = TaskService(db_session)

    # Test filtering by status
    results = service.get_tasks_by_user(
        user_id=sample_user.id,
        status="completed"
    )

    assert len(results) == 1
    assert results[0].status == "completed"

    # Test filtering by priority
    results = service.get_tasks_by_user(
        user_id=sample_user.id,
        priority="low"
    )

    assert len(results) == 1
    assert results[0].priority == "low"

    # Test filtering by tag
    results = service.get_tasks_by_user(
        user_id=sample_user.id,
        tag="personal"
    )

    assert len(results) >= 1
    for task in results:
        assert "personal" in task.tags.lower()


def test_case_insensitive_search(db_session, sample_user, sample_tasks):
    """Test that search is case insensitive."""
    service = TaskService(db_session)

    # Search with lowercase
    results_lower = service.search_tasks(
        user_id=sample_user.id,
        search_query="PROJECT"
    )

    # Search with uppercase
    results_upper = service.search_tasks(
        user_id=sample_user.id,
        search_query="project"
    )

    assert len(results_lower) == len(results_upper)
    if len(results_lower) > 0 and len(results_upper) > 0:
        assert results_lower[0].id == results_upper[0].id


def test_empty_search_returns_all(db_session, sample_user, sample_tasks):
    """Test that empty search returns all tasks for the user."""
    service = TaskService(db_session)

    all_tasks = service.get_tasks_by_user(user_id=sample_user.id)
    empty_search_results = service.search_tasks(
        user_id=sample_user.id,
        search_query=""
    )

    assert len(all_tasks) == len(empty_search_results)


if __name__ == "__main__":
    pytest.main([__file__])