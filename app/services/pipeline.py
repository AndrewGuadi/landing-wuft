import logging
from typing import Any, Dict

import requests
from flask import current_app

logger = logging.getLogger(__name__)


def run_pipeline(payload: Dict[str, Any]) -> Dict[str, Any]:
    api_url = current_app.config.get("PIPELINE_API_URL")
    api_token = current_app.config.get("PIPELINE_API_TOKEN")
    if not api_url or not api_token:
        raise ValueError("Pipeline API is not configured")

    pipeline_id = payload.get("pipeline_id")
    if not pipeline_id:
        raise ValueError("pipeline_id is required")

    response = requests.post(
        f"{api_url.rstrip('/')}/pipelines/{pipeline_id}/runs",
        json=payload.get("parameters") or {},
        headers={"Authorization": f"Bearer {api_token}"},
        timeout=15,
    )
    response.raise_for_status()
    body = response.json() if response.content else {}
    logger.info("Pipeline triggered", extra={"status_code": response.status_code, "pipeline_id": pipeline_id})
    return {
        "status": "queued",
        "provider": "pipeline",
        "pipeline_id": pipeline_id,
        "run_id": body.get("id"),
    }
