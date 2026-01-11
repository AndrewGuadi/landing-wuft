import os


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///local.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    STRIPE_API_KEY = os.getenv("STRIPE_API_KEY", "")
    STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "")
    TEAMS_WEBHOOK_URL = os.getenv("TEAMS_WEBHOOK_URL", "")
    DEFAULT_EMAIL_SENDER = os.getenv("DEFAULT_EMAIL_SENDER", "hello@wishuponafoodtruck.com")
    SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY", "")
    SENDGRID_SENDER = os.getenv("SENDGRID_SENDER", DEFAULT_EMAIL_SENDER)
    PIPELINE_API_URL = os.getenv("PIPELINE_API_URL", "")
    PIPELINE_API_TOKEN = os.getenv("PIPELINE_API_TOKEN", "")
