from datetime import datetime
from typing import Any, Dict


def send_email(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "status": "stub",
        "provider": "email",
        "action": "send",
        "received": payload,
        "queued_at": datetime.utcnow().isoformat() + "Z",
    }
