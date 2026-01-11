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
        SQLALCHEMY_DATABASE_URI="sqlite:///:memory:",
    )
    with app.app_context():
        init_auth_db(app)
    yield app
    os.remove(db_path)


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.mark.parametrize(
    "route",
    [
        "/api/stripe/checkout-session",
        "/api/teams/notify",
        "/api/email/send",
        "/api/pipeline/run",
    ],
)
def test_api_stub_requires_configuration(client, route):
    response = client.post(route, json={})
    assert response.status_code == 400
    assert response.get_json()["error"]


def test_stripe_webhook_requires_configuration(client):
    response = client.post("/api/stripe/webhook", data=b"{}")
    assert response.status_code == 400
    assert response.get_json()["error"]
