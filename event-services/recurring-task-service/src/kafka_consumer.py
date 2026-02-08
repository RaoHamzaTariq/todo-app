"""
Kafka consumer service for recurring task events in the Todo Chatbot application.
"""

import asyncio
import json
from datetime import datetime, timedelta
from typing import Dict, Any, Callable
from loguru import logger

from ....backend.src.events.task_events import (
    EventBase, RecurringTaskCreatedEvent, RecurringTaskInstanceCreatedEvent,
    TaskCreatedEvent, TaskUpdatedEvent
)


class KafkaConsumerService:
    """
    Service class for consuming Kafka events using Dapr's pub/sub capabilities.
    Specifically handles recurring task events and manages task recurrence.
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
        self.recurring_task_manager = RecurringTaskManager()

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
                # Process recurring task events
                await self._process_recurring_task_events()

                # Wait before next polling cycle
                await asyncio.sleep(1)
            except Exception as e:
                logger.error(f"Error in consumption loop: {e}")
                await asyncio.sleep(5)  # Wait longer on error

    async def _process_recurring_task_events(self):
        """
        Process recurring task events from the queue.
        In a real implementation, this would use Dapr's pub/sub subscription.
        """
        # In a real implementation, Dapr would automatically call our subscription handlers
        # This is a simplified simulation of that process
        pass

    async def handle_recurring_task_created_event(self, event_data: Dict[str, Any]):
        """
        Handle a recurring task created event by registering it with the manager.

        Args:
            event_data: The event data containing recurring task information
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

            recurring_task_event = RecurringTaskCreatedEvent(**event_dict)

            logger.info(f"Processing recurring task created event for user {recurring_task_event.user_id}, "
                       f"recurring task {recurring_task_event.data.recurring_task_id}")

            # Register the recurring task with the manager
            await self.recurring_task_manager.register_recurring_task(
                recurring_task_id=recurring_task_event.data.recurring_task_id,
                user_id=recurring_task_event.user_id,
                title=recurring_task_event.data.title,
                description=recurring_task_event.data.description,
                frequency=recurring_task_event.data.frequency,
                interval=recurring_task_event.data.interval,
                end_date=recurring_task_event.data.end_date,
                active=recurring_task_event.data.active
            )

        except Exception as e:
            logger.error(f"Error handling recurring task created event: {e}")

    async def handle_task_updated_event(self, event_data: Dict[str, Any]):
        """
        Handle a task updated event by checking if it affects recurring task patterns.

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

            # Check if this is an update to a recurring task pattern
            # This would require additional metadata to determine if it's a recurring task
            logger.info(f"Received task update event for task {task_event.data.task_id}")

        except Exception as e:
            logger.error(f"Error handling task updated event: {e}")

    async def stop_consuming(self):
        """Stop consuming messages."""
        self._running = False
        logger.info("Stopped consuming messages")


class RecurringTaskManager:
    """
    Manager for handling recurring task patterns and generating new instances.
    """

    def __init__(self):
        self.recurring_patterns = {}
        self.scheduler_task = None

    async def register_recurring_task(self, recurring_task_id: int, user_id: str,
                                   title: str, description: str = None,
                                   frequency: str = "daily", interval: int = 1,
                                   end_date: datetime = None, active: bool = True):
        """
        Register a new recurring task pattern.

        Args:
            recurring_task_id: Unique ID for the recurring task
            user_id: ID of the user who owns the recurring task
            title: Title of the recurring task
            description: Description of the recurring task
            frequency: Frequency of recurrence ('daily', 'weekly', 'monthly', 'yearly')
            interval: Interval multiplier for frequency
            end_date: End date for the recurring task (None for indefinite)
            active: Whether the recurring pattern is active
        """
        pattern_info = {
            'recurring_task_id': recurring_task_id,
            'user_id': user_id,
            'title': title,
            'description': description,
            'frequency': frequency,
            'interval': interval,
            'end_date': end_date,
            'active': active,
            'last_generated': datetime.now(),
            'created_at': datetime.now()
        }

        self.recurring_patterns[recurring_task_id] = pattern_info
        logger.info(f"Registered recurring task pattern {recurring_task_id} with frequency {frequency}")

        # Start scheduler if not already running
        if self.scheduler_task is None or self.scheduler_task.done():
            self.scheduler_task = asyncio.create_task(self._run_scheduler())

    async def _run_scheduler(self):
        """Internal method to run the scheduling loop."""
        while True:
            try:
                await self._generate_recurring_tasks()
                await asyncio.sleep(3600)  # Check every hour
            except Exception as e:
                logger.error(f"Error in recurring task scheduler: {e}")
                await asyncio.sleep(3600)  # Wait longer on error

    async def _generate_recurring_tasks(self):
        """Generate new task instances based on recurring patterns."""
        current_time = datetime.now()

        for recurring_task_id, pattern_info in self.recurring_patterns.items():
            if not pattern_info['active']:
                continue

            # Check if we should generate a new task instance
            if self._should_generate_new_instance(pattern_info, current_time):
                try:
                    await self._generate_task_instance(pattern_info, current_time)

                    # Update last generated time
                    pattern_info['last_generated'] = current_time
                except Exception as e:
                    logger.error(f"Error generating task instance for pattern {recurring_task_id}: {e}")

    def _should_generate_new_instance(self, pattern_info: Dict[str, Any], current_time: datetime) -> bool:
        """
        Determine if a new task instance should be generated based on the pattern.

        Args:
            pattern_info: Information about the recurring pattern
            current_time: Current time for comparison

        Returns:
            bool: True if a new instance should be generated
        """
        # Don't generate if the pattern has ended
        if pattern_info['end_date'] and current_time > pattern_info['end_date']:
            return False

        # Calculate the expected next occurrence based on the pattern
        last_generated = pattern_info['last_generated']

        if pattern_info['frequency'] == 'daily':
            next_expected = last_generated + timedelta(days=pattern_info['interval'])
        elif pattern_info['frequency'] == 'weekly':
            next_expected = last_generated + timedelta(weeks=pattern_info['interval'])
        elif pattern_info['frequency'] == 'monthly':
            # This is a simplified approach - in reality, monthly calculations are more complex
            next_expected = last_generated + timedelta(days=30 * pattern_info['interval'])
        elif pattern_info['frequency'] == 'yearly':
            next_expected = last_generated + timedelta(days=365 * pattern_info['interval'])
        else:
            logger.error(f"Unknown frequency: {pattern_info['frequency']}")
            return False

        return current_time >= next_expected

    async def _generate_task_instance(self, pattern_info: Dict[str, Any], current_time: datetime):
        """
        Generate a new task instance from a recurring pattern.

        Args:
            pattern_info: Information about the recurring pattern
            current_time: Current time for the new instance
        """
        from ....backend.src.events.task_events import RecurringTaskInstanceCreatedEvent, RecurringTaskInstanceCreatedEventData

        # Generate a new task ID (in a real implementation, this would come from the database)
        import uuid
        new_task_id = hash(f"{pattern_info['recurring_task_id']}_{current_time.timestamp()}") % 1000000

        # Calculate due date based on pattern frequency
        # For now, we'll use the current time as the base
        new_due_date = self._calculate_next_due_date(pattern_info, current_time)

        event_data = RecurringTaskInstanceCreatedEventData(
            original_recurring_task_id=pattern_info['recurring_task_id'],
            new_task_id=new_task_id,
            due_date=new_due_date,
            is_template=False
        )

        instance_created_event = RecurringTaskInstanceCreatedEvent(
            user_id=pattern_info['user_id'],
            data=event_data
        )

        logger.info(f"Generated new task instance {new_task_id} from recurring pattern "
                   f"{pattern_info['recurring_task_id']}")

        # In a real implementation, we'd use Dapr to publish this event
        # For now, we'll just log it
        logger.info(f"Created recurring task instance event for user {pattern_info['user_id']}, "
                   f"new task {new_task_id}, from pattern {pattern_info['recurring_task_id']}")

    def _calculate_next_due_date(self, pattern_info: Dict[str, Any], current_time: datetime) -> datetime:
        """
        Calculate the due date for the next instance based on the pattern.

        Args:
            pattern_info: Information about the recurring pattern
            current_time: Current time to base calculation on

        Returns:
            datetime: Calculated due date for the new instance
        """
        # For simplicity, we'll use the current time as the base
        # In a real implementation, the due date might follow a more complex schedule
        return current_time


class MockDaprClient:
    """Mock Dapr client for testing and development when Dapr is not available."""

    def subscribe(self, topic: str, callback: Callable):
        """Mock subscribe method."""
        print(f"[MOCK] Subscribed to topic: {topic}")
        return True