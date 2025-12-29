# SDD: Implements Task ID: T007, T008
"""TodoManager for managing tasks with in-memory storage.

This module provides the core business logic for task operations.
"""

from typing import Optional

from src.core.models import Task, TaskStatus


class TodoManager:
    """Manages Task entities with in-memory storage.

    Attributes:
        _tasks: List of Task instances (in-memory)
        _next_id: Next available integer ID for new tasks
    """

    def __init__(self) -> None:
        """Initialize with empty in-memory storage."""
        self._tasks: list[Task] = []
        self._next_id: int = 1

    # CRUD Operations - Method stubs for future implementation

    def add_task(self, title: str, description: str = "") -> Task:
        """Create and store a new task.

        Args:
            title: Task title (required, non-empty)
            description: Optional task description

        Returns:
            The created Task instance

        Raises:
            ValueError: If title is empty or whitespace only
        """
        # SDD: Implements Task ID: T010
        if not title or not title.strip():
            raise ValueError("Title cannot be empty")

        task = Task(
            id=self._next_id,
            title=title.strip(),
            description=description,
            status=TaskStatus.PENDING,
        )
        self._tasks.append(task)
        self._next_id += 1
        return task

    def list_tasks(self) -> list[Task]:
        """Retrieve all tasks ordered by ID.

        Returns:
            List of all tasks, ordered by id ascending
        """
        # SDD: Implements Task ID: T014
        return list(self._tasks)

    def get_task(self, task_id: int) -> Optional[Task]:
        """Retrieve a task by ID.

        Args:
            task_id: The integer ID of the task

        Returns:
            Task if found, None otherwise
        """
        # SDD: Implements Task ID: T016
        for task in self._tasks:
            if task.id == task_id:
                return task
        return None

    def update_task(
        self,
        task_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Optional[Task]:
        """Update an existing task's title and/or description.

        Args:
            task_id: The integer ID of the task to update
            title: New title (if provided)
            description: New description (if provided)

        Returns:
            Updated Task if found, None otherwise

        Raises:
            ValueError: If title is provided but empty
        """
        # SDD: Implements Task ID: T017
        task = self.get_task(task_id)
        if task is None:
            return None

        if title is not None:
            if not title.strip():
                raise ValueError("Title cannot be empty")
            task.title = title.strip()

        if description is not None:
            task.description = description

        return task

    def delete_task(self, task_id: int) -> bool:
        """Delete a task by ID.

        Args:
            task_id: The integer ID of the task to delete

        Returns:
            True if task was deleted, False if not found
        """
        # SDD: Implements Task ID: T021
        task = self.get_task(task_id)
        if task is None:
            return False

        self._tasks.remove(task)
        return True

    def toggle_complete(self, task_id: int) -> Optional[Task]:
        """Toggle task status between Pending and Completed.

        Args:
            task_id: The integer ID of the task

        Returns:
            Updated Task if found, None otherwise
        """
        # SDD: Implements Task ID: T019
        task = self.get_task(task_id)
        if task is None:
            return None

        task.status = (
            TaskStatus.COMPLETED
            if task.status == TaskStatus.PENDING
            else TaskStatus.PENDING
        )
        return task
