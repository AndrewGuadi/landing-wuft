import logging
from typing import Any, Dict

from flask import current_app
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

logger = logging.getLogger(__name__)


def send_email(payload: Dict[str, Any]) -> Dict[str, Any]:
    api_key = current_app.config.get("SENDGRID_API_KEY")
    sender = current_app.config.get("SENDGRID_SENDER")
    if not api_key or not sender:
        raise ValueError("SendGrid is not configured")

    to_email = payload.get("to")
    subject = payload.get("subject")
    content = payload.get("content")
    if not to_email or not subject or not content:
        raise ValueError("to, subject, and content are required")

    message = Mail(from_email=sender, to_emails=to_email, subject=subject, plain_text_content=content)
    client = SendGridAPIClient(api_key)
    response = client.send(message)
    logger.info("Email sent", extra={"status_code": response.status_code})
    return {
        "status": "sent",
        "provider": "sendgrid",
        "status_code": response.status_code,
    }
