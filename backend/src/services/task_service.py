"""
Task service for the Todo Chatbot application.
Handles business logic for task management including creation, updates, search, and filtering.
"""

from typing import List, Optional
from sqlmodel import Session, select, func
from datetime import datetime

from ..models.task_model import Task


class TaskService:
    """
    Service class for handling task-related business logic.
    """

    def __init__(self, session: Session):
        """
        Initialize the task service.

        Args:
            session: Database session to use for operations
        """
        self.session = session

    async def create_task(
        self,
        user_id: str,
        title: str,
        description: Optional[str] = None,
        due_date: Optional[datetime] = None,
        priority: str = "medium",
        tags: Optional[str] = None,
        status: str = "pending"
    ) -> Task:
        """
        Create a new task.

        Args:
            user_id: ID of the user creating the task
            title: Title of the task
            description: Description of the task
            due_date: Due date for the task
            priority: Priority level (low, medium, high)
            tags: Comma-separated tags for the task
            status: Status of the task (pending, in-progress, completed)

        Returns:
            Task: The created task
        """
        # Validate inputs
        if not title or len(title.strip()) == 0:
            raise ValueError("Title is required")

        allowed_priorities = ["low", "medium", "high"]
        if priority not in allowed_priorities:
            raise ValueError(f"Priority must be one of {allowed_priorities}")

        allowed_statuses = ["pending", "in-progress", "completed"]
        if status not in allowed_statuses:
            raise ValueError(f"Status must be one of {allowed_statuses}")

        # Create task instance
        task = Task(
            user_id=user_id,
            title=title.strip(),
            description=description,
            due_date=due_date,
            priority=priority,
            tags=tags,
            status=status
        )

        # Add to session and commit
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)

        return task

    async def get_tasks_by_user(
        self,
        user_id: str,
        completed: Optional[bool] = None,
        priority: Optional[str] = None,
        tag: Optional[str] = None,
        status: Optional[str] = None,
        search: Optional[str] = None
    ) -> List[Task]:
        """
        Get all tasks for a user with optional filters.

        Args:
            user_id: ID of the user whose tasks to retrieve
            completed: Filter by completion status
            priority: Filter by priority level
            tag: Filter by tag
            status: Filter by task status
            search: Search term to match in title or description

        Returns:
            List[Task]: List of tasks matching the criteria
        """
        query = select(Task).where(Task.user_id == user_id)

        # Apply filters
        if completed is not None:
            query = query.where(Task.completed == completed)

        if priority is not None:
            query = query.where(Task.priority == priority.lower())

        if status is not None:
            query = query.where(Task.status == status.lower().replace(" ", "-"))

        if tag is not None:
            # Search for tasks that contain the tag
            query = query.where(Task.tags.contains(tag.lower()))

        if search is not None and len(search.strip()) > 0:
            search_term = f"%{search.strip()}%"
            query = query.where(
                (Task.title.ilike(search_term)) | (Task.description.ilike(search_term))
            )

        # Execute query
        tasks = self.session.exec(query).all()
        return tasks

    async def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """
        Get a specific task by its ID.

        Args:
            task_id: ID of the task to retrieve

        Returns:
            Task: The requested task, or None if not found
        """
        query = select(Task).where(Task.id == task_id)
        task = self.session.exec(query).first()
        return task

    async def update_task(
        self,
        task_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        due_date: Optional[datetime] = None,
        priority: Optional[str] = None,
        tags: Optional[str] = None,
        status: Optional[str] = None
    ) -> Optional[Task]:
        """
        Update an existing task.

        Args:
            task_id: ID of the task to update
            title: New title for the task
            description: New description for the task
            due_date: New due date for the task
            priority: New priority level
            tags: New tags for the task
            status: New status for the task

        Returns:
            Task: The updated task, or None if not found
        """
        # Get the existing task
        task = await self.get_task_by_id(task_id)
        if not task:
            return None

        # Update fields if provided
        if title is not None:
            if not title or len(title.strip()) == 0:
                raise ValueError("Title cannot be empty")
            task.title = title.strip()

        if description is not None:
            task.description = description

        if due_date is not None:
            task.due_date = due_date

        if priority is not None:
            allowed_priorities = ["low", "medium", "high"]
            if priority not in allowed_priorities:
                raise ValueError(f"Priority must be one of {allowed_priorities}")
            task.priority = priority

        if tags is not None:
            task.tags = tags

        if status is not None:
            allowed_statuses = ["pending", "in-progress", "completed"]
            if status not in allowed_statuses:
                raise ValueError(f"Status must be one of {allowed_statuses}")
            task.status = status

        # Update timestamps
        task.updated_at = datetime.utcnow()

        # Commit changes
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)

        return task

    async def delete_task(self, task_id: int) -> bool:
        """
        Delete a task.

        Args:
            task_id: ID of the task to delete

        Returns:
            bool: True if the task was deleted, False if not found
        """
        task = await self.get_task_by_id(task_id)
        if not task:
            return False

        self.session.delete(task)
        self.session.commit()
        return True

    async def toggle_task_completion(self, task_id: int) -> Optional[Task]:
        """
        Toggle the completion status of a task.

        Args:
            task_id: ID of the task to toggle

        Returns:
            Task: The updated task with toggled completion status, or None if not found
        """
        task = await self.get_task_by_id(task_id)
        if not task:
            return None

        # Toggle completion status
        task.completed = not task.completed
        task.updated_at = datetime.utcnow()

        # Commit changes
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)

        return task

    async def search_tasks(
        self,
        user_id: str,
        search_query: str,
        priority: Optional[str] = None,
        tag: Optional[str] = None,
        status: Optional[str] = None,
        completed: Optional[bool] = None,
        sort_by: str = "created_at",
        order: str = "desc"
    ) -> List[Task]:
        """
        Search tasks with filters, sorting, and pagination.

        Args:
            user_id: ID of the user whose tasks to search
            search_query: Query string to search for
            priority: Filter by priority level
            tag: Filter by tag
            status: Filter by task status
            completed: Filter by completion status
            sort_by: Field to sort by (created_at, updated_at, due_date, priority)
            order: Sort order ('asc' or 'desc')

        Returns:
            List[Task]: List of matching tasks
        """
        # Build query
        query = select(Task).where(Task.user_id == user_id)

        # Apply search filter
        if search_query and len(search_query.strip()) > 0:
            search_term = f"%{search_query.strip()}%"
            query = query.where(
                (Task.title.ilike(search_term)) | (Task.description.ilike(search_term))
            )

        # Apply other filters
        if completed is not None:
            query = query.where(Task.completed == completed)

        if priority is not None:
            query = query.where(Task.priority == priority.lower())

        if status is not None:
            query = query.where(Task.status == status.lower().replace(" ", "-"))

        if tag is not None:
            # Search for tasks that contain the tag
            query = query.where(Task.tags.contains(tag.lower()))

        # Apply sorting
        if hasattr(Task, sort_by):
            sort_column = getattr(Task, sort_by)
            if order.lower() == "desc":
                query = query.order_by(sort_column.desc())
            else:
                query = query.order_by(sort_column.asc())

        # Execute query
        tasks = self.session.exec(query).all()
        return tasks