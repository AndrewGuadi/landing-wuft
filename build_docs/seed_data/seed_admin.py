import os
from dotenv import load_dotenv, find_dotenv

# Find the nearest .env file by walking up the directory tree
dotenv_path = find_dotenv(filename=".env", raise_error_if_not_found=False)

if dotenv_path:
    load_dotenv(dotenv_path=dotenv_path, override=False)
    print(f"[dotenv] Loaded environment variables from: {dotenv_path}")
else:
    print("[dotenv] No .env file found. Using system environment variables only.")


from app import create_app
from app.services.auth_store import create_user, init_auth_db




def main() -> None:
    email = os.getenv("ADMIN_EMAIL")
    password = os.getenv("ADMIN_PASSWORD")

    if not email or not password:
        raise SystemExit("Set ADMIN_EMAIL and ADMIN_PASSWORD to seed an admin account.")

    app = create_app()
    with app.app_context():
        init_auth_db(app)
        create_user(app, email, password)
    print(f"Admin user created for {email}.")


if __name__ == "__main__":
    main()
