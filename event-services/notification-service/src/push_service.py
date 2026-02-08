"""
Push notification service for the Todo Chatbot application.
Handles sending push notifications to users' devices.
"""

import asyncio
import os
from typing import Dict, Any
from firebase_admin import messaging, initialize_app, credentials


class PushService:
    """
    Service class for sending push notifications.
    """

    def __init__(self):
        """
        Initialize the push notification service with Firebase configuration.
        Configuration comes from environment variables.
        """
        self.firebase_creds_path = os.getenv("FIREBASE_CREDENTIALS_PATH")

        if self.firebase_creds_path:
            try:
                cred = credentials.Certificate(self.firebase_creds_path)
                initialize_app(cred)
                self.app_initialized = True
            except Exception as e:
                print(f"Error initializing Firebase: {str(e)}")
                self.app_initialized = False
        else:
            print("Warning: Firebase credentials not found. Push notifications will be disabled.")
            self.app_initialized = False

    async def send_push_notification(self, recipient_token: str, payload: Dict[str, Any]) -> bool:
        """
        Send a push notification to the specified device token.

        Args:
            recipient_token: The device token for the recipient
            payload: The notification payload containing title, body, and data

        Returns:
            bool: True if the push notification was sent successfully, False otherwise
        """
        if not self.app_initialized:
            print("Push service not configured: Firebase not initialized")
            return False

        try:
            # Extract notification data
            title = payload.get("title", "")
            body = payload.get("body", "")

            # Create message
            message = messaging.Message(
                notification=messaging.Notification(
                    title=title,
                    body=body
                ),
                data=payload.get("data", {}),
                token=recipient_token
            )

            # Send message
            response = messaging.send(message)
            print(f"Successfully sent message: {response}")
            return True

        except Exception as e:
            print(f"Error sending push notification to {recipient_token}: {str(e)}")
            return False

    async def send_bulk_push_notifications(self, recipient_tokens: list, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Send push notifications to multiple device tokens.

        Args:
            recipient_tokens: List of device tokens for recipients
            payload: The notification payload containing title, body, and data

        Returns:
            Dict[str, Any]: Results of the bulk notification operation
        """
        if not self.app_initialized:
            print("Push service not configured: Firebase not initialized")
            return {"success_count": 0, "failure_count": len(recipient_tokens)}

        try:
            # Extract notification data
            title = payload.get("title", "")
            body = payload.get("body", "")

            # Create messages
            messages = []
            for token in recipient_tokens:
                message = messaging.Message(
                    notification=messaging.Notification(
                        title=title,
                        body=body
                    ),
                    data=payload.get("data", {}),
                    token=token
                )
                messages.append(message)

            # Send messages in batches of 500 (Firebase limit)
            success_count = 0
            failure_count = 0

            for i in range(0, len(messages), 500):
                batch = messages[i:i+500]
                response = messaging.send_all(batch)

                success_count += response.success_count
                failure_count += response.failure_count

            result = {
                "success_count": success_count,
                "failure_count": failure_count
            }

            print(f"Bulk notification result: {result}")
            return result

        except Exception as e:
            print(f"Error sending bulk push notifications: {str(e)}")
            return {"success_count": 0, "failure_count": len(recipient_tokens)}

    async def subscribe_to_topic(self, device_token: str, topic: str) -> bool:
        """
        Subscribe a device to a topic for targeted notifications.

        Args:
            device_token: The device token to subscribe
            topic: The topic to subscribe to

        Returns:
            bool: True if subscription was successful, False otherwise
        """
        if not self.app_initialized:
            return False

        try:
            messaging.subscribe_to_topic(device_token, topic)
            print(f"Device {device_token} subscribed to topic {topic}")
            return True
        except Exception as e:
            print(f"Error subscribing device to topic: {str(e)}")
            return False

    async def unsubscribe_from_topic(self, device_token: str, topic: str) -> bool:
        """
        Unsubscribe a device from a topic.

        Args:
            device_token: The device token to unsubscribe
            topic: The topic to unsubscribe from

        Returns:
            bool: True if unsubscription was successful, False otherwise
        """
        if not self.app_initialized:
            return False

        try:
            messaging.unsubscribe_from_topic(device_token, topic)
            print(f"Device {device_token} unsubscribed from topic {topic}")
            return True
        except Exception as e:
            print(f"Error unsubscribing device from topic: {str(e)}")
            return False