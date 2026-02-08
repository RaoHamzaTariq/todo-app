"""
RecurringTaskService for the Todo Chatbot application.
This service handles the business logic for recurring tasks.
"""

from datetime import datetime, timedelta
from typing import List, Optional
from sqlmodel import Session, select
from loguru import logger

from ..models.task_model import Task, User
from ..models.recurring_task_model import RecurringTask
from ..services.dapr_pubsub_service import publish_task_event
from ..events.task_events import (
    RecurringTaskCreatedEvent, RecurringTaskCreatedEventData,
    RecurringTaskInstanceCreatedEvent, RecurringTaskInstanceCreatedEventData
)


class RecurringTaskService:
    """
    Service class for handling recurring task operations.
    Manages the creation, updating, and generation of recurring tasks.
    """

    def __init__(self, db_session: Session):
        """
        Initialize the RecurringTaskService.

        Args:
            db_session: Database session for database operations
        """
        self.db_session = db_session

    async def create_recurring_task(
        self,
        user_id: str,
        title: str,
        description: Optional[str] = None,
        frequency: str = "daily",
        interval: int = 1,
        end_date: Optional[datetime] = None,
        active: bool = True
    ) -> RecurringTask:
        """
        Create a new recurring task pattern.

        Args:
            user_id: ID of the user creating the recurring task
            title: Title of the recurring task
            description: Description of the recurring task
            frequency: How often the task recurs (daily, weekly, monthly, yearly)
            interval: Multiplier for the frequency (e.g., every 2 weeks)
            end_date: Date when the recurring pattern ends (optional)
            active: Whether the recurring pattern is active

        Returns:
            RecurringTask: The created recurring task pattern
        """
        # Validate inputs
        if not title or len(title.strip()) == 0:
            raise ValueError("Title cannot be empty")

        allowed_frequencies = ["daily", "weekly", "monthly", "yearly"]
        if frequency not in allowed_frequencies:
            raise ValueError(f"Frequency must be one of {allowed_frequencies}")

        if interval <= 0:
            raise ValueError("Interval must be a positive integer")

        if end_date and end_date < datetime.utcnow():
            raise ValueError("End date cannot be in the past")

        # Create the recurring task
        recurring_task = RecurringTask(
            user_id=user_id,
            title=title.strip(),
            description=description,
            frequency=frequency,
            interval=interval,
            end_date=end_date,
            active=active
        )

        # Add to database
        self.db_session.add(recurring_task)
        self.db_session.commit()
        self.db_session.refresh(recurring_task)

        # Publish event
        try:
            event_data = RecurringTaskCreatedEventData(
                recurring_task_id=recurring_task.id,
                title=recurring_task.title,
                description=recurring_task.description,
                frequency=recurring_task.frequency,
                interval=recurring_task.interval,
                end_date=recurring_task.end_date,
                active=recurring_task.active
            )

            event = RecurringTaskCreatedEvent(
                user_id=user_id,
                data=event_data
            )

            await publish_task_event("recurring-task-events", event)
        except Exception as e:
            logger.error(f"Failed to publish recurring task created event: {e}")

        logger.info(f"Created recurring task {recurring_task.id} for user {user_id}")
        return recurring_task

    async def get_recurring_task_by_id(self, recurring_task_id: int) -> Optional[RecurringTask]:
        """
        Get a recurring task by its ID.

        Args:
            recurring_task_id: ID of the recurring task to retrieve

        Returns:
            RecurringTask: The recurring task if found, None otherwise
        """
        statement = select(RecurringTask).where(RecurringTask.id == recurring_task_id)
        result = self.db_session.exec(statement)
        return result.first()

    async def get_recurring_tasks_by_user(self, user_id: str) -> List[RecurringTask]:
        """
        Get all recurring tasks for a specific user.

        Args:
            user_id: ID of the user whose recurring tasks to retrieve

        Returns:
            List[RecurringTask]: List of recurring tasks for the user
        """
        statement = select(RecurringTask).where(RecurringTask.user_id == user_id)
        result = self.db_session.exec(statement)
        return result.all()

    async def update_recurring_task(
        self,
        recurring_task_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        frequency: Optional[str] = None,
        interval: Optional[int] = None,
        end_date: Optional[datetime] = None,
        active: Optional[bool] = None
    ) -> Optional[RecurringTask]:
        """
        Update an existing recurring task.

        Args:
            recurring_task_id: ID of the recurring task to update
            title: New title (optional)
            description: New description (optional)
            frequency: New frequency (optional)
            interval: New interval (optional)
            end_date: New end date (optional)
            active: New active status (optional)

        Returns:
            RecurringTask: Updated recurring task if successful, None if not found
        """
        recurring_task = await self.get_recurring_task_by_id(recurring_task_id)
        if not recurring_task:
            return None

        # Update fields if provided
        if title is not None:
            if not title or len(title.strip()) == 0:
                raise ValueError("Title cannot be empty")
            recurring_task.title = title.strip()

        if description is not None:
            recurring_task.description = description

        if frequency is not None:
            allowed_frequencies = ["daily", "weekly", "monthly", "yearly"]
            if frequency not in allowed_frequencies:
                raise ValueError(f"Frequency must be one of {allowed_frequencies}")
            recurring_task.frequency = frequency

        if interval is not None:
            if interval <= 0:
                raise ValueError("Interval must be a positive integer")
            recurring_task.interval = interval

        if end_date is not None:
            if end_date < datetime.utcnow():
                raise ValueError("End date cannot be in the past")
            recurring_task.end_date = end_date

        if active is not None:
            recurring_task.active = active

        # Update the updated_at timestamp
        recurring_task.updated_at = datetime.utcnow()

        # Save to database
        self.db_session.add(recurring_task)
        self.db_session.commit()
        self.db_session.refresh(recurring_task)

        logger.info(f"Updated recurring task {recurring_task.id}")
        return recurring_task

    async def delete_recurring_task(self, recurring_task_id: int) -> bool:
        """
        Delete a recurring task.

        Args:
            recurring_task_id: ID of the recurring task to delete

        Returns:
            bool: True if the recurring task was deleted, False if not found
        """
        recurring_task = await self.get_recurring_task_by_id(recurring_task_id)
        if not recurring_task:
            return False

        # Mark as inactive instead of hard deleting to preserve history
        recurring_task.active = False
        recurring_task.updated_at = datetime.utcnow()

        self.db_session.add(recurring_task)
        self.db_session.commit()

        logger.info(f"Deactivated recurring task {recurring_task.id}")
        return True

    async def generate_task_instances_from_recurring(self, recurring_task_id: int) -> List[Task]:
        """
        Generate task instances from a recurring task pattern.

        Args:
            recurring_task_id: ID of the recurring task to generate instances from

        Returns:
            List[Task]: List of generated task instances
        """
        recurring_task = await self.get_recurring_task_by_id(recurring_task_id)
        if not recurring_task or not recurring_task.active:
            return []

        # Find the last generated task for this recurring pattern
        # In a real implementation, we would track which instances have been generated
        # For this implementation, we'll just generate the next instance

        now = datetime.utcnow()

        # Calculate the next occurrence based on the pattern
        next_occurrence = recurring_task.calculate_next_occurrence(now)
        if not next_occurrence:
            return []  # Pattern is not active anymore

        # Create a new task instance
        new_task = Task(
            user_id=recurring_task.user_id,
            title=recurring_task.title,
            description=recurring_task.description,
            due_date=next_occurrence,
            priority="medium",  # Default priority for generated tasks
            status="pending",
            completed=False
        )

        # Add to database
        self.db_session.add(new_task)
        self.db_session.commit()
        self.db_session.refresh(new_task)

        # Publish event for the new task instance
        try:
            event_data = RecurringTaskInstanceCreatedEventData(
                original_recurring_task_id=recurring_task.id,
                new_task_id=new_task.id,
                due_date=new_task.due_date,
                is_template=False
            )

            event = RecurringTaskInstanceCreatedEvent(
                user_id=recurring_task.user_id,
                data=event_data
            )

            await publish_task_event("recurring-task-events", event)
        except Exception as e:
            logger.error(f"Failed to publish recurring task instance created event: {e}")

        logger.info(f"Generated task instance {new_task.id} from recurring task {recurring_task.id}")
        return [new_task]

    async def get_active_recurring_tasks(self) -> List[RecurringTask]:
        """
        Get all active recurring tasks.

        Returns:
            List[RecurringTask]: List of all active recurring tasks
        """
        statement = select(RecurringTask).where(RecurringTask.active == True)
        result = self.db_session.exec(statement)
        return result.all()

    async def process_recurring_tasks(self) -> int:
        """
        Process all active recurring tasks and generate new instances if needed.

        Returns:
            int: Number of task instances generated
        """
        active_recurring_tasks = await self.get_active_recurring_tasks()
        generated_count = 0

        for recurring_task in active_recurring_tasks:
            try:
                # Generate instances for this recurring task
                instances = await self.generate_task_instances_from_recurring(recurring_task.id)
                generated_count += len(instances)
            except Exception as e:
                logger.error(f"Error processing recurring task {recurring_task.id}: {e}")

        logger.info(f"Processed recurring tasks, generated {generated_count} instances")
        return generated_count