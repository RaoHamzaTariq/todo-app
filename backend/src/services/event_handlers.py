"""
Event handlers for the Todo Chatbot application.
Handles various events in the system and coordinates with Kafka for event-driven architecture.
"""

import asyncio
import json
from datetime import datetime
from typing import Dict, Any, Optional
from sqlmodel import Session

from ..models.task_event_model import TaskEvent, TaskEventType, TaskEventCreate
from ..models.task_model import Task
from ..core.database import get_session
from ..services.kafka_producer import KafkaProducerService
from dapr.ext.grpc import App
from dapr.clients import DaprClient


class TaskEventHandler:
    """
    Service class for handling task-related events in an event-driven architecture.
    """

    def __init__(self, session: Session, kafka_producer: KafkaProducerService):
        """
        Initialize the task event handler.

        Args:
            session: Database session for database operations
            kafka_producer: Kafka producer for publishing events
        """
        self.session = session
        self.kafka_producer = kafka_producer

    async def handle_task_created(self, task: Task) -> bool:
        """
        Handle the task created event.

        Args:
            task: The task that was created

        Returns:
            bool: True if the event was handled successfully, False otherwise
        """
        try:
            # Create a task event record
            event_data = TaskEventCreate(
                event_type=TaskEventType.TASK_CREATED,
                user_id=task.user_id,
                task_id=task.id,
                payload={
                    "title": task.title,
                    "description": task.description,
                    "priority": task.priority,
                    "status": task.status,
                    "created_at": task.created_at.isoformat() if task.created_at else None,
                    "due_date": task.due_date.isoformat() if task.due_date else None
                }
            )

            # Save the event to the database
            task_event = TaskEvent(
                event_type=event_data.event_type,
                user_id=event_data.user_id,
                task_id=event_data.task_id,
                payload=json.dumps(event_data.payload)
            )
            self.session.add(task_event)
            self.session.commit()
            self.session.refresh(task_event)

            # Publish the event to Kafka
            event_message = {
                "event_id": task_event.id,
                "event_type": task_event.event_type.value,
                "user_id": task_event.user_id,
                "task_id": task_event.task_id,
                "payload": task_event.get_payload_data(),
                "timestamp": datetime.utcnow().isoformat()
            }

            await self.kafka_producer.publish_event("task-events", event_message)

            # Trigger any related processes (e.g., reminder scheduling if due date is set)
            if task.due_date:
                await self._schedule_reminder_if_needed(task)

            return True

        except Exception as e:
            print(f"Error handling task created event: {str(e)}")
            return False

    async def handle_task_updated(self, task: Task, old_task: Optional[Task] = None) -> bool:
        """
        Handle the task updated event.

        Args:
            task: The updated task
            old_task: The previous version of the task (optional)

        Returns:
            bool: True if the event was handled successfully, False otherwise
        """
        try:
            # Determine what changed
            changes = {}
            if old_task:
                if old_task.title != task.title:
                    changes['title'] = {'old': old_task.title, 'new': task.title}
                if old_task.description != task.description:
                    changes['description'] = {'old': old_task.description, 'new': task.description}
                if old_task.completed != task.completed:
                    changes['completed'] = {'old': old_task.completed, 'new': task.completed}
                if old_task.priority != task.priority:
                    changes['priority'] = {'old': old_task.priority, 'new': task.priority}
                if old_task.status != task.status:
                    changes['status'] = {'old': old_task.status, 'new': task.status}
                if old_task.due_date != task.due_date:
                    changes['due_date'] = {'old': old_task.due_date.isoformat() if old_task.due_date else None,
                                         'new': task.due_date.isoformat() if task.due_date else None}
            else:
                # If we don't have the old task, just record the current state
                changes = {
                    "title": task.title,
                    "description": task.description,
                    "completed": task.completed,
                    "priority": task.priority,
                    "status": task.status,
                    "due_date": task.due_date.isoformat() if task.due_date else None
                }

            # Create a task event record
            event_data = TaskEventCreate(
                event_type=TaskEventType.TASK_UPDATED,
                user_id=task.user_id,
                task_id=task.id,
                payload={
                    "changes": changes,
                    "updated_at": task.updated_at.isoformat() if task.updated_at else None
                }
            )

            # Save the event to the database
            task_event = TaskEvent(
                event_type=event_data.event_type,
                user_id=event_data.user_id,
                task_id=event_data.task_id,
                payload=json.dumps(event_data.payload)
            )
            self.session.add(task_event)
            self.session.commit()
            self.session.refresh(task_event)

            # Publish the event to Kafka
            event_message = {
                "event_id": task_event.id,
                "event_type": task_event.event_type.value,
                "user_id": task_event.user_id,
                "task_id": task_event.task_id,
                "payload": task_event.get_payload_data(),
                "timestamp": datetime.utcnow().isoformat()
            }

            await self.kafka_producer.publish_event("task-events", event_message)

            # Handle any special cases after update
            await self._handle_task_update_effects(task, old_task)

            return True

        except Exception as e:
            print(f"Error handling task updated event: {str(e)}")
            return False

    async def handle_task_deleted(self, user_id: str, task_id: int) -> bool:
        """
        Handle the task deleted event.

        Args:
            user_id: ID of the user who owned the task
            task_id: ID of the task that was deleted

        Returns:
            bool: True if the event was handled successfully, False otherwise
        """
        try:
            # Create a task event record
            event_data = TaskEventCreate(
                event_type=TaskEventType.TASK_DELETED,
                user_id=user_id,
                task_id=task_id,
                payload={
                    "deleted_at": datetime.utcnow().isoformat()
                }
            )

            # Save the event to the database
            task_event = TaskEvent(
                event_type=event_data.event_type,
                user_id=event_data.user_id,
                task_id=event_data.task_id,
                payload=json.dumps(event_data.payload)
            )
            self.session.add(task_event)
            self.session.commit()
            self.session.refresh(task_event)

            # Publish the event to Kafka
            event_message = {
                "event_id": task_event.id,
                "event_type": task_event.event_type.value,
                "user_id": task_event.user_id,
                "task_id": task_event.task_id,
                "payload": task_event.get_payload_data(),
                "timestamp": datetime.utcnow().isoformat()
            }

            await self.kafka_producer.publish_event("task-events", event_message)

            return True

        except Exception as e:
            print(f"Error handling task deleted event: {str(e)}")
            return False

    async def handle_task_completed(self, task: Task) -> bool:
        """
        Handle the task completed event.

        Args:
            task: The task that was completed

        Returns:
            bool: True if the event was handled successfully, False otherwise
        """
        try:
            # Create a task event record
            event_data = TaskEventCreate(
                event_type=TaskEventType.TASK_COMPLETED,
                user_id=task.user_id,
                task_id=task.id,
                payload={
                    "completed_at": task.updated_at.isoformat() if task.updated_at else None,
                    "title": task.title
                }
            )

            # Save the event to the database
            task_event = TaskEvent(
                event_type=event_data.event_type,
                user_id=event_data.user_id,
                task_id=event_data.task_id,
                payload=json.dumps(event_data.payload)
            )
            self.session.add(task_event)
            self.session.commit()
            self.session.refresh(task_event)

            # Publish the event to Kafka
            event_message = {
                "event_id": task_event.id,
                "event_type": task_event.event_type.value,
                "user_id": task_event.user_id,
                "task_id": task_event.task_id,
                "payload": task_event.get_payload_data(),
                "timestamp": datetime.utcnow().isoformat()
            }

            await self.kafka_producer.publish_event("task-events", event_message)

            return True

        except Exception as e:
            print(f"Error handling task completed event: {str(e)}")
            return False

    async def _schedule_reminder_if_needed(self, task: Task) -> bool:
        """
        Schedule a reminder if the task has a due date.

        Args:
            task: The task to check for due date

        Returns:
            bool: True if scheduling was attempted, False otherwise
        """
        if not task.due_date:
            return False

        try:
            # Create a reminder event
            event_data = TaskEventCreate(
                event_type=TaskEventType.REMINDER_SCHEDULED,
                user_id=task.user_id,
                task_id=task.id,
                payload={
                    "due_date": task.due_date.isoformat(),
                    "scheduled_at": datetime.utcnow().isoformat()
                }
            )

            # Save the event to the database
            task_event = TaskEvent(
                event_type=event_data.event_type,
                user_id=event_data.user_id,
                task_id=event_data.task_id,
                payload=json.dumps(event_data.payload)
            )
            self.session.add(task_event)
            self.session.commit()
            self.session.refresh(task_event)

            # Publish the event to Kafka for the reminder service to process
            event_message = {
                "event_id": task_event.id,
                "event_type": task_event.event_type.value,
                "user_id": task_event.user_id,
                "task_id": task_event.task_id,
                "payload": task_event.get_payload_data(),
                "timestamp": datetime.utcnow().isoformat()
            }

            await self.kafka_producer.publish_event("reminder-events", event_message)

            return True

        except Exception as e:
            print(f"Error scheduling reminder: {str(e)}")
            return False

    async def _handle_task_update_effects(self, task: Task, old_task: Optional[Task] = None) -> bool:
        """
        Handle any special effects of task updates (e.g., completing a recurring task creates a new instance).

        Args:
            task: The updated task
            old_task: The previous version of the task (optional)

        Returns:
            bool: True if effects were handled successfully, False otherwise
        """
        try:
            # If task was marked as completed and it's part of a recurring pattern,
            # trigger creation of the next instance
            if (old_task and not old_task.completed and task.completed and task.recurring_pattern):
                # This would trigger creation of the next recurring task instance
                event_data = TaskEventCreate(
                    event_type=TaskEventType.RECURRING_TASK_UPDATED,
                    user_id=task.user_id,
                    task_id=task.id,
                    related_entity_id=task.recurring_pattern.id,
                    related_entity_type="recurring_task",
                    payload={
                        "action": "generate_next_instance",
                        "completed_task_id": task.id,
                        "recurring_pattern_id": task.recurring_pattern.id
                    }
                )

                # Save the event to the database
                task_event = TaskEvent(
                    event_type=event_data.event_type,
                    user_id=event_data.user_id,
                    task_id=event_data.task_id,
                    related_entity_id=event_data.related_entity_id,
                    related_entity_type=event_data.related_entity_type,
                    payload=json.dumps(event_data.payload)
                )
                self.session.add(task_event)
                self.session.commit()
                self.session.refresh(task_event)

                # Publish the event to Kafka
                event_message = {
                    "event_id": task_event.id,
                    "event_type": task_event.event_type.value,
                    "user_id": task_event.user_id,
                    "task_id": task_event.task_id,
                    "related_entity_id": task_event.related_entity_id,
                    "related_entity_type": task_event.related_entity_type,
                    "payload": task_event.get_payload_data(),
                    "timestamp": datetime.utcnow().isoformat()
                }

                await self.kafka_producer.publish_event("recurring-task-events", event_message)

            return True

        except Exception as e:
            print(f"Error handling task update effects: {str(e)}")
            return False


class KafkaEventConsumer:
    """
    Kafka consumer for processing task events.
    """

    def __init__(self, kafka_consumer, event_handler: TaskEventHandler):
        """
        Initialize the Kafka event consumer.

        Args:
            kafka_consumer: Kafka consumer for reading events
            event_handler: Task event handler to process events
        """
        self.kafka_consumer = kafka_consumer
        self.event_handler = event_handler

    async def start_consuming(self):
        """
        Start consuming task events from Kafka and processing them.
        """
        # Subscribe to the task events topic
        await self.kafka_consumer.start()

        try:
            async for msg in self.kafka_consumer:
                try:
                    # Deserialize the message
                    event_data = json.loads(msg.value.decode('utf-8'))

                    # Process based on event type
                    event_type = event_data.get('event_type')

                    # Here we would route to appropriate handler based on event type
                    # For now, we'll just log the event
                    print(f"Received event: {event_type} for user {event_data.get('user_id')}")

                    # Mark message as processed
                    await self.kafka_consumer.commit()

                except Exception as e:
                    print(f"Error processing message: {str(e)}")
                    # Optionally, send to a dead letter queue
                    await self._handle_failed_message(msg, e)

        finally:
            await self.kafka_consumer.stop()

    async def _handle_failed_message(self, msg, error: Exception):
        """
        Handle a failed message by sending it to a dead letter queue or logging.

        Args:
            msg: The failed Kafka message
            error: The error that occurred during processing
        """
        print(f"Failed to process message: {error}")
        # In a real implementation, you might send to a dead letter queue
        # or implement retry logic


# Global instance for use in other parts of the application
# This would be initialized when the app starts
app_event_handler: Optional[TaskEventHandler] = None


def get_event_handler() -> Optional[TaskEventHandler]:
    """
    Get the global event handler instance.

    Returns:
        TaskEventHandler: The global event handler instance or None if not initialized
    """
    return app_event_handler


def init_event_handler(session: Session, kafka_producer: KafkaProducerService):
    """
    Initialize the global event handler instance.

    Args:
        session: Database session
        kafka_producer: Kafka producer service
    """
    global app_event_handler
    app_event_handler = TaskEventHandler(session, kafka_producer)