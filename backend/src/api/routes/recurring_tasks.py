"""
API routes for recurring tasks in the Todo Chatbot application.
This module implements the endpoints for creating, updating, and managing recurring tasks.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from datetime import datetime

from ...models.recurring_task_api_models import (
    RecurringTaskCreate, RecurringTaskUpdate, RecurringTaskPublic
)
from ...services.recurring_task_service import RecurringTaskService
from ...core.database import get_session
from ...models.task_model import User
from ...core.security import get_current_user

router = APIRouter(prefix="/api", tags=["recurring-tasks"])


@router.post("/users/{user_id}/tasks/recurring", response_model=RecurringTaskPublic)
async def create_recurring_task(
    user_id: str,
    recurring_task: RecurringTaskCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new recurring task pattern for a user.

    Args:
        user_id: ID of the user creating the recurring task
        recurring_task: Details of the recurring task to create
        session: Database session
        current_user: Currently authenticated user

    Returns:
        RecurringTaskPublic: The created recurring task

    Raises:
        HTTPException: If the user is not authorized or inputs are invalid
    """
    # Verify that the user ID in the path matches the authenticated user
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create recurring tasks for this user"
        )

    # Create an instance of the recurring task service
    recurring_task_service = RecurringTaskService(session)

    try:
        # Create the recurring task
        created_task = await recurring_task_service.create_recurring_task(
            user_id=user_id,
            title=recurring_task.title,
            description=recurring_task.description,
            frequency=recurring_task.frequency,
            interval=recurring_task.interval,
            end_date=recurring_task.end_date,
            active=recurring_task.active
        )

        return created_task
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/users/{user_id}/tasks/recurring", response_model=List[RecurringTaskPublic])
async def get_recurring_tasks(
    user_id: str,
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Get all recurring tasks for a user.

    Args:
        user_id: ID of the user whose recurring tasks to retrieve
        skip: Number of tasks to skip (for pagination)
        limit: Maximum number of tasks to return (for pagination)
        session: Database session
        current_user: Currently authenticated user

    Returns:
        List[RecurringTaskPublic]: List of recurring tasks for the user
    """
    # Verify that the user ID in the path matches the authenticated user
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view recurring tasks for this user"
        )

    # Create an instance of the recurring task service
    recurring_task_service = RecurringTaskService(session)

    # Get the recurring tasks for the user
    recurring_tasks = await recurring_task_service.get_recurring_tasks_by_user(user_id)

    # Apply pagination
    paginated_tasks = recurring_tasks[skip : skip + limit]

    return paginated_tasks


@router.get("/users/{user_id}/tasks/recurring/{recurring_task_id}", response_model=RecurringTaskPublic)
async def get_recurring_task(
    user_id: str,
    recurring_task_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Get a specific recurring task by its ID.

    Args:
        user_id: ID of the user owning the recurring task
        recurring_task_id: ID of the recurring task to retrieve
        session: Database session
        current_user: Currently authenticated user

    Returns:
        RecurringTaskPublic: The requested recurring task

    Raises:
        HTTPException: If the recurring task doesn't exist or user is not authorized
    """
    # Verify that the user ID in the path matches the authenticated user
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this recurring task"
        )

    # Create an instance of the recurring task service
    recurring_task_service = RecurringTaskService(session)

    # Get the specific recurring task
    recurring_task = await recurring_task_service.get_recurring_task_by_id(recurring_task_id)

    if not recurring_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recurring task not found"
        )

    # Verify that the recurring task belongs to the user
    if recurring_task.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this recurring task"
        )

    return recurring_task


@router.put("/users/{user_id}/tasks/recurring/{recurring_task_id}", response_model=RecurringTaskPublic)
async def update_recurring_task(
    user_id: str,
    recurring_task_id: int,
    recurring_task_update: RecurringTaskUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Update an existing recurring task.

    Args:
        user_id: ID of the user owning the recurring task
        recurring_task_id: ID of the recurring task to update
        recurring_task_update: Updated details for the recurring task
        session: Database session
        current_user: Currently authenticated user

    Returns:
        RecurringTaskPublic: The updated recurring task

    Raises:
        HTTPException: If the recurring task doesn't exist or user is not authorized
    """
    # Verify that the user ID in the path matches the authenticated user
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this recurring task"
        )

    # Create an instance of the recurring task service
    recurring_task_service = RecurringTaskService(session)

    # Get the existing recurring task to verify it exists and belongs to the user
    existing_task = await recurring_task_service.get_recurring_task_by_id(recurring_task_id)

    if not existing_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recurring task not found"
        )

    # Verify that the recurring task belongs to the user
    if existing_task.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this recurring task"
        )

    # Update the recurring task
    updated_task = await recurring_task_service.update_recurring_task(
        recurring_task_id=recurring_task_id,
        title=recurring_task_update.title,
        description=recurring_task_update.description,
        frequency=recurring_task_update.frequency,
        interval=recurring_task_update.interval,
        end_date=recurring_task_update.end_date,
        active=recurring_task_update.active
    )

    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recurring task could not be updated"
        )

    return updated_task


@router.delete("/users/{user_id}/tasks/recurring/{recurring_task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_recurring_task(
    user_id: str,
    recurring_task_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Delete (deactivate) an existing recurring task.

    Args:
        user_id: ID of the user owning the recurring task
        recurring_task_id: ID of the recurring task to delete
        session: Database session
        current_user: Currently authenticated user

    Raises:
        HTTPException: If the recurring task doesn't exist or user is not authorized
    """
    # Verify that the user ID in the path matches the authenticated user
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this recurring task"
        )

    # Create an instance of the recurring task service
    recurring_task_service = RecurringTaskService(session)

    # Get the existing recurring task to verify it exists and belongs to the user
    existing_task = await recurring_task_service.get_recurring_task_by_id(recurring_task_id)

    if not existing_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recurring task not found"
        )

    # Verify that the recurring task belongs to the user
    if existing_task.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this recurring task"
        )

    # Delete (deactivate) the recurring task
    success = await recurring_task_service.delete_recurring_task(recurring_task_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recurring task could not be deleted"
        )