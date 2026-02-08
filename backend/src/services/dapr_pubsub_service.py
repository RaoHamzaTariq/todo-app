"""
Dapr pub/sub integration service for publishing events in the Todo Chatbot application.
This service ensures all communication between services uses Dapr APIs as required.
"""

import asyncio
import json
from typing import Any, Optional
from loguru import logger

from ..events.task_events import AnyEvent


class DaprPubSubService:
    """
    Service class for integrating with Dapr's pub/sub building block.
    This ensures all communication between services uses Dapr APIs as required.
    """

    def __init__(self, dapr_client=None):
        """
        Initialize the Dapr pub/sub service.

        Args:
            dapr_client: Dapr client instance (will be injected by Dapr runtime)
        """
        self.dapr_client = dapr_client
        self._initialized = False
        self._pubsub_name = 'kafka-pubsub'  # As defined in Dapr component

    async def initialize(self):
        """Initialize the Dapr pub/sub service."""
        try:
            # In a Dapr environment, the client should be provided
            if self.dapr_client is None:
                # Import here to avoid dependency issues if Dapr is not available
                try:
                    from dapr.aio.clients import DaprClient
                    self.dapr_client = DaprClient()
                    logger.info("Dapr client initialized")
                except ImportError:
                    logger.warning("Dapr client not available. Using mock mode.")
                    self.dapr_client = MockDaprClient()

            self._initialized = True
            logger.info("DaprPubSubService initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize DaprPubSubService: {e}")
            raise

    async def publish_event(self, topic: str, event: AnyEvent) -> bool:
        """
        Publish an event to the specified topic using Dapr's pub/sub.

        Args:
            topic: The topic to publish to
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
                pubsub_name=self._pubsub_name,
                topic_name=topic,
                data=serialized_event,
                data_content_type='application/json'
            )

            logger.success(f"Successfully published event to topic '{topic}'")
            return True

        except Exception as e:
            logger.error(f"Failed to publish event to topic '{topic}': {e}")
            return False

    async def publish_multiple_events(self, topic: str, events: list) -> bool:
        """
        Publish multiple events to the same topic using Dapr's pub/sub.

        Args:
            topic: The topic to publish to
            events: List of event objects to publish

        Returns:
            bool: True if all events were published successfully, False otherwise
        """
        if not self._initialized:
            await self.initialize()

        success_count = 0
        for event in events:
            if await self.publish_event(topic, event):
                success_count += 1

        logger.info(f"Published {success_count}/{len(events)} events to topic '{topic}'")
        return success_count == len(events)

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

        print(f"[MOCK] Dapr published to {pubsub_name}:{topic_name}: {data}")


# Singleton instance for easy access throughout the application
_dapr_pubsub_service = None


async def get_dapr_pubsub_service() -> DaprPubSubService:
    """
    Get the singleton instance of the Dapr pub/sub service.

    Returns:
        DaprPubSubService: The singleton instance
    """
    global _dapr_pubsub_service
    if _dapr_pubsub_service is None:
        _dapr_pubsub_service = DaprPubSubService()
        await _dapr_pubsub_service.initialize()
    return _dapr_pubsub_service


# Utility functions for specific event types
async def publish_task_event(topic: str, event: AnyEvent) -> bool:
    """
    Publish a task-related event using the Dapr pub/sub service.

    Args:
        topic: The topic to publish to
        event: The event to publish

    Returns:
        bool: True if the event was published successfully, False otherwise
    """
    service = await get_dapr_pubsub_service()
    return await service.publish_event(topic, event)