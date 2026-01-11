from flask import Blueprint, jsonify, request

from ...services import email_service, pipeline_service, stripe_service, teams_service

api_bp = Blueprint("api", __name__, url_prefix="/api")


@api_bp.post("/stripe/checkout-session")
def create_checkout_session():
    payload = request.get_json(silent=True) or {}
    session = stripe_service.create_checkout_session(payload)
    return jsonify(session), 201


@api_bp.post("/stripe/webhook")
def stripe_webhook():
    payload = request.get_json(silent=True) or {}
    signature = request.headers.get("Stripe-Signature", "")
    result = stripe_service.handle_webhook(payload, signature)
    return jsonify(result), 200


@api_bp.post("/teams/notify")
def teams_notify():
    payload = request.get_json(silent=True) or {}
    result = teams_service.send_notification(payload)
    return jsonify(result), 200


@api_bp.post("/email/send")
def email_send():
    payload = request.get_json(silent=True) or {}
    result = email_service.send_email(payload)
    return jsonify(result), 202


@api_bp.post("/pipeline/run")
def pipeline_run():
    payload = request.get_json(silent=True) or {}
    result = pipeline_service.run_pipeline(payload)
    return jsonify(result), 202
