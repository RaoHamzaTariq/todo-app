"""
SMS service for the Todo Chatbot application.
Handles sending SMS notifications to users.
"""

import asyncio
import os
from typing import Optional
from twilio.rest import Client


class SMSService:
    """
    Service class for sending SMS notifications.
    """

    def __init__(self):
        """
        Initialize the SMS service with Twilio configuration.
        Configuration comes from environment variables.
        """
        self.account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        self.auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        self.from_phone = os.getenv("TWILIO_FROM_PHONE")

        if self.account_sid and self.auth_token:
            self.client = Client(self.account_sid, self.auth_token)
        else:
            self.client = None
            print("Warning: Twilio credentials not found. SMS service will be disabled.")

    async def send_sms(self, recipient: str, message: str) -> bool:
        """
        Send an SMS to the specified recipient.

        Args:
            recipient: The recipient's phone number
            message: The message content to send

        Returns:
            bool: True if the SMS was sent successfully, False otherwise
        """
        if not self.client:
            print("SMS service not configured: missing Twilio credentials")
            return False

        try:
            # Remove any non-digit characters from phone number
            clean_recipient = ''.join(filter(str.isdigit, recipient))

            # Ensure the phone number starts with a country code
            if not clean_recipient.startswith('+'):
                # Assume US number if no country code provided
                clean_recipient = '+1' + clean_recipient

            message = self.client.messages.create(
                body=message,
                from_=self.from_phone,
                to=clean_recipient
            )

            print(f"SMS sent successfully to {clean_recipient}")
            return True

        except Exception as e:
            print(f"Error sending SMS to {recipient}: {str(e)}")
            return False

    async def send_sms_with_verification(self, recipient: str, message: str) -> bool:
        """
        Send an SMS with verification (if applicable with the provider).

        Args:
            recipient: The recipient's phone number
            message: The message content to send

        Returns:
            bool: True if the SMS was sent successfully, False otherwise
        """
        # In a real implementation, this might include verification steps
        # For now, just call the regular send_sms method
        return await self.send_sms(recipient, message)