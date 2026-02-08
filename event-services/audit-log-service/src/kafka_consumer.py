"""
Kafka consumer service for audit log events in the Todo Chatbot application.
"""

import asyncio
import json
from datetime import datetime
from typing import Dict, Any, Callable
from loguru import logger
import aiofiles
import os

from ....backend.src.events.task_events import (
    EventBase, AuditEvent, TaskCreatedEvent, TaskUpdatedEvent,
    RecurringTaskCreatedEvent, ReminderScheduledEvent
)


class KafkaConsumerService:
    """
    Service class for consuming Kafka events using Dapr's pub/sub capabilities.
    Specifically handles audit log events and stores them appropriately.
    """

    def __init__(self, dapr_client=None, log_file_path=None):
        """
        Initialize the Kafka consumer service.

        Args:
            dapr_client: Dapr client instance (will be injected by Dapr runtime)
            log_file_path: Path to store audit logs (defaults to ./audit.log)
        """
        self.dapr_client = dapr_client
        self.log_file_path = log_file_path or "./audit.log"
        self._initialized = False
        self._subscriptions = {}
        self._running = False
        self.audit_logger = AuditLogger(self.log_file_path)

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

            # Ensure log directory exists
            log_dir = os.path.dirname(self.log_file_path)
            if log_dir:
                os.makedirs(log_dir, exist_ok=True)

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
                # Process audit log events
                await self._process_audit_events()

                # Wait before next polling cycle
                await asyncio.sleep(1)
            except Exception as e:
                logger.error(f"Error in consumption loop: {e}")
                await asyncio.sleep(5)  # Wait longer on error

    async def _process_audit_events(self):
        """
        Process audit events from the queue.
        In a real implementation, this would use Dapr's pub/sub subscription.
        """
        # In a real implementation, Dapr would automatically call our subscription handlers
        # This is a simplified simulation of that process
        pass

    async def handle_task_created_event(self, event_data: Dict[str, Any]):
        """
        Handle a task created event by logging it to the audit trail.

        Args:
            event_data: The event data containing task creation information
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

            audit_entry = {
                'timestamp': datetime.now().isoformat(),
                'user_id': task_event.user_id,
                'action': 'task.created',
                'resource_id': str(task_event.data.task_id),
                'resource_type': 'task',
                'details': {
                    'title': task_event.data.title,
                    'description': task_event.data.description,
                    'priority': task_event.data.priority.value if hasattr(task_event.data.priority, 'value') else task_event.data.priority,
                    'status': task_event.data.status.value if hasattr(task_event.data.status, 'value') else task_event.data.status,
                    'due_date': task_event.data.due_date.isoformat() if task_event.data.due_date else None
                },
                'correlation_id': task_event.correlation_id
            }

            await self.audit_logger.log(audit_entry)

        except Exception as e:
            logger.error(f"Error handling task created event for audit: {e}")

    async def handle_task_updated_event(self, event_data: Dict[str, Any]):
        """
        Handle a task updated event by logging it to the audit trail.

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

            audit_entry = {
                'timestamp': datetime.now().isoformat(),
                'user_id': task_event.user_id,
                'action': 'task.updated',
                'resource_id': str(task_event.data.task_id),
                'resource_type': 'task',
                'details': {
                    'updated_fields': task_event.data.updated_fields,
                    'changes': {field: {
                        'old_value': change.old_value if hasattr(change, 'old_value') else change.get('old_value'),
                        'new_value': change.new_value if hasattr(change, 'new_value') else change.get('new_value')
                    } for field, change in task_event.data.changes.items()}
                },
                'correlation_id': task_event.correlation_id
            }

            await self.audit_logger.log(audit_entry)

        except Exception as e:
            logger.error(f"Error handling task updated event for audit: {e}")

    async def handle_recurring_task_created_event(self, event_data: Dict[str, Any]):
        """
        Handle a recurring task created event by logging it to the audit trail.

        Args:
            event_data: The event data containing recurring task creation information
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

            audit_entry = {
                'timestamp': datetime.now().isoformat(),
                'user_id': recurring_task_event.user_id,
                'action': 'recurring_task.created',
                'resource_id': str(recurring_task_event.data.recurring_task_id),
                'resource_type': 'recurring_task',
                'details': {
                    'title': recurring_task_event.data.title,
                    'description': recurring_task_event.data.description,
                    'frequency': recurring_task_event.data.frequency,
                    'interval': recurring_task_event.data.interval,
                    'end_date': recurring_task_event.data.end_date.isoformat() if recurring_task_event.data.end_date else None,
                    'active': recurring_task_event.data.active
                },
                'correlation_id': recurring_task_event.correlation_id
            }

            await self.audit_logger.log(audit_entry)

        except Exception as e:
            logger.error(f"Error handling recurring task created event for audit: {e}")

    async def handle_reminder_scheduled_event(self, event_data: Dict[str, Any]):
        """
        Handle a reminder scheduled event by logging it to the audit trail.

        Args:
            event_data: The event data containing reminder scheduling information
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

            audit_entry = {
                'timestamp': datetime.now().isoformat(),
                'user_id': reminder_event.user_id,
                'action': 'reminder.scheduled',
                'resource_id': str(reminder_event.data.reminder_id),
                'resource_type': 'reminder',
                'details': {
                    'task_id': reminder_event.data.task_id,
                    'scheduled_time': reminder_event.data.scheduled_time.isoformat() if isinstance(reminder_event.data.scheduled_time, datetime) else reminder_event.data.scheduled_time,
                    'channel': reminder_event.data.channel,
                    'trigger_condition': reminder_event.data.trigger_condition
                },
                'correlation_id': reminder_event.correlation_id
            }

            await self.audit_logger.log(audit_entry)

        except Exception as e:
            logger.error(f"Error handling reminder scheduled event for audit: {e}")

    async def handle_generic_event(self, event_data: Dict[str, Any]):
        """
        Handle any generic event by logging it to the audit trail.

        Args:
            event_data: The event data to audit
        """
        try:
            audit_entry = {
                'timestamp': datetime.now().isoformat(),
                'user_id': event_data.get('user_id', 'unknown'),
                'action': event_data.get('event_type', 'unknown'),
                'resource_id': 'unknown',
                'resource_type': 'generic',
                'details': event_data.get('data', {}),
                'correlation_id': event_data.get('correlation_id')
            }

            await self.audit_logger.log(audit_entry)

        except Exception as e:
            logger.error(f"Error handling generic event for audit: {e}")

    async def stop_consuming(self):
        """Stop consuming messages."""
        self._running = False
        logger.info("Stopped consuming messages")


class AuditLogger:
    """
    Logger for audit entries with file-based persistence.
    """

    def __init__(self, log_file_path: str):
        self.log_file_path = log_file_path
        self._lock = asyncio.Lock()

    async def log(self, entry: Dict[str, Any]):
        """
        Log an audit entry to the file.

        Args:
            entry: The audit entry to log
        """
        async with self._lock:
            try:
                # Convert entry to JSON and write to file
                json_line = json.dumps(entry) + '\n'

                async with aiofiles.open(self.log_file_path, 'a', encoding='utf-8') as f:
                    await f.write(json_line)

                logger.info(f"Audit log entry written: {entry['action']} for user {entry['user_id']}")
            except Exception as e:
                logger.error(f"Error writing audit log entry: {e}")

    async def get_logs(self, user_id: str = None, action: str = None, limit: int = 100) -> list:
        """
        Retrieve audit logs, optionally filtered by user or action.

        Args:
            user_id: Filter logs by user ID (optional)
            action: Filter logs by action type (optional)
            limit: Maximum number of logs to return (default 100)

        Returns:
            list: List of audit log entries
        """
        try:
            if not os.path.exists(self.log_file_path):
                return []

            logs = []
            async with aiofiles.open(self.log_file_path, 'r', encoding='utf-8') as f:
                lines = await f.readlines()
                # Process from newest to oldest, up to the limit
                for line in reversed(lines[-limit:]):
                    try:
                        entry = json.loads(line.strip())
                        # Apply filters
                        if user_id and entry.get('user_id') != user_id:
                            continue
                        if action and entry.get('action') != action:
                            continue
                        logs.append(entry)
                    except json.JSONDecodeError:
                        continue

            # Return in chronological order (oldest first)
            return list(reversed(logs))
        except Exception as e:
            logger.error(f"Error retrieving audit logs: {e}")
            return []

    async def clear_logs(self):
        """
        Clear all audit logs.
        """
        try:
            if os.path.exists(self.log_file_path):
                async with aiofiles.open(self.log_file_path, 'w') as f:
                    await f.write('')
                logger.info("Audit logs cleared")
        except Exception as e:
            logger.error(f"Error clearing audit logs: {e}")


class MockDaprClient:
    """Mock Dapr client for testing and development when Dapr is not available."""

    def subscribe(self, topic: str, callback: Callable):
        """Mock subscribe method."""
        print(f"[MOCK] Subscribed to topic: {topic}")
        return True