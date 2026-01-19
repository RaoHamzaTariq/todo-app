"""
Task API endpoints with JWT authentication and user isolation.

All endpoints follow the pattern: /api/{user_id}/tasks/*
The user_id in the path must match the user_id in the JWT token.
"""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlmodel import Session

from src.app.database import get_session
from src.app.middleware.auth import jwt_bearer
from src.app.schemas.task import (
    CreateTaskInput,
    UpdateTaskInput,
    TaskResponse,
    TaskListResponse,
)
from src.app.schemas.error import ErrorResponse
from src.app.services.task_service import TaskService


router = APIRouter(prefix="/api", tags=["tasks"])


def verify_user_id_match(path_user_id: str, auth_user_id: str) -> None:
    """
    Verify that the user_id in the path matches the authenticated user's ID.

    This prevents users from accessing or modifying other users' data.

    Args:
        path_user_id: user_id from the URL path
        auth_user_id: user_id extracted from JWT token

    Raises:
        HTTPException: 403 if IDs don't match
    """
    if path_user_id != auth_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: user ID mismatch"
        )


@router.get(
    "/{user_id}/tasks",
    response_model=TaskListResponse,
    responses={
        401: {"model": ErrorResponse, "description": "Invalid or missing token"},
        403: {"model": ErrorResponse, "description": "User ID mismatch"},
    }
)
async def list_tasks(
    user_id: str,
    completed: Optional[bool] = None,
    auth_user: dict = Depends(jwt_bearer),
    session: Session = Depends(get_session),
):
    """
    List all tasks for the authenticated user.

    Returns only tasks owned by the authenticated user (user isolation).
    Optionally filters by completion status.
    """
    # Verify ownership
    verify_user_id_match(user_id, auth_user["user_id"])

    # Get tasks for this user
    service = TaskService(session)
    tasks = service.get_tasks_by_user(auth_user["user_id"], completed)

    return TaskListResponse(tasks=[TaskResponse.model_validate(t) for t in tasks])


@router.post(
    "/{user_id}/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        401: {"model": ErrorResponse, "description": "Invalid or missing token"},
        403: {"model": ErrorResponse, "description": "User ID mismatch"},
        422: {"model": ErrorResponse, "description": "Validation error"},
    }
)
async def create_task(
    user_id: str,
    task_data: CreateTaskInput,
    auth_user: dict = Depends(jwt_bearer),
    session: Session = Depends(get_session),
):
    """
    Create a new task for the authenticated user.

    The task is assigned to the user_id from the JWT token (not from request body).
    This ensures strict user data isolation.
    """
    # Verify ownership
    verify_user_id_match(user_id, auth_user["user_id"])

    # Create task using user_id from JWT
    service = TaskService(session)
    task = service.create_task(
        user_id=auth_user["user_id"],
        title=task_data.title,
        description=task_data.description,
        priority=task_data.priority,
        starred=task_data.starred,
    )

    return TaskResponse.model_validate(task)


@router.get(
    "/{user_id}/tasks/{task_id}",
    response_model=TaskResponse,
    responses={
        401: {"model": ErrorResponse, "description": "Invalid or missing token"},
        404: {"model": ErrorResponse, "description": "Task not found"},
    }
)
async def get_task(
    user_id: str,
    task_id: int,
    auth_user: dict = Depends(jwt_bearer),
    session: Session = Depends(get_session),
):
    """
    Get a specific task by ID.

    Returns 404 if task doesn't exist or belongs to a different user.
    This prevents information disclosure about task existence.
    """
    # Verify ownership
    verify_user_id_match(user_id, auth_user["user_id"])

    # Get task with ownership check
    service = TaskService(session)
    task = service.get_task_by_id_and_user(task_id, auth_user["user_id"])

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return TaskResponse.model_validate(task)


@router.put(
    "/{user_id}/tasks/{task_id}",
    response_model=TaskResponse,
    responses={
        401: {"model": ErrorResponse, "description": "Invalid or missing token"},
        404: {"model": ErrorResponse, "description": "Task not found"},
        422: {"model": ErrorResponse, "description": "Validation error"},
    }
)
async def update_task(
    user_id: str,
    task_id: int,
    task_data: UpdateTaskInput,
    auth_user: dict = Depends(jwt_bearer),
    session: Session = Depends(get_session),
):
    """
    Update an existing task.

    Only the task owner can update their tasks.
    Returns 404 if task doesn't exist or belongs to a different user.
    """
    # Verify ownership
    verify_user_id_match(user_id, auth_user["user_id"])

    # Get task with ownership check
    service = TaskService(session)
    task = service.get_task_by_id_and_user(task_id, auth_user["user_id"])

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Update task
    updated_task = service.update_task(
        task=task,
        user_id=auth_user["user_id"],
        title=task_data.title,
        description=task_data.description,
        completed=task_data.completed,
        priority=task_data.priority,
        starred=task_data.starred,
    )

    return TaskResponse.model_validate(updated_task)


@router.delete(
    "/{user_id}/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        401: {"model": ErrorResponse, "description": "Invalid or missing token"},
        404: {"model": ErrorResponse, "description": "Task not found"},
    }
)
async def delete_task(
    user_id: str,
    task_id: int,
    auth_user: dict = Depends(jwt_bearer),
    session: Session = Depends(get_session),
):
    """
    Delete a task (permanent deletion).

    Only the task owner can delete their tasks.
    Returns 404 if task doesn't exist or belongs to a different user.
    """
    # Verify ownership
    verify_user_id_match(user_id, auth_user["user_id"])

    # Get task with ownership check
    service = TaskService(session)
    task = service.get_task_by_id_and_user(task_id, auth_user["user_id"])

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Delete task
    service.delete_task(task, auth_user["user_id"])

    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)


@router.patch(
    "/{user_id}/tasks/{task_id}/complete",
    response_model=TaskResponse,
    responses={
        401: {"model": ErrorResponse, "description": "Invalid or missing token"},
        404: {"model": ErrorResponse, "description": "Task not found"},
    }
)
async def toggle_complete(
    user_id: str,
    task_id: int,
    auth_user: dict = Depends(jwt_bearer),
    session: Session = Depends(get_session),
):
    """
    Toggle task completion status.

    If task is incomplete, mark as complete.
    If task is complete, mark as incomplete.
    Only the task owner can toggle their tasks.
    """
    # Verify ownership
    verify_user_id_match(user_id, auth_user["user_id"])

    # Get task with ownership check
    service = TaskService(session)
    task = service.get_task_by_id_and_user(task_id, auth_user["user_id"])

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Toggle completion
    updated_task = service.toggle_complete(task, auth_user["user_id"])

    return TaskResponse.model_validate(updated_task)
