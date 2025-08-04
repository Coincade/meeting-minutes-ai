from typing import Type
from datetime import datetime

from crewai.tools import BaseTool
from pydantic import BaseModel, Field

try:
    from .gmail_utility import authenticate_gmail, create_message, create_draft
except ImportError:
    # Fallback for when running as standalone script
    import sys
    import os
    sys.path.append(os.path.dirname(__file__))
    from gmail_utility import authenticate_gmail, create_message, create_draft
# from agentops import record_tool

import os

class GmailToolInput(BaseModel):
    """Input schema for GmailTool."""

    body: str = Field(..., description="The body of the email to send.")


class GmailTool(BaseTool):
    name: str = "GmailTool"
    description: str = (
        "Clear description for what this tool is useful for, you agent will need this information to use it."
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
            draft = create_draft(service, "me", message)

            return f"Email draft created successfully! Draft id: {draft['id']}"
        except Exception as e:
            return f"Error sending email: {e}"