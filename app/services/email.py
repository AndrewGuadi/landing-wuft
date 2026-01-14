import logging
import smtplib
from email.message import EmailMessage
from typing import Any, Dict, Optional

from flask import current_app, render_template

logger = logging.getLogger(__name__)


def _get_smtp_config() -> Dict[str, Any]:
    config = current_app.config
    server = config.get("MAIL_SERVER")
    port = config.get("MAIL_PORT")
    username = config.get("MAIL_USERNAME")
    password = config.get("MAIL_PASSWORD")
    default_sender = config.get("MAIL_DEFAULT_SENDER")
    use_tls = config.get("MAIL_USE_TLS", True)
    if not server or not port or not username or not password or not default_sender:
        raise ValueError("SMTP email is not configured")
    return {
        "server": server,
        "port": port,
        "username": username,
        "password": password,
        "default_sender": default_sender,
        "use_tls": bool(use_tls),
    }


def _send_smtp_email(
    subject: str,
    recipient: str,
    text_body: str,
    html_body: Optional[str] = None,
    sender: Optional[str] = None,
) -> Dict[str, Any]:
    if not recipient or not subject or not text_body:
        raise ValueError("recipient, subject, and text_body are required")

    config = _get_smtp_config()
    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = sender or config["default_sender"]
    message["To"] = recipient
    message.set_content(text_body)
    if html_body:
        message.add_alternative(html_body, subtype="html")

    with smtplib.SMTP(config["server"], int(config["port"])) as smtp:
        if config["use_tls"]:
            smtp.starttls()
        smtp.login(config["username"], config["password"])
        smtp.send_message(message)

    logger.info("Email sent via SMTP", extra={"recipient": recipient})
    return {
        "status": "sent",
        "provider": "smtp",
    }


def send_email(payload: Dict[str, Any]) -> Dict[str, Any]:
    to_email = payload.get("to")
    subject = payload.get("subject")
    content = payload.get("content")
    html_content = payload.get("html")
    if not to_email or not subject or not content:
        raise ValueError("to, subject, and content are required")

    return _send_smtp_email(
        subject=subject,
        recipient=to_email,
        text_body=content,
        html_body=html_content,
    )


def send_sponsorship_thank_you(recipient: str, sponsor_tier: str) -> Dict[str, Any]:
    tier_label = sponsor_tier or "Sponsor"
    subject = "Thank you for sponsoring Wish Upon a Food Truck!"
    text_body = (
        "Thank you for sponsoring Wish Upon a Food Truck.\n"
        f"Sponsorship tier: {tier_label}\n\n"
        "We appreciate your generosity and support. We'll be in touch with next steps."
    )
    html_body = render_template(
        "email/sponsorship-thank-you.html",
        sponsor_tier=tier_label,
    )
    return _send_smtp_email(
        subject=subject,
        recipient=recipient,
        text_body=text_body,
        html_body=html_body,
    )
