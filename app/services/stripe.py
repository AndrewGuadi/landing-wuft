from typing import Any, Dict, Union

import stripe
from flask import current_app
from stripe import error as stripe_error


def _get_price_map() -> Dict[str, str]:
    return {
        "food_vendor": current_app.config.get("STRIPE_PRICE_FOOD_VENDOR", ""),
        "liability_fee": current_app.config.get("STRIPE_PRICE_LIABILITY_FEE", ""),
        "sponsor_wish_granter": current_app.config.get("STRIPE_PRICE_SPONSOR_WISH_GRANTER", ""),
        "sponsor_wonders_wishes": current_app.config.get(
            "STRIPE_PRICE_SPONSOR_WONDERS_WISHES", ""
        ),
        "sponsor_food_truck_champion": current_app.config.get(
            "STRIPE_PRICE_SPONSOR_FOOD_TRUCK_CHAMPION", ""
        ),
        "sponsor_dream_maker": current_app.config.get("STRIPE_PRICE_SPONSOR_DREAM_MAKER", ""),
        "sponsor_wish_builder": current_app.config.get("STRIPE_PRICE_SPONSOR_WISH_BUILDER", ""),
        "sponsor_hope_helper": current_app.config.get("STRIPE_PRICE_SPONSOR_HOPE_HELPER", ""),
        "sponsor_joy_giver": current_app.config.get("STRIPE_PRICE_SPONSOR_JOY_GIVER", ""),
        "sponsor_test": current_app.config.get("STRIPE_PRICE_TEST_SPONSOR", ""),
        "sponsor_every_dream_matters": current_app.config.get(
            "STRIPE_PRICE_SPONSOR_EVERY_DREAM_MATTERS", ""
        ),
    }


def create_checkout_session(payload: Dict[str, Any]) -> Dict[str, Any]:
    stripe.api_key = current_app.config.get("STRIPE_API_KEY")
    if not stripe.api_key:
        raise ValueError("Stripe API key is not configured")

    product = payload.get("product")
    if not product or not isinstance(product, str):
        raise ValueError("product must be a non-empty string")

    price_map = _get_price_map()
    price_id = price_map.get(product)
    if not price_id:
        raise ValueError(f"Stripe price is not configured for product '{product}'")

    quantity = payload.get("quantity", 1)
    if not isinstance(quantity, int) or quantity < 1:
        raise ValueError("quantity must be a positive integer")

    line_items = [{"price": price_id, "quantity": quantity}]

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
