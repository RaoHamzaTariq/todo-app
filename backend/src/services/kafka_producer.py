"""
Kafka producer service for publishing task events in the Todo Chatbot application.
"""

import asyncio
import json
from typing import Any
from loguru import logger

from ..events.task_events import AnyEvent


class KafkaProducerService:
    """
    Service class for producing Kafka events using Dapr's pub/sub capabilities.
    """

    def __init__(self, dapr_client=None):
        """
        Initialize the Kafka producer service.

        Args:
            dapr_client: Dapr client instance (will be injected by Dapr runtime)
        """
        self.dapr_client = dapr_client
        self._initialized = False

    async def initialize(self):
        """Initialize the Kafka producer service."""
        try:
            # In a Dapr environment, the client will be provided
            if self.dapr_client is None:
                # Import here to avoid dependency issues if Dapr is not available
                try:
                    from dapr.aio.clients import DaprClient
                    self.dapr_client = DaprClient()
                except ImportError:
                    logger.warning("Dapr client not available. Using mock mode.")
                    self.dapr_client = MockDaprClient()

            self._initialized = True
            logger.info("KafkaProducerService initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize KafkaProducerService: {e}")
            raise

    async def publish_event(self, topic: str, event: AnyEvent) -> bool:
        """
        Publish an event to the specified Kafka topic.

        Args:
            topic: The Kafka topic to publish to
            event: The event object to publish

        Returns:
            bool: True if the event was published successfully, False otherwise
        """
        if not self._initialized:
            await self.initialize()

        try:
            # Serialize the event to JSON
            event_data = event.dict()
            serialized_event = json.dumps(event_data, default=str)

            logger.info(f"Publishing event to topic '{topic}': {event.event_type} for user {event.user_id}")

            # Publish the event using Dapr's pub/sub
            await self.dapr_client.publish_event(
                pubsub_name='kafka-pubsub',
                topic_name=topic,
                data=serialized_event,
                data_content_type='application/json'
            )

            logger.success(f"Successfully published event to topic '{topic}'")
            return True

        except Exception as e:
            logger.error(f"Failed to publish event to topic '{topic}': {e}")
            return False

    async def publish_task_created(self, task_id: int, user_id: str, title: str,
                                  description: str = None, due_date: str = None,
                                  priority: str = "medium", tags: list = None,
                                  status: str = "pending", correlation_id: str = None) -> bool:
        """
        Publish a TaskCreatedEvent.

        Args:
            task_id: The ID of the created task
            user_id: The ID of the user who created the task
            title: The title of the task
            description: The description of the task
            due_date: The due date of the task
            priority: The priority of the task
            tags: List of tags for the task
            status: The status of the task
            correlation_id: Optional correlation ID for tracing

        Returns:
            bool: True if the event was published successfully, False otherwise
        """
        from ..events.task_events import TaskCreatedEvent, TaskCreatedEventData, TaskPriority, TaskStatus

        event_data = TaskCreatedEventData(
            task_id=task_id,
            title=title,
            description=description,
            due_date=due_date,
            priority=TaskPriority(priority.lower()),
            tags=tags or [],
            status=TaskStatus(status.lower().replace(" ", "-")),
        )

        event = TaskCreatedEvent(
            user_id=user_id,
            correlation_id=correlation_id,
            data=event_data
        )

        return await self.publish_event("task-events", event)

    async def publish_task_updated(self, task_id: int, user_id: str,
                                  changes: dict, updated_fields: list,
                                  correlation_id: str = None) -> bool:
        """
        Publish a TaskUpdatedEvent.

        Args:
            task_id: The ID of the updated task
            user_id: The ID of the user who updated the task
            changes: Dictionary of field changes
            updated_fields: List of fields that were updated
            correlation_id: Optional correlation ID for tracing

        Returns:
            bool: True if the event was published successfully, False otherwise
        """
        from ..events.task_events import TaskUpdatedEvent, TaskUpdatedEventData, TaskUpdatedFieldChange

        # Convert changes to the expected format
        field_changes = {}
        for field_name, change_data in changes.items():
            field_changes[field_name] = TaskUpdatedFieldChange(
                old_value=change_data.get('old_value'),
                new_value=change_data.get('new_value')
            )

        event_data = TaskUpdatedEventData(
            task_id=task_id,
            changes=field_changes,
            updated_fields=updated_fields
        )

        event = TaskUpdatedEvent(
            user_id=user_id,
            correlation_id=correlation_id,
            data=event_data
        )

        return await self.publish_event("task-events", event)

    async def publish_recurring_task_created(self, recurring_task_id: int, user_id: str,
                                           title: str, description: str = None,
                                           frequency: str = "daily", interval: int = 1,
                                           end_date: str = None, active: bool = True,
                                           correlation_id: str = None) -> bool:
        """
        Publish a RecurringTaskCreatedEvent.

        Args:
            recurring_task_id: The ID of the recurring task
            user_id: The ID of the user who created the recurring task
            title: The title of the recurring task
            description: The description of the recurring task
            frequency: The frequency of recurrence
            interval: The interval for recurrence
            end_date: The end date for recurrence
            active: Whether the recurring task is active
            correlation_id: Optional correlation ID for tracing

        Returns:
            bool: True if the event was published successfully, False otherwise
        """
        from ..events.task_events import RecurringTaskCreatedEvent, RecurringTaskCreatedEventData

        event_data = RecurringTaskCreatedEventData(
            recurring_task_id=recurring_task_id,
            title=title,
            description=description,
            frequency=frequency,
            interval=interval,
            end_date=end_date,
            active=active
        )

        event = RecurringTaskCreatedEvent(
            user_id=user_id,
            correlation_id=correlation_id,
            data=event_data
        )

        return await self.publish_event("recurring-task-events", event)

    async def publish_reminder_scheduled(self, reminder_id: int, user_id: str,
                                        task_id: int, scheduled_time: str,
                                        channel: str = "email",
                                        trigger_condition: str = "before_due_date",
                                        correlation_id: str = None) -> bool:
        """
        Publish a ReminderScheduledEvent.

        Args:
            reminder_id: The ID of the scheduled reminder
            user_id: The ID of the user the reminder is for
            task_id: The ID of the task the reminder is for
            scheduled_time: When the reminder should be sent
            channel: The channel to send the reminder (email, push, sms)
            trigger_condition: The condition that triggers the reminder
            correlation_id: Optional correlation ID for tracing

        Returns:
            bool: True if the event was published successfully, False otherwise
        """
        from ..events.task_events import ReminderScheduledEvent, ReminderScheduledEventData

        event_data = ReminderScheduledEventData(
            reminder_id=reminder_id,
            task_id=task_id,
            scheduled_time=scheduled_time,
            channel=channel,
            trigger_condition=trigger_condition
        )

        event = ReminderScheduledEvent(
            user_id=user_id,
            correlation_id=correlation_id,
            data=event_data
        )

        return await self.publish_event("reminder-events", event)

    async def close(self):
        """Close the Dapr client connection."""
        if hasattr(self.dapr_client, 'close'):
            await self.dapr_client.close()


class MockDaprClient:
    """Mock Dapr client for testing and development when Dapr is not available."""

    async def publish_event(self, pubsub_name: str, topic_name: str,
                           data: Any, data_content_type: str = None):
        """Mock publish event method."""
        import random
        # Simulate occasional failures for testing
        if random.random() < 0.05:  # 5% failure rate
            raise Exception("Simulated publishing failure")

        print(f"[MOCK] Published to {pubsub_name}:{topic_name}: {data}")