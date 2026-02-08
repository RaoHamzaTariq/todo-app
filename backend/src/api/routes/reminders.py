"""
API routes for reminders in the Todo Chatbot application.
This module implements the endpoints for creating, updating, and managing task reminders.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from datetime import datetime

from ...models.reminder_api_models import (
    ReminderCreate, ReminderUpdate, ReminderPublic
)
from ...services.reminder_service import ReminderService
from ...core.database import get_session
from ...models.task_model import User
from ...core.security import get_current_user

router = APIRouter(prefix="/api", tags=["reminders"])


@router.post("/users/{user_id}/reminders", response_model=ReminderPublic)
async def create_reminder(
    user_id: str,
    reminder: ReminderCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new reminder for a task.

    Args:
        user_id: ID of the user creating the reminder
        reminder: Details of the reminder to create
        session: Database session
        current_user: Currently authenticated user

    Returns:
        ReminderPublic: The created reminder

    Raises:
        HTTPException: If the user is not authorized or inputs are invalid
    """
    # Verify that the user ID in the path matches the authenticated user
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create reminders for this user"
        )

    # Create an instance of the reminder service
    reminder_service = ReminderService(session)

    try:
        # Create the reminder
        created_reminder = await reminder_service.create_reminder(
            user_id=user_id,
            task_id=reminder.task_id,
            reminder_datetime=reminder.reminder_datetime,
            channel=reminder.channel
        )

        return created_reminder
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/users/{user_id}/reminders", response_model=List[ReminderPublic])
async def get_reminders(
    user_id: str,
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Get all reminders for a user.

    Args:
        user_id: ID of the user whose reminders to retrieve
        skip: Number of reminders to skip (for pagination)
        limit: Maximum number of reminders to return (for pagination)
        session: Database session
        current_user: Currently authenticated user

    Returns:
        List[ReminderPublic]: List of reminders for the user
    """
    # Verify that the user ID in the path matches the authenticated user
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view reminders for this user"
        )

    # Create an instance of the reminder service
    reminder_service = ReminderService(session)

    # Get the reminders for the user
    reminders = await reminder_service.get_reminders_by_user(user_id)

    # Apply pagination
    paginated_reminders = reminders[skip : skip + limit]

    return paginated_reminders


@router.get("/users/{user_id}/reminders/{reminder_id}", response_model=ReminderPublic)
async def get_reminder(
    user_id: str,
    reminder_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Get a specific reminder by its ID.

    Args:
        user_id: ID of the user owning the reminder
        reminder_id: ID of the reminder to retrieve
        session: Database session
        current_user: Currently authenticated user

    Returns:
        ReminderPublic: The requested reminder

    Raises:
        HTTPException: If the reminder doesn't exist or user is not authorized
    """
    # Verify that the user ID in the path matches the authenticated user
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this reminder"
        )

    # Create an instance of the reminder service
    reminder_service = ReminderService(session)

    # Get the specific reminder
    reminder = await reminder_service.get_reminder_by_id(reminder_id)

    if not reminder:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reminder not found"
        )

    # Verify that the reminder belongs to the user
    if reminder.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this reminder"
        )

    return reminder


@router.put("/users/{user_id}/reminders/{reminder_id}", response_model=ReminderPublic)
async def update_reminder(
    user_id: str,
    reminder_id: int,
    reminder_update: ReminderUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Update an existing reminder.

    Args:
        user_id: ID of the user owning the reminder
        reminder_id: ID of the reminder to update
        reminder_update: Updated details for the reminder
        session: Database session
        current_user: Currently authenticated user

    Returns:
        ReminderPublic: The updated reminder

    Raises:
        HTTPException: If the reminder doesn't exist or user is not authorized
    """
    # Verify that the user ID in the path matches the authenticated user
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this reminder"
        )

    # Create an instance of the reminder service
    reminder_service = ReminderService(session)

    # Get the existing reminder to verify it exists and belongs to the user
    existing_reminder = await reminder_service.get_reminder_by_id(reminder_id)

    if not existing_reminder:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reminder not found"
        )

    # Verify that the reminder belongs to the user
    if existing_reminder.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this reminder"
        )

    # Update the reminder
    updated_reminder = await reminder_service.update_reminder(
        reminder_id=reminder_id,
        reminder_datetime=reminder_update.reminder_datetime,
        channel=reminder_update.channel
    )

    if not updated_reminder:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reminder could not be updated"
        )

    return updated_reminder


@router.delete("/users/{user_id}/reminders/{reminder_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_reminder(
    user_id: str,
    reminder_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Delete (cancel) an existing reminder.

    Args:
        user_id: ID of the user owning the reminder
        reminder_id: ID of the reminder to delete
        session: Database session
        current_user: Currently authenticated user

    Raises:
        HTTPException: If the reminder doesn't exist or user is not authorized
    """
    # Verify that the user ID in the path matches the authenticated user
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this reminder"
        )

    # Create an instance of the reminder service
    reminder_service = ReminderService(session)

    # Get the existing reminder to verify it exists and belongs to the user
    existing_reminder = await reminder_service.get_reminder_by_id(reminder_id)

    if not existing_reminder:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reminder not found"
        )

    # Verify that the reminder belongs to the user
    if existing_reminder.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this reminder"
        )

    # Delete (cancel) the reminder
    success = await reminder_service.delete_reminder(reminder_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reminder could not be deleted"
        )