from typing import Type
from datetime import datetime

from crewai.tools import BaseTool
from pydantic import BaseModel, Field

from .gmail_utility import authenticate_gmail, create_message, send_message
# from agentops import record_tool

import os

class GmailToolInput(BaseModel):
    """Input schema for GmailTool."""

    body: str = Field(..., description="The body of the email to send directly.")


class GmailTool(BaseTool):
    name: str = "GmailTool"
    description: str = (
        "A tool to send emails directly via Gmail API. Use this to send meeting minutes and other emails to recipients."
    )
    args_schema: Type[BaseModel] = GmailToolInput

    def _run(self, body: str) -> str:
        try:
            service = authenticate_gmail()

            sender = os.getenv("GMAIL_SENDER")
            to = os.getenv("GMAIL_RECIPIENT")
            current_date = datetime.now().strftime("%B %d, %Y")
            subject = f"Meeting Minutes - {current_date}"
            message_text = body

            message = create_message(sender, to, subject, message_text)
            sent_message = send_message(service, "me", message)

            return f"Email sent successfully! Message id: {sent_message['id']}"
        except Exception as e:
            return f"Error sending email: {e}"