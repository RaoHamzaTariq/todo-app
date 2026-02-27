"""
RecurringTaskScheduler for the Todo Chatbot application.
This service handles scheduling and execution of recurring task generation.
"""

import asyncio
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from loguru import logger

from backend.src.services.recurring_task_service import RecurringTaskService
from backend.src.models.recurring_task_model import RecurringTask
from backend.src.events.task_events import (
    RecurringTaskInstanceCreatedEvent, RecurringTaskInstanceCreatedEventData
)
from backend.src.services.dapr_pubsub_service import publish_task_event


class RecurringTaskScheduler:
    """
    Scheduler class for handling recurring task generation.
    Monitors recurring task patterns and creates new task instances based on their schedule.
    """

    def __init__(self, recurring_task_service: RecurringTaskService):
        """
        Initialize the RecurringTaskScheduler.

        Args:
            recurring_task_service: Service instance to handle recurring task operations
        """
        self.recurring_task_service = recurring_task_service
        self._scheduler_thread = None
        self._stop_event = threading.Event()
        self._is_running = False

    async def start(self):
        """
        Start the recurring task scheduler.
        """
        if self._is_running:
            logger.warning("RecurringTaskScheduler already running")
            return

        self._is_running = True
        self._stop_event.clear()

        # Start scheduler in a separate thread
        self._scheduler_thread = threading.Thread(target=self._run_scheduler, daemon=True)
        self._scheduler_thread.start()

        logger.info("RecurringTaskScheduler started")

    def stop(self):
        """
        Stop the recurring task scheduler.
        """
        if not self._is_running:
            logger.warning("RecurringTaskScheduler already stopped")
            return

        self._is_running = False
        self._stop_event.set()

        if self._scheduler_thread and self._scheduler_thread.is_alive():
            self._scheduler_thread.join(timeout=5.0)  # Wait up to 5 seconds

        logger.info("RecurringTaskScheduler stopped")

    def _run_scheduler(self):
        """
        Internal method to run the scheduler loop in a separate thread.
        """
        logger.info("RecurringTaskScheduler thread started")

        while not self._stop_event.is_set():
            try:
                # Process recurring tasks
                generated_count = asyncio.run(self._process_recurring_tasks())

                if generated_count > 0:
                    logger.info(f"Scheduler processed {generated_count} recurring task instances")

                # Sleep for a while before the next check
                # Use shorter sleep during development/testing
                sleep_interval = 300  # 5 minutes in production

                # During development, we can use a shorter interval
                for _ in range(sleep_interval):
                    if self._stop_event.is_set():
                        break
                    self._stop_event.wait(1)  # Wait 1 second, check for stop signal

            except Exception as e:
                logger.error(f"Error in recurring task scheduler: {e}")

                # Wait before retrying to avoid rapid error loops
                for _ in range(60):  # Wait 60 seconds before retry
                    if self._stop_event.is_set():
                        break
                    self._stop_event.wait(1)

        logger.info("RecurringTaskScheduler thread stopped")

    async def _process_recurring_tasks(self) -> int:
        """
        Process all active recurring tasks and generate new instances if needed.

        Returns:
            int: Number of task instances generated
        """
        try:
            return await self.recurring_task_service.process_recurring_tasks()
        except Exception as e:
            logger.error(f"Error processing recurring tasks: {e}")
            return 0

    async def schedule_recurring_task_creation(self, recurring_task: RecurringTask):
        """
        Schedule the creation of a recurring task pattern.

        Args:
            recurring_task: The recurring task pattern to schedule
        """
        logger.info(f"Scheduling recurring task creation: {recurring_task.title}")

        # In a real implementation, we might want to schedule specific events
        # For now, this is more of a placeholder for future enhancement

    async def get_scheduled_tasks_info(self) -> Dict:
        """
        Get information about scheduled recurring tasks.

        Returns:
            Dict: Information about scheduled tasks
        """
        active_tasks = await self.recurring_task_service.get_active_recurring_tasks()

        info = {
            "total_active_patterns": len(active_tasks),
            "patterns": []
        }

        for task in active_tasks:
            pattern_info = {
                "id": task.id,
                "title": task.title,
                "frequency": task.frequency,
                "interval": task.interval,
                "end_date": task.end_date.isoformat() if task.end_date else None,
                "next_occurrence_calculated": task.calculate_next_occurrence(datetime.utcnow()).isoformat()
                                             if task.calculate_next_occurrence(datetime.utcnow()) else None
            }
            info["patterns"].append(pattern_info)

        return info

    def is_running(self) -> bool:
        """
        Check if the scheduler is currently running.

        Returns:
            bool: True if the scheduler is running, False otherwise
        """
        return self._is_running


class StandaloneRecurringTaskScheduler:
    """
    Standalone version of the RecurringTaskScheduler that can be used independently.
    """

    def __init__(self, db_session):
        """
        Initialize the standalone scheduler.

        Args:
            db_session: Database session to use
        """
        self.db_session = db_session
        self.recurring_task_service = RecurringTaskService(db_session)
        self.scheduler = RecurringTaskScheduler(self.recurring_task_service)

    async def start(self):
        """
        Start the standalone scheduler.
        """
        await self.scheduler.start()

    def stop(self):
        """
        Stop the standalone scheduler.
        """
        self.scheduler.stop()

    async def get_status(self) -> Dict:
        """
        Get the status of the scheduler.

        Returns:
            Dict: Status information
        """
        info = await self.scheduler.get_scheduled_tasks_info()
        info["is_running"] = self.scheduler.is_running()
        info["scheduler_type"] = "standalone"

        return info


# Global scheduler instance for easy access
_scheduler_instance = None


async def get_recurring_task_scheduler(db_session) -> StandaloneRecurringTaskScheduler:
    """
    Get the singleton instance of the recurring task scheduler.

    Args:
        db_session: Database session to use

    Returns:
        StandaloneRecurringTaskScheduler: The scheduler instance
    """
    global _scheduler_instance
    if _scheduler_instance is None:
        _scheduler_instance = StandaloneRecurringTaskScheduler(db_session)
    return _scheduler_instance