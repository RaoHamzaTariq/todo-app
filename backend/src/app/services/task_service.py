"""
Business logic for task operations.

All functions use user_id from JWT token (not from request body)
to ensure strict user data isolation per Constitution Principle VI.
"""

from typing import Optional, List

from sqlmodel import Session, select

from src.app.models.task import Task


class TaskService:
    """Service class for task business logic."""

    def __init__(self, session: Session):
        """Initialize with database session."""
        self.session = session

    def create_task(
        self,
        user_id: str,
        title: str,
        description: Optional[str] = None,
        priority: str = "medium",
        starred: bool = False
    ) -> Task:
        """
        Create a new task for the authenticated user.

        Args:
            user_id: Owner ID from JWT token (NOT from request body)
            title: Task title
            description: Optional task description
            priority: Task priority
            starred: Is task starred

        Returns:
            Created Task instance
        """
        task = Task(
            user_id=user_id,
            title=title,
            description=description,
            priority=priority,
            is_starred=starred
        )
        self.session.add(task)
        self.session.flush()
        self.session.refresh(task)
        return task

    def get_tasks_by_user(self, user_id: str, completed: Optional[bool] = None) -> List[Task]:
        """
        Get all tasks for a user, optionally filtered by completion status.

        Args:
            user_id: Owner ID from JWT token
            completed: Optional filter for completion status

        Returns:
            List of Task instances
        """
        query = select(Task).where(Task.user_id == user_id)
        if completed is not None:
            query = query.where(Task.completed == completed)
        query = query.order_by(Task.is_starred.desc(), Task.created_at.desc()) # Starred first
        return list(self.session.exec(query).all())

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """
        Get a task by ID (without ownership check).

        Args:
            task_id: Task ID

        Returns:
            Task instance or None
        """
        return self.session.get(Task, task_id)

    def get_task_by_id_and_user(self, task_id: int, user_id: str) -> Optional[Task]:
        """
        Get a task by ID with ownership verification.

        Args:
            task_id: Task ID
            user_id: Owner ID from JWT token

        Returns:
            Task instance or None if not found or not owned by user
        """
        task = self.session.get(Task, task_id)
        if task is None or task.user_id != user_id:
            return None
        return task

    def update_task(
        self,
        task: Task,
        user_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        completed: Optional[bool] = None,
        priority: Optional[str] = None,
        starred: Optional[bool] = None
    ) -> Task:
        """
        Update an existing task.

        Args:
            task: Task instance to update
            user_id: Owner ID from JWT token (for ownership verification)
            title: New title (optional)
            description: New description (optional)
            completed: New completion status (optional)
            priority: New priority (optional)
            starred: New starred status (optional)

        Returns:
            Updated Task instance

        Raises:
            ValueError: If user_id would be changed (immutable)
        """
        # Verify ownership
        if task.user_id != user_id:
            raise ValueError("Cannot update task owned by another user")

        # Update fields if provided
        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        if completed is not None:
            task.completed = completed
        if priority is not None:
            task.priority = priority
        if starred is not None:
            task.is_starred = starred

        task.updated_at = task.__class__.updated_at.field.get_default()()

        self.session.flush()
        self.session.refresh(task)
        return task

    def toggle_complete(self, task: Task, user_id: str) -> Task:
        """
        Toggle task completion status.

        Args:
            task: Task instance to toggle
            user_id: Owner ID from JWT token

        Returns:
            Updated Task instance
        """
        # Verify ownership
        if task.user_id != user_id:
            raise ValueError("Cannot toggle task owned by another user")

        # Toggle completion status
        task.completed = not task.completed
        task.updated_at = task.__class__.updated_at.field.get_default()()

        self.session.flush()
        self.session.refresh(task)
        return task

    def delete_task(self, task: Task, user_id: str) -> None:
        """
        Delete a task (permanent deletion).

        Args:
            task: Task instance to delete
            user_id: Owner ID from JWT token

        Raises:
            ValueError: If task owned by different user
        """
        # Verify ownership
        if task.user_id != user_id:
            raise ValueError("Cannot delete task owned by another user")

        self.session.delete(task)
        self.session.flush()
