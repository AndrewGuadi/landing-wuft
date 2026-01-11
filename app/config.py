import os


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    AUTH_DB_PATH = os.getenv("AUTH_DB_PATH", os.path.join(os.path.dirname(__file__), "auth.db"))
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///local.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.getenv(
        "UPLOAD_FOLDER", os.path.join(os.path.dirname(__file__), "uploads")
    )
    ALLOW_PUBLIC_REGISTRATION = os.getenv("ALLOW_PUBLIC_REGISTRATION", "false").lower() == "true"
    STRIPE_API_KEY = os.getenv("STRIPE_API_KEY", "")
    STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "")
    TEAMS_WEBHOOK_URL = os.getenv("TEAMS_WEBHOOK_URL", "")
    DEFAULT_EMAIL_SENDER = os.getenv("DEFAULT_EMAIL_SENDER", "hello@wishuponafoodtruck.com")
    SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY", "")
    SENDGRID_SENDER = os.getenv("SENDGRID_SENDER", DEFAULT_EMAIL_SENDER)
    PIPELINE_API_URL = os.getenv("PIPELINE_API_URL", "")
    PIPELINE_API_TOKEN = os.getenv("PIPELINE_API_TOKEN", "")
