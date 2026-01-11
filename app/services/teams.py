from datetime import datetime
from typing import Any, Dict


def send_notification(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "status": "stub",
        "provider": "microsoft_teams",
        "action": "notify",
        "received": payload,
        "sent_at": datetime.utcnow().isoformat() + "Z",
    }
