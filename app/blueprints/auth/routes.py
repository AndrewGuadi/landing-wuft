from flask import Blueprint, jsonify, request

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        return jsonify({"status": "ok", "message": "Login accepted (stub)."}), 200
    return jsonify({"status": "ok", "message": "Login endpoint ready."}), 200


@auth_bp.route("/register", methods=["POST"])
def register():
    payload = request.get_json(silent=True) or {}
    return jsonify({"status": "ok", "message": "Registration stub.", "payload": payload}), 201


@auth_bp.post("/logout")
def logout():
    return jsonify({"status": "ok", "message": "Logged out (stub)."}), 200
