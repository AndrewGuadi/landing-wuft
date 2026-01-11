import os


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///local.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    STRIPE_API_KEY = os.getenv("STRIPE_API_KEY", "")
    STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "")
    TEAMS_WEBHOOK_URL = os.getenv("TEAMS_WEBHOOK_URL", "")
    DEFAULT_EMAIL_SENDER = os.getenv("DEFAULT_EMAIL_SENDER", "hello@wishuponafoodtruck.com")
