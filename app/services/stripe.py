from typing import Any, Dict, Union

import stripe
from flask import current_app
from stripe import error as stripe_error


def create_checkout_session(payload: Dict[str, Any]) -> Dict[str, Any]:
    stripe.api_key = current_app.config.get("STRIPE_API_KEY")
    if not stripe.api_key:
        raise ValueError("Stripe API key is not configured")

    line_items = payload.get("line_items")
    if not isinstance(line_items, list) or not line_items:
        raise ValueError("line_items must be a non-empty list")

    mode = payload.get("mode", "payment")
    success_url = payload.get("success_url")
    cancel_url = payload.get("cancel_url")
    if not success_url or not cancel_url:
        raise ValueError("success_url and cancel_url are required")

    session = stripe.checkout.Session.create(
        line_items=line_items,
        mode=mode,
        success_url=success_url,
        cancel_url=cancel_url,
        customer_email=payload.get("customer_email"),
        metadata=payload.get("metadata"),
    )
    return {
        "status": "created",
        "provider": "stripe",
        "session_id": session.id,
        "url": session.url,
    }


def handle_webhook(payload: Union[str, bytes], signature: str) -> Dict[str, Any]:
    webhook_secret = current_app.config.get("STRIPE_WEBHOOK_SECRET")
    if not webhook_secret:
        raise ValueError("Stripe webhook secret is not configured")
    if not signature:
        raise ValueError("Stripe signature header is required")

    try:
        event = stripe.Webhook.construct_event(payload, signature, webhook_secret)
    except (ValueError, stripe_error.SignatureVerificationError) as exc:
        raise ValueError(f"Invalid Stripe webhook: {exc}") from exc

    event_payload = event.to_dict() if hasattr(event, "to_dict") else event
    return {
        "status": "processed",
        "provider": "stripe",
        "type": event_payload.get("type"),
        "id": event_payload.get("id"),
        "data": event_payload.get("data"),
    }


def retrieve_checkout_session(session_id: str) -> Dict[str, Any]:
    stripe.api_key = current_app.config.get("STRIPE_API_KEY")
    if not stripe.api_key:
        raise ValueError("Stripe API key is not configured")
    if not session_id:
        raise ValueError("Stripe session id is required")

    session = stripe.checkout.Session.retrieve(session_id)
    session_payload = session.to_dict() if hasattr(session, "to_dict") else session
    return {
        "status": "retrieved",
        "provider": "stripe",
        "session": session_payload,
    }
