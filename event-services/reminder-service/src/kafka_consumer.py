"""
Kafka consumer service for reminder events in the Todo Chatbot application.
"""

import asyncio
import json
from datetime import datetime
from typing import Dict, Any, Callable
from loguru import logger

from ....backend.src.events.task_events import (
    EventBase, ReminderScheduledEvent, ReminderTriggeredEvent,
    TaskCreatedEvent, TaskUpdatedEvent, RecurringTaskCreatedEvent
)


class KafkaConsumerService:
    """
    Service class for consuming Kafka events using Dapr's pub/sub capabilities.
    Specifically handles reminder-related events and schedules reminders appropriately.
    """

    def __init__(self, dapr_client=None):
        """
        Initialize the Kafka consumer service.

        Args:
            dapr_client: Dapr client instance (will be injected by Dapr runtime)
        """
        self.dapr_client = dapr_client
        self._initialized = False
        self._subscriptions = {}
        self._running = False
        self.reminder_scheduler = ReminderScheduler()

    async def initialize(self):
        """Initialize the Kafka consumer service."""
        try:
            if self.dapr_client is None:
                # Import here to avoid dependency issues if Dapr is not available
                try:
                    from dapr.aio.clients import DaprClient
                    self.dapr_client = DaprClient()
                except ImportError:
                    logger.warning("Dapr client not available. Using mock mode.")
                    self.dapr_client = MockDaprClient()

            self._initialized = True
            logger.info("KafkaConsumerService initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize KafkaConsumerService: {e}")
            raise

    async def subscribe_to_topic(self, topic: str, callback: Callable[[Dict[str, Any]], None]):
        """
        Subscribe to a Kafka topic with a callback function.

        Args:
            topic: The Kafka topic to subscribe to
            callback: Function to call when a message is received
        """
        if not self._initialized:
            await self.initialize()

        self._subscriptions[topic] = callback
        logger.info(f"Subscribed to topic: {topic}")

    async def start_consuming(self):
        """Start consuming messages from subscribed topics."""
        if not self._initialized:
            await self.initialize()

        self._running = True
        logger.info("Starting to consume messages...")

        # In a real Dapr implementation, we'd use Dapr's subscription mechanism
        # For now, we'll simulate this with a polling approach
        while self._running:
            try:
                # Process reminder events
                await self._process_reminder_events()

                # Wait before next polling cycle
                await asyncio.sleep(1)
            except Exception as e:
                logger.error(f"Error in consumption loop: {e}")
                await asyncio.sleep(5)  # Wait longer on error

    async def _process_reminder_events(self):
        """
        Process reminder events from the queue.
        In a real implementation, this would use Dapr's pub/sub subscription.
        """
        # In a real implementation, Dapr would automatically call our subscription handlers
        # This is a simplified simulation of that process
        pass

    async def handle_reminder_scheduled_event(self, event_data: Dict[str, Any]):
        """
        Handle a reminder scheduled event by adding it to the scheduler.

        Args:
            event_data: The event data containing reminder information
        """
        try:
            # Deserialize the event
            event_dict = {
                'event_type': event_data['event_type'],
                'event_id': event_data['event_id'],
                'timestamp': datetime.fromisoformat(event_data['timestamp'].replace('Z', '+00:00')),
                'user_id': event_data['user_id'],
                'correlation_id': event_data.get('correlation_id'),
                'data': event_data['data']
            }

            reminder_event = ReminderScheduledEvent(**event_dict)

            logger.info(f"Processing reminder scheduled event for user {reminder_event.user_id}, "
                       f"task {reminder_event.data.task_id}, reminder {reminder_event.data.reminder_id}")

            # Schedule the reminder with the reminder scheduler
            await self.reminder_scheduler.schedule_reminder(
                reminder_id=reminder_event.data.reminder_id,
                user_id=reminder_event.user_id,
                task_id=reminder_event.data.task_id,
                scheduled_time=reminder_event.data.scheduled_time,
                channel=reminder_event.data.channel,
                trigger_condition=reminder_event.data.trigger_condition
            )

        except Exception as e:
            logger.error(f"Error handling reminder scheduled event: {e}")

    async def handle_task_created_event(self, event_data: Dict[str, Any]):
        """
        Handle a task created event by checking if it has a due date that needs a reminder.

        Args:
            event_data: The event data containing task information
        """
        try:
            # Deserialize the event
            event_dict = {
                'event_type': event_data['event_type'],
                'event_id': event_data['event_id'],
                'timestamp': datetime.fromisoformat(event_data['timestamp'].replace('Z', '+00:00')),
                'user_id': event_data['user_id'],
                'correlation_id': event_data.get('correlation_id'),
                'data': event_data['data']
            }

            task_event = TaskCreatedEvent(**event_dict)

            # Check if the task has a due date and if the user wants a reminder
            if task_event.data.due_date:
                logger.info(f"Task {task_event.data.task_id} has due date, checking for reminder preferences")

                # Schedule a reminder based on user preferences (e.g., 1 hour before due date)
                await self.reminder_scheduler.create_default_reminder(
                    user_id=task_event.user_id,
                    task_id=task_event.data.task_id,
                    due_date=task_event.data.due_date
                )

        except Exception as e:
            logger.error(f"Error handling task created event: {e}")

    async def handle_task_updated_event(self, event_data: Dict[str, Any]):
        """
        Handle a task updated event by checking if reminder adjustments are needed.

        Args:
            event_data: The event data containing task update information
        """
        try:
            # Deserialize the event
            event_dict = {
                'event_type': event_data['event_type'],
                'event_id': event_data['event_id'],
                'timestamp': datetime.fromisoformat(event_data['timestamp'].replace('Z', '+00:00')),
                'user_id': event_data['user_id'],
                'correlation_id': event_data.get('correlation_id'),
                'data': event_data['data']
            }

            task_event = TaskUpdatedEvent(**event_dict)

            # Check if the due date was updated and adjust reminders accordingly
            if 'due_date' in task_event.data.updated_fields:
                old_due_date = task_event.data.changes.get('due_date', {}).get('old_value')
                new_due_date = task_event.data.changes.get('due_date', {}).get('new_value')

                if old_due_date != new_due_date:
                    logger.info(f"Task {task_event.data.task_id} due date updated, "
                               f"adjusting reminders from {old_due_date} to {new_due_date}")

                    # Reschedule any existing reminders for this task
                    await self.reminder_scheduler.reschedule_reminder_for_task(
                        task_id=task_event.data.task_id,
                        new_due_date=new_due_date
                    )

        except Exception as e:
            logger.error(f"Error handling task updated event: {e}")

    async def stop_consuming(self):
        """Stop consuming messages."""
        self._running = False
        logger.info("Stopped consuming messages")


class ReminderScheduler:
    """
    Simple reminder scheduler to manage reminder timing and delivery.
    In a real implementation, this might interface with a more sophisticated scheduling system.
    """

    def __init__(self):
        self.pending_reminders = {}
        self.scheduler_task = None

    async def schedule_reminder(self, reminder_id: int, user_id: str, task_id: int,
                              scheduled_time: datetime, channel: str,
                              trigger_condition: str):
        """
        Schedule a reminder for delivery at a specific time.

        Args:
            reminder_id: Unique ID for the reminder
            user_id: ID of the user to notify
            task_id: ID of the task associated with the reminder
            scheduled_time: When the reminder should be sent
            channel: How to send the reminder (email, push, sms)
            trigger_condition: Condition that triggers the reminder
        """
        # Store reminder in memory (in production, this would be persisted)
        reminder_info = {
            'reminder_id': reminder_id,
            'user_id': user_id,
            'task_id': task_id,
            'scheduled_time': scheduled_time,
            'channel': channel,
            'trigger_condition': trigger_condition,
            'created_at': datetime.now()
        }

        self.pending_reminders[reminder_id] = reminder_info
        logger.info(f"Scheduled reminder {reminder_id} for {scheduled_time}")

        # Start scheduler if not already running
        if self.scheduler_task is None or self.scheduler_task.done():
            self.scheduler_task = asyncio.create_task(self._run_scheduler())

    async def create_default_reminder(self, user_id: str, task_id: int, due_date: datetime):
        """
        Create a default reminder for a task (e.g., 1 hour before due date).

        Args:
            user_id: ID of the user to notify
            task_id: ID of the task associated with the reminder
            due_date: The due date of the task
        """
        # Create a reminder 1 hour before the due date
        from datetime import timedelta
        reminder_time = due_date - timedelta(hours=1)

        # Generate a unique reminder ID
        import uuid
        reminder_id = hash(f"{task_id}_{reminder_time}") % 1000000

        await self.schedule_reminder(
            reminder_id=reminder_id,
            user_id=user_id,
            task_id=task_id,
            scheduled_time=reminder_time,
            channel="email",  # Default channel
            trigger_condition="before_due_date"
        )

    async def reschedule_reminder_for_task(self, task_id: int, new_due_date: datetime):
        """
        Reschedule existing reminders for a task based on new due date.

        Args:
            task_id: ID of the task to reschedule reminders for
            new_due_date: The new due date for the task
        """
        from datetime import timedelta

        # Find existing reminders for this task
        reminders_to_update = [
            rid for rid, rinfo in self.pending_reminders.items()
            if rinfo['task_id'] == task_id
        ]

        for reminder_id in reminders_to_update:
            old_reminder = self.pending_reminders[reminder_id]

            # Calculate new reminder time (e.g., 1 hour before new due date)
            new_reminder_time = new_due_date - timedelta(hours=1)

            # Update the reminder
            old_reminder['scheduled_time'] = new_reminder_time
            old_reminder['updated_at'] = datetime.now()

            logger.info(f"Rescheduled reminder {reminder_id} to {new_reminder_time}")

    async def _run_scheduler(self):
        """Internal method to run the scheduling loop."""
        while True:
            try:
                await self._check_and_process_reminders()
                await asyncio.sleep(30)  # Check every 30 seconds
            except Exception as e:
                logger.error(f"Error in reminder scheduler: {e}")
                await asyncio.sleep(60)  # Wait longer on error

    async def _check_and_process_reminders(self):
        """Check for reminders that are due and process them."""
        current_time = datetime.now()

        due_reminders = [
            (rid, rinfo) for rid, rinfo in self.pending_reminders.items()
            if rinfo['scheduled_time'] <= current_time
        ]

        for reminder_id, reminder_info in due_reminders:
            await self._trigger_reminder(reminder_info)
            # Remove the reminder after triggering
            del self.pending_reminders[reminder_id]

    async def _trigger_reminder(self, reminder_info: Dict[str, Any]):
        """
        Trigger a reminder by publishing a ReminderTriggeredEvent.

        Args:
            reminder_info: Information about the reminder to trigger
        """
        from ....backend.src.events.task_events import ReminderTriggeredEvent, ReminderTriggeredEventData

        event_data = ReminderTriggeredEventData(
            reminder_id=reminder_info['reminder_id'],
            task_id=reminder_info['task_id'],
            delivery_time=reminder_info['scheduled_time'],
            channel=reminder_info['channel']
        )

        triggered_event = ReminderTriggeredEvent(
            user_id=reminder_info['user_id'],
            data=event_data
        )

        # In a real implementation, we'd use Dapr to publish this event
        # For now, we'll just log it
        logger.info(f"Triggering reminder {reminder_info['reminder_id']} "
                   f"via {reminder_info['channel']} for task {reminder_info['task_id']}")


class MockDaprClient:
    """Mock Dapr client for testing and development when Dapr is not available."""

    def subscribe(self, topic: str, callback: Callable):
        """Mock subscribe method."""
        print(f"[MOCK] Subscribed to topic: {topic}")
        return True