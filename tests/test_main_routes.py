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
        "/",
        "/sponsor",
        "/food-vendor",
        "/food-vendor-application",
        "/sponsorship-application",
        "/liability-application",
    ],
)
def test_page_routes_ok(client, route):
    response = client.get(route)
    assert response.status_code == 200


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}
