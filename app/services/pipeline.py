from datetime import datetime
from typing import Any, Dict


def run_pipeline(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "status": "stub",
        "provider": "pipeline",
        "action": "run",
        "received": payload,
        "queued_at": datetime.utcnow().isoformat() + "Z",
    }
