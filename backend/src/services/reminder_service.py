"""
ReminderService for the Todo Chatbot application.
This service handles the business logic for task reminders.
"""

from datetime import datetime, timedelta
from typing import List, Optional
from sqlmodel import Session, select
from loguru import logger

from ..models.task_model import Task
from ..models.reminder_model import Reminder
from ..services.dapr_pubsub_service import publish_task_event
from ..events.task_events import ReminderScheduledEvent, ReminderScheduledEventData


class ReminderService:
    """
    Service class for handling reminder operations.
    Manages the creation, updating, and processing of task reminders.
    """

    def __init__(self, db_session: Session):
        """
        Initialize the ReminderService.

        Args:
            db_session: Database session for database operations
        """
        self.db_session = db_session

    async def create_reminder(
        self,
        user_id: str,
        task_id: int,
        reminder_datetime: datetime,
        channel: str = "email"
    ) -> Reminder:
        """
        Create a new reminder for a task.

        Args:
            user_id: ID of the user the reminder is for
            task_id: ID of the task the reminder is for
            reminder_datetime: When the reminder should be sent
            channel: How the reminder should be sent (email, push, sms)

        Returns:
            Reminder: The created reminder
        """
        # Validate inputs
        if reminder_datetime < datetime.utcnow():
            raise ValueError("Reminder datetime cannot be in the past")

        allowed_channels = ["email", "push", "sms"]
        if channel not in allowed_channels:
            raise ValueError(f"Channel must be one of {allowed_channels}")

        # Check if task exists
        task = await self.get_task_by_id(task_id)
        if not task:
            raise ValueError(f"Task with ID {task_id} does not exist")

        # Check if user owns the task
        if task.user_id != user_id:
            raise ValueError("User does not have permission to set reminder for this task")

        # Create the reminder
        reminder = Reminder(
            user_id=user_id,
            task_id=task_id,
            reminder_datetime=reminder_datetime,
            channel=channel
        )

        # Add to database
        self.db_session.add(reminder)
        self.db_session.commit()
        self.db_session.refresh(reminder)

        # Publish event
        try:
            event_data = ReminderScheduledEventData(
                reminder_id=reminder.id,
                task_id=reminder.task_id,
                scheduled_time=reminder.reminder_datetime,
                channel=reminder.channel,
                trigger_condition="specific_time"  # Default trigger condition
            )

            event = ReminderScheduledEvent(
                user_id=user_id,
                data=event_data
            )

            await publish_task_event("reminder-events", event)
        except Exception as e:
            logger.error(f"Failed to publish reminder scheduled event: {e}")

        logger.info(f"Created reminder {reminder.id} for task {task_id} and user {user_id}")
        return reminder

    async def get_reminder_by_id(self, reminder_id: int) -> Optional[Reminder]:
        """
        Get a reminder by its ID.

        Args:
            reminder_id: ID of the reminder to retrieve

        Returns:
            Reminder: The reminder if found, None otherwise
        """
        statement = select(Reminder).where(Reminder.id == reminder_id)
        result = self.db_session.exec(statement)
        return result.first()

    async def get_reminders_by_user(self, user_id: str) -> List[Reminder]:
        """
        Get all reminders for a specific user.

        Args:
            user_id: ID of the user whose reminders to retrieve

        Returns:
            List[Reminder]: List of reminders for the user
        """
        statement = select(Reminder).where(Reminder.user_id == user_id)
        result = self.db_session.exec(statement)
        return result.all()

    async def get_reminders_by_task(self, task_id: int) -> List[Reminder]:
        """
        Get all reminders for a specific task.

        Args:
            task_id: ID of the task whose reminders to retrieve

        Returns:
            List[Reminder]: List of reminders for the task
        """
        statement = select(Reminder).where(Reminder.task_id == task_id)
        result = self.db_session.exec(statement)
        return result.all()

    async def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """
        Get a task by its ID.

        Args:
            task_id: ID of the task to retrieve

        Returns:
            Task: The task if found, None otherwise
        """
        statement = select(Task).where(Task.id == task_id)
        result = self.db_session.exec(statement)
        return result.first()

    async def update_reminder(
        self,
        reminder_id: int,
        reminder_datetime: Optional[datetime] = None,
        channel: Optional[str] = None
    ) -> Optional[Reminder]:
        """
        Update an existing reminder.

        Args:
            reminder_id: ID of the reminder to update
            reminder_datetime: New reminder datetime (optional)
            channel: New channel (optional)

        Returns:
            Reminder: Updated reminder if successful, None if not found
        """
        reminder = await self.get_reminder_by_id(reminder_id)
        if not reminder:
            return None

        # Update fields if provided
        if reminder_datetime is not None:
            if reminder_datetime < datetime.utcnow():
                raise ValueError("Reminder datetime cannot be in the past")
            reminder.reminder_datetime = reminder_datetime

        if channel is not None:
            allowed_channels = ["email", "push", "sms"]
            if channel not in allowed_channels:
                raise ValueError(f"Channel must be one of {allowed_channels}")
            reminder.channel = channel

        # Update the updated_at timestamp
        reminder.updated_at = datetime.utcnow()

        # Save to database
        self.db_session.add(reminder)
        self.db_session.commit()
        self.db_session.refresh(reminder)

        logger.info(f"Updated reminder {reminder.id}")
        return reminder

    async def delete_reminder(self, reminder_id: int) -> bool:
        """
        Delete a reminder.

        Args:
            reminder_id: ID of the reminder to delete

        Returns:
            bool: True if the reminder was deleted, False if not found
        """
        reminder = await self.get_reminder_by_id(reminder_id)
        if not reminder:
            return False

        # Instead of hard deleting, mark as sent to keep history
        reminder.sent = True
        reminder.updated_at = datetime.utcnow()

        self.db_session.add(reminder)
        self.db_session.commit()

        logger.info(f"Marked reminder {reminder.id} as sent")
        return True

    async def mark_reminder_as_sent(self, reminder_id: int) -> bool:
        """
        Mark a reminder as sent.

        Args:
            reminder_id: ID of the reminder to mark as sent

        Returns:
            bool: True if successful, False if reminder not found
        """
        reminder = await self.get_reminder_by_id(reminder_id)
        if not reminder:
            return False

        reminder.sent = True
        reminder.updated_at = datetime.utcnow()

        self.db_session.add(reminder)
        self.db_session.commit()

        logger.info(f"Marked reminder {reminder.id} as sent")
        return True

    async def get_overdue_reminders(self) -> List[Reminder]:
        """
        Get all overdue reminders (not sent and datetime passed).

        Returns:
            List[Reminder]: List of overdue reminders
        """
        now = datetime.utcnow()
        statement = select(Reminder).where(
            (Reminder.sent == False) &
            (Reminder.reminder_datetime < now)
        )
        result = self.db_session.exec(statement)
        return result.all()

    async def get_reminders_needing_processing(self, buffer_minutes: int = 5) -> List[Reminder]:
        """
        Get all reminders that need processing (within the buffer time).

        Args:
            buffer_minutes: Number of minutes before the reminder time to start processing

        Returns:
            List[Reminder]: List of reminders needing processing
        """
        now = datetime.utcnow()
        buffer_time = now + timedelta(minutes=buffer_minutes)

        statement = select(Reminder).where(
            (Reminder.sent == False) &
            (Reminder.reminder_datetime <= buffer_time) &
            (Reminder.reminder_datetime >= now)
        )
        result = self.db_session.exec(statement)
        return result.all()

    async def process_reminders(self) -> int:
        """
        Process all reminders that need sending.

        Returns:
            int: Number of reminders processed
        """
        reminders_to_process = await self.get_reminders_needing_processing()
        processed_count = 0

        for reminder in reminders_to_process:
            try:
                # In a real implementation, this would trigger the actual notification
                # For this example, we'll just mark the reminder as sent
                await self.mark_reminder_as_sent(reminder.id)
                processed_count += 1

                logger.info(f"Processed reminder {reminder.id} for task {reminder.task_id}")
            except Exception as e:
                logger.error(f"Error processing reminder {reminder.id}: {e}")

        logger.info(f"Processed {processed_count} reminders")
        return processed_count

    async def create_default_reminder(
        self,
        user_id: str,
        task_id: int,
        minutes_before_due: int = 60
    ) -> Optional[Reminder]:
        """
        Create a default reminder for a task based on its due date.

        Args:
            user_id: ID of the user the reminder is for
            task_id: ID of the task to create a reminder for
            minutes_before_due: Minutes before the due date to send the reminder

        Returns:
            Reminder: The created reminder if successful, None if task has no due date
        """
        task = await self.get_task_by_id(task_id)
        if not task or not task.due_date:
            return None

        # Calculate reminder time
        reminder_time = task.due_date - timedelta(minutes=minutes_before_due)

        # Don't create a reminder if it's already in the past
        if reminder_time < datetime.utcnow():
            return None

        # Create the reminder
        reminder = await self.create_reminder(
            user_id=user_id,
            task_id=task_id,
            reminder_datetime=reminder_time,
            channel="email"  # Default channel
        )

        return reminder