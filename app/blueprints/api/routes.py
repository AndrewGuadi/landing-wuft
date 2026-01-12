import logging
from json import JSONDecodeError

from flask import Blueprint, jsonify, request
from werkzeug.exceptions import BadRequest

from ...services import email_service, pipeline_service, stripe_service, teams_service
from ...extensions import db
from ...models import SponsorshipApplication

logger = logging.getLogger(__name__)

api_bp = Blueprint("api", __name__, url_prefix="/api")


def _get_json_payload():
    if not request.data:
        raise ValueError("JSON body is required")
    try:
        payload = request.get_json()
    except (BadRequest, JSONDecodeError) as exc:
        raise ValueError("Invalid JSON payload") from exc
    if not isinstance(payload, dict):
        raise ValueError("JSON body must be an object")
    return payload


def _handle_service_error(error: Exception, status_code: int = 400):
    logger.warning("API error", exc_info=error)
    return jsonify({"error": str(error)}), status_code


@api_bp.post("/stripe/checkout-session")
def create_checkout_session():
    try:
        payload = _get_json_payload()
        session = stripe_service.create_checkout_session(payload)
        return jsonify(session), 201
    except ValueError as exc:
        return _handle_service_error(exc, 400)
    except Exception as exc:  # pragma: no cover - safeguard for unexpected provider errors
        return _handle_service_error(exc, 502)


@api_bp.post("/stripe/webhook")
def stripe_webhook():
    signature = request.headers.get("Stripe-Signature", "")
    try:
        payload = request.get_data(as_text=False)
        result = stripe_service.handle_webhook(payload, signature)
        if result.get("type") == "checkout.session.completed":
            metadata = (result.get("data") or {}).get("object", {}).get("metadata", {})
            application_id = metadata.get("application_id")
            if application_id:
                application = SponsorshipApplication.query.get(int(application_id))
                if application:
                    application.payment_status = "paid"
                    application.status = "paid"
                    db.session.commit()
        return jsonify(result), 200
    except ValueError as exc:
        return _handle_service_error(exc, 400)
    except Exception as exc:  # pragma: no cover - safeguard for unexpected provider errors
        return _handle_service_error(exc, 502)


@api_bp.post("/teams/notify")
def teams_notify():
    try:
        payload = _get_json_payload()
        result = teams_service.send_notification(payload)
        return jsonify(result), 200
    except ValueError as exc:
        return _handle_service_error(exc, 400)
    except Exception as exc:  # pragma: no cover - safeguard for unexpected provider errors
        return _handle_service_error(exc, 502)


@api_bp.post("/email/send")
def email_send():
    try:
        payload = _get_json_payload()
        result = email_service.send_email(payload)
        return jsonify(result), 202
    except ValueError as exc:
        return _handle_service_error(exc, 400)
    except Exception as exc:  # pragma: no cover - safeguard for unexpected provider errors
        return _handle_service_error(exc, 502)


@api_bp.post("/pipeline/run")
def pipeline_run():
    try:
        payload = _get_json_payload()
        result = pipeline_service.run_pipeline(payload)
        return jsonify(result), 202
    except ValueError as exc:
        return _handle_service_error(exc, 400)
    except Exception as exc:  # pragma: no cover - safeguard for unexpected provider errors
        return _handle_service_error(exc, 502)
