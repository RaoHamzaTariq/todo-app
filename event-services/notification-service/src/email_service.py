"""
Email service for the Todo Chatbot application.
Handles sending email notifications to users.
"""

import asyncio
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
import os


class EmailService:
    """
    Service class for sending email notifications.
    """

    def __init__(self):
        """
        Initialize the email service with SMTP configuration.
        Configuration comes from environment variables.
        """
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.smtp_username = os.getenv("SMTP_USERNAME")
        self.smtp_password = os.getenv("SMTP_PASSWORD")
        self.from_email = os.getenv("FROM_EMAIL")

    async def send_email(self, recipient: str, subject: str, body: str) -> bool:
        """
        Send an email to the specified recipient.

        Args:
            recipient: The recipient's email address
            subject: The subject of the email
            body: The body content of the email

        Returns:
            bool: True if the email was sent successfully, False otherwise
        """
        if not self.smtp_username or not self.smtp_password or not self.from_email:
            print("Email service not configured: missing SMTP credentials")
            return False

        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.from_email
            msg['To'] = recipient
            msg['Subject'] = subject

            # Add body to email
            msg.attach(MIMEText(body, 'plain'))

            # Create SMTP session
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()  # Enable security
            server.login(self.smtp_username, self.smtp_password)

            # Send email
            text = msg.as_string()
            server.sendmail(self.from_email, recipient, text)
            server.quit()

            print(f"Email sent successfully to {recipient}")
            return True

        except Exception as e:
            print(f"Error sending email to {recipient}: {str(e)}")
            return False

    async def send_template_email(self, recipient: str, template_name: str, template_vars: dict) -> bool:
        """
        Send an email using a predefined template.

        Args:
            recipient: The recipient's email address
            template_name: The name of the email template to use
            template_vars: Variables to substitute in the template

        Returns:
            bool: True if the email was sent successfully, False otherwise
        """
        # In a real implementation, this would load a template and substitute variables
        # For now, we'll just send a basic reminder email
        subject = template_vars.get("subject", "Task Reminder")
        body = template_vars.get("body", "You have a task reminder.")

        return await self.send_email(recipient, subject, body)