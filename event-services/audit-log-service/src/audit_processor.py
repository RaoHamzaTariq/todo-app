"""
Audit logging service for the Todo Chatbot application.
Processes events and creates audit logs for compliance and monitoring.
"""

import asyncio
import json
import traceback
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
from dataclasses import dataclass

import aiokafka
from sqlmodel import Session
from dapr.ext.grpc import App
from dapr.clients import DaprClient


@dataclass
class AuditLogEntry:
    """Data class for audit log entries."""
    id: Optional[int] = None
    user_id: str = ""
    action: str = ""  # e.g., "task_created", "task_updated", "task_deleted"
    entity_type: str = ""  # e.g., "task", "reminder", "recurring_task"
    entity_id: Optional[int] = None
    old_values: Optional[Dict[str, Any]] = None  # Previous values before change
    new_values: Optional[Dict[str, Any]] = None  # New values after change
    timestamp: datetime = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    correlation_id: Optional[str] = None
    severity: str = "INFO"  # INFO, WARN, ERROR


class AuditLogService:
    """
    Service class for handling audit logging in the system.
    """

    def __init__(self, session: Session, kafka_consumer: aiokafka.AIOKafkaConsumer):
        """
        Initialize the audit log service.

        Args:
            session: Database session for storing audit logs
            kafka_consumer: Kafka consumer for receiving events to audit
        """
        self.session = session
        self.kafka_consumer = kafka_consumer
        self.dapr_client = DaprClient()

    async def process_event_for_audit(self, event_data: Dict[str, Any]) -> bool:
        """
        Process an incoming event and create an audit log entry.

        Args:
            event_data: Dictionary containing event information

        Returns:
            bool: True if the audit log was created successfully, False otherwise
        """
        try:
            # Extract event information
            event_type = event_data.get("event_type")
            user_id = event_data.get("user_id")
            task_id = event_data.get("task_id")
            payload = event_data.get("payload", {})
            timestamp_str = event_data.get("timestamp")
            timestamp = datetime.fromisoformat(timestamp_str) if timestamp_str else datetime.utcnow()

            # Map event types to audit actions
            action_map = {
                TaskEventType.TASK_CREATED.value: "task_created",
                TaskEventType.TASK_UPDATED.value: "task_updated",
                TaskEventType.TASK_DELETED.value: "task_deleted",
                TaskEventType.TASK_COMPLETED.value: "task_completed",
                TaskEventType.TASK_REOPENED.value: "task_reopened",
                TaskEventType.REMINDER_SCHEDULED.value: "reminder_scheduled",
                TaskEventType.REMINDER_SENT.value: "reminder_sent",
                TaskEventType.RECURRING_TASK_CREATED.value: "recurring_task_created",
                TaskEventType.RECURRING_TASK_UPDATED.value: "recurring_task_updated",
            }

            action = action_map.get(event_type, event_type)

            # Determine severity based on event type
            severity = "INFO"
            if "error" in event_type.lower() or "failed" in str(payload).lower():
                severity = "ERROR"
            elif "delete" in event_type.lower():
                severity = "WARN"

            # Create audit log entry
            audit_entry = AuditLogEntry(
                user_id=user_id or "",
                action=action,
                entity_type="task",
                entity_id=task_id,
                new_values=payload,
                timestamp=timestamp,
                severity=severity
            )

            # Store the audit log entry
            success = await self.store_audit_log(audit_entry)

            if success:
                print(f"Audit log created for event: {action} by user {user_id}")
            else:
                print(f"Failed to create audit log for event: {action}")

            return success

        except Exception as e:
            print(f"Error processing event for audit: {str(e)}")
            traceback.print_exc()
            return False

    async def store_audit_log(self, audit_entry: AuditLogEntry) -> bool:
        """
        Store an audit log entry in the database.

        Args:
            audit_entry: The audit log entry to store

        Returns:
            bool: True if the audit log was stored successfully, False otherwise
        """
        try:
            # In a real implementation, we would store this in an audit log table
            # For now, we'll just log to console
            log_entry = {
                "user_id": audit_entry.user_id,
                "action": audit_entry.action,
                "entity_type": audit_entry.entity_type,
                "entity_id": audit_entry.entity_id,
                "timestamp": audit_entry.timestamp.isoformat(),
                "severity": audit_entry.severity,
                "details": {
                    "new_values": audit_entry.new_values,
                    "old_values": audit_entry.old_values
                }
            }

            # Print to simulate storing in a log
            print(f"[AUDIT LOG] {audit_entry.severity}: {log_entry}")

            # In a real implementation, we would save this to an audit table
            # await self.session.add(AuditLog(...))
            # await self.session.commit()

            return True

        except Exception as e:
            print(f"Error storing audit log: {str(e)}")
            traceback.print_exc()
            return False

    async def get_audit_logs(self, user_id: str, action: Optional[str] = None,
                           start_date: Optional[datetime] = None,
                           end_date: Optional[datetime] = None,
                           limit: int = 100, offset: int = 0) -> List[AuditLogEntry]:
        """
        Retrieve audit logs with optional filters.

        Args:
            user_id: Filter by user ID
            action: Filter by action type
            start_date: Filter by start date
            end_date: Filter by end date
            limit: Maximum number of logs to return
            offset: Number of logs to skip

        Returns:
            List[AuditLogEntry]: List of audit log entries
        """
        try:
            # In a real implementation, we would query an audit log table
            # For now, we'll return an empty list
            print(f"Retrieving audit logs for user {user_id}")
            return []

        except Exception as e:
            print(f"Error retrieving audit logs: {str(e)}")
            traceback.print_exc()
            return []

    async def get_user_activity_summary(self, user_id: str, days: int = 30) -> Dict[str, Any]:
        """
        Get a summary of user activity for compliance reporting.

        Args:
            user_id: The user ID to get activity for
            days: Number of days to look back

        Returns:
            Dict[str, Any]: Summary of user activity
        """
        try:
            start_date = datetime.utcnow() - timedelta(days=days)

            # In a real implementation, we would query the audit log table
            # For now, we'll return a mock summary
            summary = {
                "user_id": user_id,
                "period_start": start_date.isoformat(),
                "period_end": datetime.utcnow().isoformat(),
                "total_events": 0,
                "event_types": {},
                "critical_events": 0,
                "last_activity": None
            }

            print(f"Returning activity summary for user {user_id}")
            return summary

        except Exception as e:
            print(f"Error getting user activity summary: {str(e)}")
            traceback.print_exc()
            return {}

    async def start_processing_events(self):
        """
        Start processing events from Kafka for audit logging.
        """
        print("Starting audit log service...")

        # Subscribe to the events topic
        await self.kafka_consumer.start()

        try:
            async for msg in self.kafka_consumer:
                try:
                    # Deserialize the message
                    event_data = json.loads(msg.value.decode('utf-8'))

                    # Process the event for auditing
                    await self.process_event_for_audit(event_data)

                    # Mark message as processed
                    await self.kafka_consumer.commit()

                except Exception as e:
                    print(f"Error processing audit event: {str(e)}")
                    traceback.print_exc()
                    # Optionally, send to a dead letter queue
                    await self._handle_failed_message(msg, e)

        except Exception as e:
            print(f"Error in audit log consumer loop: {str(e)}")
            traceback.print_exc()
        finally:
            await self.kafka_consumer.stop()

    async def _handle_failed_message(self, msg, error: Exception):
        """
        Handle a failed message by sending it to a dead letter queue or logging.

        Args:
            msg: The failed Kafka message
            error: The error that occurred during processing
        """
        print(f"Failed to process audit message: {error}")
        # In a real implementation, you might send to a dead letter queue
        # or implement retry logic


class KafkaAuditConsumer:
    """
    Kafka consumer specifically for audit logging.
    """

    def __init__(self, kafka_consumer: aiokafka.AIOKafkaConsumer, audit_service: AuditLogService):
        """
        Initialize the Kafka audit consumer.

        Args:
            kafka_consumer: Kafka consumer for reading events
            audit_service: Audit log service to process events
        """
        self.kafka_consumer = kafka_consumer
        self.audit_service = audit_service

    async def start_consuming(self):
        """
        Start consuming events from Kafka for audit logging.
        """
        print("Audit consumer starting...")

        # Subscribe to the events topic
        await self.kafka_consumer.start()

        try:
            async for msg in self.kafka_consumer:
                try:
                    # Deserialize the message
                    event_data = json.loads(msg.value.decode('utf-8'))

                    # Process the event for auditing
                    await self.audit_service.process_event_for_audit(event_data)

                    # Mark message as processed
                    await self.kafka_consumer.commit()

                except Exception as e:
                    print(f"Error processing audit event: {str(e)}")
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
        print(f"Failed to process audit message: {error}")
        # In a real implementation, you might send to a dead letter queue
        # or implement retry logic


# Standalone function to initialize and run the audit service
async def run_audit_service():
    """
    Initialize and run the audit service.
    This function sets up Kafka consumer and audit service.
    """
    # Initialize Kafka consumer
    kafka_consumer = aiokafka.AIOKafkaConsumer(
        'task-events', 'reminder-events', 'recurring-task-events',  # Listen to multiple event topics
        bootstrap_servers=['localhost:9092'],  # This would come from config
        value_deserializer=lambda x: json.loads(x.decode('utf-8')),
        group_id='audit-service-group',
        enable_auto_commit=False
    )

    # Initialize database session
    # This is a simplified initialization - in reality, you'd want to manage sessions properly
    from backend.src.app.database import engine
    session = Session(engine)

    # Initialize audit service
    audit_service = AuditLogService(session, kafka_consumer)

    # Initialize Kafka audit consumer
    audit_consumer = KafkaAuditConsumer(kafka_consumer, audit_service)

    # Start consuming messages
    await audit_consumer.start_consuming()


if __name__ == "__main__":
    # Run the audit service
    asyncio.run(run_audit_service())