from flask import current_app


def send_placeholder_email(subject: str, recipient: str) -> None:
    current_app.logger.info(
        "Placeholder email sent to %s with subject: %s",
        recipient,
        subject,
    )
