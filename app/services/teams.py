import logging
from typing import Any, Dict

import requests
from flask import current_app

logger = logging.getLogger(__name__)


def send_notification(payload: Dict[str, Any]) -> Dict[str, Any]:
    webhook_url = current_app.config.get("TEAMS_WEBHOOK_URL")
    if not webhook_url:
        raise ValueError("Teams webhook URL is not configured")

    message = payload.get("message")
    if not message:
        raise ValueError("message is required")

    response = requests.post(webhook_url, json={"text": message}, timeout=10)
    response.raise_for_status()
    logger.info("Teams notification sent", extra={"status_code": response.status_code})
    return {
        "status": "sent",
        "provider": "microsoft_teams",
        "status_code": response.status_code,
    }
