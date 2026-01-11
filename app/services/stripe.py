from datetime import datetime
from typing import Any, Dict


def create_checkout_session(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "status": "stub",
        "provider": "stripe",
        "action": "create_checkout_session",
        "received": payload,
        "created_at": datetime.utcnow().isoformat() + "Z",
    }


def handle_webhook(payload: Dict[str, Any], signature: str) -> Dict[str, Any]:
    return {
        "status": "stub",
        "provider": "stripe",
        "action": "webhook_received",
        "signature_present": bool(signature),
        "event": payload,
        "processed_at": datetime.utcnow().isoformat() + "Z",
    }
