import re

from flask import Blueprint, current_app, jsonify, request
from flask_login import login_user, logout_user

from app.services.auth_store import authenticate_user, create_user

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")
EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        payload = request.get_json(silent=True) or {}
        errors = _validate_credentials(payload)
        if errors:
            return jsonify({"status": "error", "errors": errors}), 400

        user = authenticate_user(
            current_app,
            payload["email"],
            payload["password"],
        )
        if not user:
            return jsonify({"status": "error", "message": "Invalid credentials."}), 401
        login_user(user)
        return jsonify({"status": "ok", "user": _user_response(user)}), 200
    return jsonify({"status": "ok", "message": "Login endpoint ready."}), 200


@auth_bp.route("/register", methods=["POST"])
def register():
    if not current_app.config.get("ALLOW_PUBLIC_REGISTRATION", False):
        return jsonify({"status": "error", "message": "Registration is disabled."}), 403
    payload = request.get_json(silent=True) or {}
    errors = _validate_credentials(payload)
    if errors:
        return jsonify({"status": "error", "errors": errors}), 400
    try:
        user = create_user(
            current_app,
            payload["email"],
            payload["password"],
        )
    except ValueError as exc:
        return jsonify({"status": "error", "message": str(exc)}), 409
    return jsonify({"status": "ok", "user": _user_response(user)}), 201


@auth_bp.post("/logout")
def logout():
    logout_user()
    return jsonify({"status": "ok", "message": "Logged out."}), 200


def _validate_credentials(payload: dict) -> list[str]:
    errors = []
    email = payload.get("email", "")
    password = payload.get("password", "")
    if not email or not isinstance(email, str) or not EMAIL_PATTERN.match(email):
        errors.append("Valid email is required.")
    if not password or not isinstance(password, str) or len(password) < 8:
        errors.append("Password must be at least 8 characters.")
    return errors


def _user_response(user) -> dict:
    return {"id": user.id, "email": user.email}
