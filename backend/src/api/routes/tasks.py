"""
API routes for tasks in the Todo Chatbot application.
This module implements the endpoints for creating, updating, and managing user tasks.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from datetime import datetime

from ...models.task_model import Task, TaskBase, User
from ...services.task_service import TaskService
from ...core.database import get_session
from ...core.security import get_current_user

router = APIRouter(prefix="/api", tags=["tasks"])


@router.post("/users/{user_id}/tasks", response_model=Task)
async def create_task(
    user_id: str,
    task: TaskBase,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new task for a user.

    Args:
        user_id: ID of the user creating the task
        task: Details of the task to create
        session: Database session
        current_user: Currently authenticated user

    Returns:
        Task: The created task

    Raises:
        HTTPException: If the user is not authorized or inputs are invalid
    """
    # Verify that the user ID in the path matches the authenticated user
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create tasks for this user"
        )

    # Create an instance of the task service
    task_service = TaskService(session)

    try:
        # Create the task
        created_task = await task_service.create_task(
            user_id=user_id,
            title=task.title,
            description=task.description,
            due_date=task.due_date,
            priority=task.priority,
            tags=task.tags,
            status=task.status
        )

        return created_task
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/users/{user_id}/tasks", response_model=List[Task])
async def get_tasks(
    user_id: str,
    skip: int = 0,
    limit: int = 100,
    completed: Optional[bool] = None,
    priority: Optional[str] = None,
    tag: Optional[str] = None,
    status: Optional[str] = None,
    search: Optional[str] = None,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Get all tasks for a user with optional filters.

    Args:
        user_id: ID of the user whose tasks to retrieve
        skip: Number of tasks to skip (for pagination)
        limit: Maximum number of tasks to return (for pagination)
        completed: Filter by completion status
        priority: Filter by priority level
        tag: Filter by tag
        status: Filter by task status
        search: Search term to match in title or description
        session: Database session
        current_user: Currently authenticated user

    Returns:
        List[Task]: List of tasks for the user
    """
    # Verify that the user ID in the path matches the authenticated user
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view tasks for this user"
        )

    # Create an instance of the task service
    task_service = TaskService(session)

    # Get the tasks for the user with filters
    tasks = await task_service.get_tasks_by_user(
        user_id=user_id,
        completed=completed,
        priority=priority,
        tag=tag,
        status=status,
        search=search
    )

    # Apply pagination
    paginated_tasks = tasks[skip : skip + limit]

    return paginated_tasks


@router.get("/users/{user_id}/tasks/{task_id}", response_model=Task)
async def get_task(
    user_id: str,
    task_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Get a specific task by its ID.

    Args:
        user_id: ID of the user owning the task
        task_id: ID of the task to retrieve
        session: Database session
        current_user: Currently authenticated user

    Returns:
        Task: The requested task

    Raises:
        HTTPException: If the task doesn't exist or user is not authorized
    """
    # Verify that the user ID in the path matches the authenticated user
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this task"
        )

    # Create an instance of the task service
    task_service = TaskService(session)

    # Get the specific task
    task = await task_service.get_task_by_id(task_id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Verify that the task belongs to the user
    if task.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this task"
        )

    return task


@router.put("/users/{user_id}/tasks/{task_id}", response_model=Task)
async def update_task(
    user_id: str,
    task_id: int,
    task_update: TaskBase,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Update an existing task.

    Args:
        user_id: ID of the user owning the task
        task_id: ID of the task to update
        task_update: Updated details for the task
        session: Database session
        current_user: Currently authenticated user

    Returns:
        Task: The updated task

    Raises:
        HTTPException: If the task doesn't exist or user is not authorized
    """
    # Verify that the user ID in the path matches the authenticated user
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this task"
        )

    # Create an instance of the task service
    task_service = TaskService(session)

    # Get the existing task to verify it exists and belongs to the user
    existing_task = await task_service.get_task_by_id(task_id)

    if not existing_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Verify that the task belongs to the user
    if existing_task.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this task"
        )

    # Update the task
    updated_task = await task_service.update_task(
        task_id=task_id,
        title=task_update.title,
        description=task_update.description,
        due_date=task_update.due_date,
        priority=task_update.priority,
        tags=task_update.tags,
        status=task_update.status
    )

    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task could not be updated"
        )

    return updated_task


@router.delete("/users/{user_id}/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    user_id: str,
    task_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Delete an existing task.

    Args:
        user_id: ID of the user owning the task
        task_id: ID of the task to delete
        session: Database session
        current_user: Currently authenticated user

    Raises:
        HTTPException: If the task doesn't exist or user is not authorized
    """
    # Verify that the user ID in the path matches the authenticated user
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this task"
        )

    # Create an instance of the task service
    task_service = TaskService(session)

    # Get the existing task to verify it exists and belongs to the user
    existing_task = await task_service.get_task_by_id(task_id)

    if not existing_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Verify that the task belongs to the user
    if existing_task.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this task"
        )

    # Delete the task
    success = await task_service.delete_task(task_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task could not be deleted"
        )


@router.patch("/users/{user_id}/tasks/{task_id}/complete", response_model=Task)
async def toggle_task_completion(
    user_id: str,
    task_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Toggle the completion status of a task.

    Args:
        user_id: ID of the user owning the task
        task_id: ID of the task to toggle completion status
        session: Database session
        current_user: Currently authenticated user

    Returns:
        Task: The updated task with toggled completion status

    Raises:
        HTTPException: If the task doesn't exist or user is not authorized
    """
    # Verify that the user ID in the path matches the authenticated user
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to modify this task"
        )

    # Create an instance of the task service
    task_service = TaskService(session)

    # Get the existing task to verify it exists and belongs to the user
    existing_task = await task_service.get_task_by_id(task_id)

    if not existing_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Verify that the task belongs to the user
    if existing_task.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to modify this task"
        )

    # Toggle completion status
    updated_task = await task_service.toggle_task_completion(task_id)

    return updated_task


@router.get("/users/{user_id}/tasks/search", response_model=List[Task])
async def search_tasks(
    user_id: str,
    q: str,
    priority: Optional[str] = None,
    tag: Optional[str] = None,
    status: Optional[str] = None,
    completed: Optional[bool] = None,
    sort_by: Optional[str] = "created_at",
    order: Optional[str] = "desc",
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Search tasks with filters, sorting, and pagination.

    Args:
        user_id: ID of the user whose tasks to search
        q: Search query string
        priority: Filter by priority level
        tag: Filter by tag
        status: Filter by task status
        completed: Filter by completion status
        sort_by: Field to sort by (created_at, updated_at, due_date, priority)
        order: Sort order (asc or desc)
        skip: Number of tasks to skip (for pagination)
        limit: Maximum number of tasks to return (for pagination)
        session: Database session
        current_user: Currently authenticated user

    Returns:
        List[Task]: List of matching tasks
    """
    # Verify that the user ID in the path matches the authenticated user
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to search tasks for this user"
        )

    # Create an instance of the task service
    task_service = TaskService(session)

    # Search tasks with filters
    tasks = await task_service.search_tasks(
        user_id=user_id,
        search_query=q,
        priority=priority,
        tag=tag,
        status=status,
        completed=completed,
        sort_by=sort_by,
        order=order
    )

    # Apply pagination
    paginated_tasks = tasks[skip : skip + limit]

    return paginated_tasks