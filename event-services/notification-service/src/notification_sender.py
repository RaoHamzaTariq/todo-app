"""
Notification sender service for the Todo Chatbot application.
Handles sending notifications through various channels (email, SMS, push notifications).
Integrates with Kafka for event-driven notifications and Dapr for service communication.
"""

import asyncio
import json
from datetime import datetime
from typing import Dict, Any, Optional
from dataclasses import dataclass

from dapr.aio.clients import DaprClient
from dapr.ext.grpc import App, InvokeMethodRequest
import aiokafka
from sqlmodel import Session

from backend.src.models.reminder_model import Reminder
from .email_service import EmailService
from .sms_service import SMSService
from .push_service import PushService


@dataclass
class NotificationMessage:
    """Data class for notification messages."""
    reminder_id: int
    user_id: str
    task_title: str
    reminder_datetime: datetime
    channel: str
    recipient: str


class NotificationSender:
    """
    Service class for sending notifications through various channels.
    Integrates with Kafka for event-driven notifications and Dapr for service communication.
    """

    def __init__(self, dapr_client: DaprClient, kafka_producer: aiokafka.AIOKafkaProducer):
        """
        Initialize the notification sender service.

        Args:
            dapr_client: Dapr client for service invocation
            kafka_producer: Kafka producer for sending notification events
        """
        self.dapr_client = dapr_client
        self.kafka_producer = kafka_producer
        self.email_service = EmailService()
        self.sms_service = SMSService()
        self.push_service = PushService()

    async def send_notification(self, reminder: Reminder, recipient: str) -> bool:
        """
        Send a notification for a reminder based on the specified channel.

        Args:
            reminder: The reminder object containing notification details
            recipient: The recipient's contact information (email, phone, etc.)

        Returns:
            bool: True if the notification was sent successfully, False otherwise
        """
        try:
            # Determine the channel to use
            channel = reminder.channel.lower()

            if channel == "email":
                return await self._send_email_notification(reminder, recipient)
            elif channel == "sms":
                return await self._send_sms_notification(reminder, recipient)
            elif channel == "push":
                return await self._send_push_notification(reminder, recipient)
            else:
                raise ValueError(f"Unsupported notification channel: {channel}")

        except Exception as e:
            print(f"Error sending notification for reminder {reminder.id}: {str(e)}")
            return False

    async def _send_email_notification(self, reminder: Reminder, recipient: str) -> bool:
        """
        Send an email notification for a reminder.

        Args:
            reminder: The reminder object containing notification details
            recipient: The recipient's email address

        Returns:
            bool: True if the email was sent successfully, False otherwise
        """
        subject = f"Task Reminder: {reminder.task.title}"
        body = f"""
        Hi there,

        This is a reminder for your task: {reminder.task.title}

        Scheduled for: {reminder.reminder_datetime.strftime('%Y-%m-%d %H:%M:%S')}

        Please complete this task as soon as possible.

        Best regards,
        Todo Chatbot Team
        """

        return await self.email_service.send_email(recipient, subject, body)

    async def _send_sms_notification(self, reminder: Reminder, recipient: str) -> bool:
        """
        Send an SMS notification for a reminder.

        Args:
            reminder: The reminder object containing notification details
            recipient: The recipient's phone number

        Returns:
            bool: True if the SMS was sent successfully, False otherwise
        """
        message = f"Reminder: {reminder.task.title} is due at {reminder.reminder_datetime.strftime('%H:%M')}."

        return await self.sms_service.send_sms(recipient, message)

    async def _send_push_notification(self, reminder: Reminder, recipient: str) -> bool:
        """
        Send a push notification for a reminder.

        Args:
            reminder: The reminder object containing notification details
            recipient: The recipient's device token

        Returns:
            bool: True if the push notification was sent successfully, False otherwise
        """
        payload = {
            "title": "Task Reminder",
            "body": f"{reminder.task.title} is due at {reminder.reminder_datetime.strftime('%H:%M')}",
            "data": {
                "task_id": reminder.task_id,
                "reminder_id": reminder.id
            }
        }

        return await self.push_service.send_push_notification(recipient, payload)

    async def process_reminder_event(self, reminder_data: Dict[str, Any]) -> bool:
        """
        Process a reminder event received from Kafka and send the appropriate notification.

        Args:
            reminder_data: Dictionary containing reminder information from Kafka event

        Returns:
            bool: True if the notification was processed successfully, False otherwise
        """
        try:
            # Create a notification message from the event data
            notification_msg = NotificationMessage(
                reminder_id=reminder_data['reminder_id'],
                user_id=reminder_data['user_id'],
                task_title=reminder_data['task_title'],
                reminder_datetime=datetime.fromisoformat(reminder_data['reminder_datetime']),
                channel=reminder_data['channel'],
                recipient=reminder_data['recipient']
            )

            # Fetch the reminder from the database to get full details
            # This would typically involve fetching from the database
            # For now, we'll simulate getting the reminder details
            reminder = await self._get_reminder_by_id(notification_msg.reminder_id)

            if not reminder:
                print(f"Could not find reminder with ID {notification_msg.reminder_id}")
                return False

            # Send the notification
            success = await self.send_notification(reminder, notification_msg.recipient)

            if success:
                # Update the reminder status to indicate it was sent
                await self._mark_reminder_as_sent(reminder.id)

                # Publish an event to indicate the notification was sent
                await self._publish_notification_sent_event(reminder.id, notification_msg.channel)

            return success

        except Exception as e:
            print(f"Error processing reminder event: {str(e)}")
            return False

    async def _get_reminder_by_id(self, reminder_id: int) -> Optional[Reminder]:
        """
        Fetch a reminder by its ID from the database.

        Args:
            reminder_id: The ID of the reminder to fetch

        Returns:
            Reminder: The reminder object if found, None otherwise
        """
        # This would normally involve a database lookup
        # For now, returning None to indicate implementation needed
        # In a real implementation, you would query the database
        # using an async session
        pass

    async def _mark_reminder_as_sent(self, reminder_id: int) -> bool:
        """
        Mark a reminder as sent in the database.

        Args:
            reminder_id: The ID of the reminder to update

        Returns:
            bool: True if the update was successful, False otherwise
        """
        # This would normally involve a database update
        # For now, returning True to indicate implementation needed
        # In a real implementation, you would update the database
        # using an async session
        return True

    async def _publish_notification_sent_event(self, reminder_id: int, channel: str) -> bool:
        """
        Publish an event indicating that a notification was sent.

        Args:
            reminder_id: The ID of the reminder for which notification was sent
            channel: The channel through which the notification was sent

        Returns:
            bool: True if the event was published successfully, False otherwise
        """
        event_data = {
            "reminder_id": reminder_id,
            "channel": channel,
            "timestamp": datetime.utcnow().isoformat(),
            "status": "sent"
        }

        try:
            # Serialize the event data
            serialized_data = json.dumps(event_data).encode('utf-8')

            # Publish the event to Kafka
            await self.kafka_producer.send_and_wait(
                'notification-events',
                serialized_data
            )

            return True
        except Exception as e:
            print(f"Error publishing notification sent event: {str(e)}")
            return False


class KafkaNotificationConsumer:
    """
    Kafka consumer for processing reminder notification events.
    """

    def __init__(self, kafka_consumer: aiokafka.AIOKafkaConsumer, notification_sender: NotificationSender):
        """
        Initialize the Kafka notification consumer.

        Args:
            kafka_consumer: Kafka consumer for reading reminder events
            notification_sender: Notification sender service to process events
        """
        self.kafka_consumer = kafka_consumer
        self.notification_sender = notification_sender

    async def start_consuming(self):
        """
        Start consuming reminder events from Kafka and processing them.
        """
        # Subscribe to the reminder topic
        await self.kafka_consumer.start()

        try:
            async for msg in self.kafka_consumer:
                try:
                    # Deserialize the message
                    reminder_data = json.loads(msg.value.decode('utf-8'))

                    # Process the reminder event
                    await self.notification_sender.process_reminder_event(reminder_data)

                except Exception as e:
                    print(f"Error processing message: {str(e)}")

                    # Optionally, send to a dead letter queue
                    await self._handle_failed_message(msg, e)

        finally:
            await self.kafka_consumer.stop()

    async def _handle_failed_message(self, msg: aiokafka.ConsumerRecord, error: Exception):
        """
        Handle a failed message by sending it to a dead letter queue or logging.

        Args:
            msg: The failed Kafka message
            error: The error that occurred during processing
        """
        print(f"Failed to process message: {error}")
        # In a real implementation, you might send to a dead letter queue
        # or implement retry logic


# Standalone function to initialize and run the notification service
async def run_notification_service():
    """
    Initialize and run the notification service.
    This function sets up Dapr client, Kafka consumer, and notification sender.
    """
    # Initialize Dapr client
    dapr_client = DaprClient()

    # Initialize Kafka producer
    kafka_producer = aiokafka.AIOKafkaProducer(
        bootstrap_servers=['localhost:9092'],  # This would come from config
        value_serializer=lambda x: json.dumps(x).encode('utf-8')
    )

    # Initialize Kafka consumer
    kafka_consumer = aiokafka.AIOKafkaConsumer(
        'reminder-notifications',
        bootstrap_servers=['localhost:9092'],  # This would come from config
        value_deserializer=lambda x: json.loads(x.decode('utf-8')),
        group_id='notification-service-group'
    )

    # Initialize notification sender
    notification_sender = NotificationSender(dapr_client, kafka_producer)

    # Initialize Kafka notification consumer
    notification_consumer = KafkaNotificationConsumer(kafka_consumer, notification_sender)

    # Start the Kafka producer
    await kafka_producer.start()

    # Start consuming messages
    await notification_consumer.start_consuming()


if __name__ == "__main__":
    # Run the notification service
    asyncio.run(run_notification_service())