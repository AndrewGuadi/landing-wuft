import os

from app import create_app
from app.services.auth_store import create_user, init_auth_db


def main() -> None:
    email = 'team@wishuponafoodtruck.com'
    password = 'newpassword'

    if not email or not password:
        raise SystemExit("Set ADMIN_EMAIL and ADMIN_PASSWORD to seed an admin account.")

    app = create_app()
    with app.app_context():
        init_auth_db(app)
        create_user(app, email, password)
    print(f"Admin user created for {email}.")


if __name__ == "__main__":
    main()
