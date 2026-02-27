"""
ReminderProcessor for the Todo Chatbot application.
This service handles processing and sending of task reminders.
"""

import asyncio
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from loguru import logger

from backend.src.services.reminder_service import ReminderService
from backend.src.models.reminder_model import Reminder
from backend.src.events.task_events import ReminderTriggeredEvent, ReminderScheduledEvent
from backend.src.services.dapr_pubsub_service import publish_task_event


class ReminderProcessor:
    """
    Processor class for handling reminder processing and delivery.
    Monitors reminders and sends notifications when they're due.
    """

    def __init__(self, reminder_service: ReminderService):
        """
        Initialize the ReminderProcessor.

        Args:
            reminder_service: Service instance to handle reminder operations
        """
        self.reminder_service = reminder_service
        self._processor_thread = None
        self._stop_event = threading.Event()
        self._is_running = False

    async def start(self):
        """
        Start the reminder processor.
        """
        if self._is_running:
            logger.warning("ReminderProcessor already running")
            return

        self._is_running = True
        self._stop_event.clear()

        # Start processor in a separate thread
        self._processor_thread = threading.Thread(target=self._run_processor, daemon=True)
        self._processor_thread.start()

        logger.info("ReminderProcessor started")

    def stop(self):
        """
        Stop the reminder processor.
        """
        if not self._is_running:
            logger.warning("ReminderProcessor already stopped")
            return

        self._is_running = False
        self._stop_event.set()

        if self._processor_thread and self._processor_thread.is_alive():
            self._processor_thread.join(timeout=5.0)  # Wait up to 5 seconds

        logger.info("ReminderProcessor stopped")

    def _run_processor(self):
        """
        Internal method to run the processor loop in a separate thread.
        """
        logger.info("ReminderProcessor thread started")

        while not self._stop_event.is_set():
            try:
                # Process reminders
                processed_count = asyncio.run(self._process_reminders())

                if processed_count > 0:
                    logger.info(f"Processor processed {processed_count} reminders")

                # Sleep for a while before the next check
                # Use shorter sleep during development/testing
                sleep_interval = 60  # 1 minute

                # During development, we can use a shorter interval
                for _ in range(sleep_interval):
                    if self._stop_event.is_set():
                        break
                    self._stop_event.wait(1)  # Wait 1 second, check for stop signal

            except Exception as e:
                logger.error(f"Error in reminder processor: {e}")

                # Wait before retrying to avoid rapid error loops
                for _ in range(30):  # Wait 30 seconds before retry
                    if self._stop_event.is_set():
                        break
                    self._stop_event.wait(1)

        logger.info("ReminderProcessor thread stopped")

    async def _process_reminders(self) -> int:
        """
        Process all reminders that need sending.

        Returns:
            int: Number of reminders processed
        """
        try:
            return await self.reminder_service.process_reminders()
        except Exception as e:
            logger.error(f"Error processing reminders: {e}")
            return 0

    async def process_single_reminder(self, reminder: Reminder) -> bool:
        """
        Process a single reminder (send notification and mark as sent).

        Args:
            reminder: The reminder to process

        Returns:
            bool: True if the reminder was processed successfully, False otherwise
        """
        try:
            # Send the actual notification based on the channel
            await self._send_notification(reminder)

            # Mark the reminder as sent
            success = await self.reminder_service.mark_reminder_as_sent(reminder.id)

            if success:
                logger.info(f"Successfully processed reminder {reminder.id} for task {reminder.task_id}")

                # Publish event for the triggered reminder
                try:
                    event_data = {
                        "reminder_id": reminder.id,
                        "task_id": reminder.task_id,
                        "delivery_time": datetime.utcnow().isoformat(),
                        "channel": reminder.channel
                    }

                    event = ReminderTriggeredEvent(
                        user_id=reminder.user_id,
                        data=event_data
                    )

                    await publish_task_event("reminder-events", event)
                except Exception as e:
                    logger.error(f"Failed to publish reminder triggered event: {e}")

            return success

        except Exception as e:
            logger.error(f"Error processing single reminder {reminder.id}: {e}")
            return False

    async def _send_notification(self, reminder: Reminder):
        """
        Send the actual notification based on the reminder's channel.

        Args:
            reminder: The reminder to send notification for
        """
        # This would integrate with actual notification services in production
        if reminder.channel == "email":
            await self._send_email_notification(reminder)
        elif reminder.channel == "push":
            await self._send_push_notification(reminder)
        elif reminder.channel == "sms":
            await self._send_sms_notification(reminder)
        else:
            logger.warning(f"Unknown channel {reminder.channel} for reminder {reminder.id}")

    async def _send_email_notification(self, reminder: Reminder):
        """
        Send an email notification for the reminder.

        Args:
            reminder: The reminder to send email for
        """
        # In a real implementation, this would use an email service
        logger.info(f"Sending email reminder for task {reminder.task_id} to user {reminder.user_id}")

        # Simulate sending email
        # email_service.send_email(reminder.user_id, subject, body)

    async def _send_push_notification(self, reminder: Reminder):
        """
        Send a push notification for the reminder.

        Args:
            reminder: The reminder to send push notification for
        """
        # In a real implementation, this would use a push notification service
        logger.info(f"Sending push reminder for task {reminder.task_id} to user {reminder.user_id}")

        # Simulate sending push notification
        # push_service.send_push(reminder.user_id, message)

    async def _send_sms_notification(self, reminder: Reminder):
        """
        Send an SMS notification for the reminder.

        Args:
            reminder: The reminder to send SMS for
        """
        # In a real implementation, this would use an SMS service
        logger.info(f"Sending SMS reminder for task {reminder.task_id} to user {reminder.user_id}")

        # Simulate sending SMS
        # sms_service.send_sms(reminder.user_id, message)

    async def get_pending_reminders_info(self) -> Dict:
        """
        Get information about pending reminders.

        Returns:
            Dict: Information about pending reminders
        """
        try:
            pending_reminders = await self.reminder_service.get_overdue_reminders()

            info = {
                "total_pending": len(pending_reminders),
                "reminders": []
            }

            for reminder in pending_reminders:
                reminder_info = {
                    "id": reminder.id,
                    "task_id": reminder.task_id,
                    "user_id": reminder.user_id,
                    "scheduled_time": reminder.reminder_datetime.isoformat(),
                    "channel": reminder.channel,
                    "time_since_due": (datetime.utcnow() - reminder.reminder_datetime).total_seconds()
                }
                info["reminders"].append(reminder_info)

            return info
        except Exception as e:
            logger.error(f"Error getting pending reminders info: {e}")
            return {"total_pending": 0, "reminders": [], "error": str(e)}

    def is_running(self) -> bool:
        """
        Check if the processor is currently running.

        Returns:
            bool: True if the processor is running, False otherwise
        """
        return self._is_running


class StandaloneReminderProcessor:
    """
    Standalone version of the ReminderProcessor that can be used independently.
    """

    def __init__(self, db_session):
        """
        Initialize the standalone processor.

        Args:
            db_session: Database session to use
        """
        self.db_session = db_session
        self.reminder_service = ReminderService(db_session)
        self.processor = ReminderProcessor(self.reminder_service)

    async def start(self):
        """
        Start the standalone processor.
        """
        await self.processor.start()

    def stop(self):
        """
        Stop the standalone processor.
        """
        self.processor.stop()

    async def get_status(self) -> Dict:
        """
        Get the status of the processor.

        Returns:
            Dict: Status information
        """
        info = await self.processor.get_pending_reminders_info()
        info["is_running"] = self.processor.is_running()
        info["processor_type"] = "standalone"

        return info

    async def process_single_reminder_by_id(self, reminder_id: int) -> bool:
        """
        Process a single reminder by its ID.

        Args:
            reminder_id: ID of the reminder to process

        Returns:
            bool: True if the reminder was processed successfully, False otherwise
        """
        reminder = await self.reminder_service.get_reminder_by_id(reminder_id)
        if not reminder:
            logger.warning(f"Reminder with ID {reminder_id} not found")
            return False

        return await self.processor.process_single_reminder(reminder)


# Global processor instance for easy access
_processor_instance = None


async def get_reminder_processor(db_session) -> StandaloneReminderProcessor:
    """
    Get the singleton instance of the reminder processor.

    Args:
        db_session: Database session to use

    Returns:
        StandaloneReminderProcessor: The processor instance
    """
    global _processor_instance
    if _processor_instance is None:
        _processor_instance = StandaloneReminderProcessor(db_session)
    return _processor_instance