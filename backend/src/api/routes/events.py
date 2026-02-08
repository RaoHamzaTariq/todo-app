"""
API routes for events in the Todo Chatbot application.
This module implements the endpoints for streaming and accessing task events.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select, func
from datetime import datetime, timedelta

from ...models.task_event_model import TaskEvent, TaskEventType
from ...services.event_handlers import get_event_handler
from ...core.database import get_session
from ...models.task_model import User
from ...core.security import get_current_user

router = APIRouter(prefix="/api", tags=["events"])


@router.get("/users/{user_id}/events/task-stream", response_model=List[TaskEvent])
async def get_task_events_stream(
    user_id: str,
    event_type: Optional[TaskEventType] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    limit: int = 50,
    offset: int = 0,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Get a stream of task events for a user with optional filters.

    Args:
        user_id: ID of the user whose events to retrieve
        event_type: Filter by specific event type
        start_date: Filter events from this date onwards
        end_date: Filter events up to this date
        limit: Maximum number of events to return (for pagination)
        offset: Number of events to skip (for pagination)
        session: Database session
        current_user: Currently authenticated user

    Returns:
        List[TaskEvent]: List of task events for the user
    """
    # Verify that the user ID in the path matches the authenticated user
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view events for this user"
        )

    # Build query
    query = select(TaskEvent).where(TaskEvent.user_id == user_id)

    # Apply filters
    if event_type:
        query = query.where(TaskEvent.event_type == event_type)

    if start_date:
        query = query.where(TaskEvent.created_at >= start_date)

    if end_date:
        query = query.where(TaskEvent.created_at <= end_date)

    # Apply ordering and pagination
    query = query.order_by(TaskEvent.created_at.desc()).offset(offset).limit(limit)

    # Execute query
    events = session.exec(query).all()

    return events


@router.get("/users/{user_id}/events/summary", response_model=dict)
async def get_events_summary(
    user_id: str,
    days: int = 7,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Get a summary of events for a user over the specified number of days.

    Args:
        user_id: ID of the user whose event summary to retrieve
        days: Number of days to look back (default: 7)
        session: Database session
        current_user: Currently authenticated user

    Returns:
        dict: Summary of events by type and count
    """
    # Verify that the user ID in the path matches the authenticated user
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view events for this user"
        )

    # Calculate the start date
    start_date = datetime.utcnow() - timedelta(days=days)

    # Count events by type
    query = select(TaskEvent.event_type, func.count(TaskEvent.id)).where(
        (TaskEvent.user_id == user_id) &
        (TaskEvent.created_at >= start_date)
    ).group_by(TaskEvent.event_type)

    results = session.exec(query).all()

    # Format the results
    summary = {
        "user_id": user_id,
        "days": days,
        "start_date": start_date.isoformat(),
        "end_date": datetime.utcnow().isoformat(),
        "event_counts": {event_type.value: count for event_type, count in results},
        "total_events": sum(count for _, count in results)
    }

    return summary


@router.get("/users/{user_id}/events/{event_id}", response_model=TaskEvent)
async def get_task_event(
    user_id: str,
    event_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Get a specific task event by its ID.

    Args:
        user_id: ID of the user owning the event
        event_id: ID of the event to retrieve
        session: Database session
        current_user: Currently authenticated user

    Returns:
        TaskEvent: The requested task event

    Raises:
        HTTPException: If the event doesn't exist or user is not authorized
    """
    # Verify that the user ID in the path matches the authenticated user
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this event"
        )

    # Get the specific event
    query = select(TaskEvent).where(
        (TaskEvent.id == event_id) &
        (TaskEvent.user_id == user_id)
    )
    event = session.exec(query).first()

    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )

    return event


@router.get("/users/{user_id}/events/processed-status", response_model=dict)
async def get_processed_events_status(
    user_id: str,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Get the processing status of events for a user.

    Args:
        user_id: ID of the user whose event processing status to retrieve
        session: Database session
        current_user: Currently authenticated user

    Returns:
        dict: Status of processed vs unprocessed events
    """
    # Verify that the user ID in the path matches the authenticated user
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view events for this user"
        )

    # Count processed vs unprocessed events
    total_query = select(func.count(TaskEvent.id)).where(TaskEvent.user_id == user_id)
    total_count = session.exec(total_query).one()

    processed_query = select(func.count(TaskEvent.id)).where(
        (TaskEvent.user_id == user_id) &
        (TaskEvent.processed == True)
    )
    processed_count = session.exec(processed_query).one()

    unprocessed_count = total_count - processed_count

    status_summary = {
        "user_id": user_id,
        "total_events": total_count,
        "processed_events": processed_count,
        "unprocessed_events": unprocessed_count,
        "processing_rate": (processed_count / total_count * 100) if total_count > 0 else 0
    }

    return status_summary