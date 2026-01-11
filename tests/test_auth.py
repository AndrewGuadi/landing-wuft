import os
import tempfile

import pytest

from app import create_app
from app.services.auth_store import init_auth_db


@pytest.fixture()
def app():
    db_fd, db_path = tempfile.mkstemp()
    os.close(db_fd)
    app = create_app()
    app.config.update(
        TESTING=True,
        AUTH_DB_PATH=db_path,
        SECRET_KEY="test-secret",
        ALLOW_PUBLIC_REGISTRATION=True,
    )
    with app.app_context():
        init_auth_db(app)
    yield app
    os.remove(db_path)


@pytest.fixture()
def client(app):
    return app.test_client()


def test_register_login_logout(client):
    response = client.post(
        "/auth/register",
        json={"email": "user@example.com", "password": "password123"},
    )
    assert response.status_code == 201
    assert response.get_json()["user"]["email"] == "user@example.com"

    bad_login = client.post(
        "/auth/login",
        json={"email": "user@example.com", "password": "wrongpass"},
    )
    assert bad_login.status_code == 401

    login = client.post(
        "/auth/login",
        json={"email": "user@example.com", "password": "password123"},
    )
    assert login.status_code == 200
    assert login.get_json()["user"]["email"] == "user@example.com"

    logout = client.post("/auth/logout")
    assert logout.status_code == 200


def test_register_validation_errors(client):
    response = client.post("/auth/register", json={"email": "not-an-email", "password": "short"})
    assert response.status_code == 400
    errors = response.get_json()["errors"]
    assert "Valid email is required." in errors
    assert "Password must be at least 8 characters." in errors


def test_register_duplicate_email(client):
    client.post(
        "/auth/register",
        json={"email": "dupe@example.com", "password": "password123"},
    )
    response = client.post(
        "/auth/register",
        json={"email": "dupe@example.com", "password": "password123"},
    )
    assert response.status_code == 409


def test_login_validation_errors(client):
    response = client.post("/auth/login", json={"email": "", "password": "short"})
    assert response.status_code == 400
    errors = response.get_json()["errors"]
    assert "Valid email is required." in errors
    assert "Password must be at least 8 characters." in errors


def test_login_unknown_user(client):
    response = client.post(
        "/auth/login",
        json={"email": "missing@example.com", "password": "password123"},
    )
    assert response.status_code == 401
