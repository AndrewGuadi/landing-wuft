# Architecture and Build Guide

## App entrypoint and app factory
- **Entrypoint:** `app.py` initializes the Flask application by calling `create_app()` and runs the app directly when executed (`python app.py`).
- **App factory:** `app.create_app` (defined in `app/__init__.py`) creates the Flask instance, loads configuration from `Config`, and registers all blueprints.

## Blueprints and responsibilities
- **`main` (`app/blueprints/main`)**: Serves public, template-rendered pages such as the homepage, sponsor page, and application forms.
- **`auth` (`app/blueprints/auth`)**: Provides authentication-related API endpoints (`/auth/login`, `/auth/register`, `/auth/logout`) as JSON stubs.
- **`api` (`app/blueprints/api`)**: Provides JSON API endpoints for integrations (Stripe checkout/webhook, Teams notifications, email sending, and pipeline run).

## Templates and routes
Templates live under `app/templates/` and are rendered by the `main` blueprint:

| Template | Route | Blueprint handler |
| --- | --- | --- |
| `home.html` | `/` | `main.home` |
| `sponsor-page.html` | `/sponsor` | `main.sponsor_page` |
| `food-vendor.html` | `/food-vendor` | `main.food_vendor_page` |
| `food-vendor-application.html` | `/food-vendor-application` | `main.food_vendor_application` |
| `sponsorship-application.html` | `/sponsorship-application` | `main.sponsorship_application` |
| `liability-application.html` | `/liability-application` | `main.liability_application` |

## Environment variables
Configuration is defined in `app/config.py` and loaded via `Config`:

- `SECRET_KEY` (defaults to `dev-secret-key` for local development)
- `STRIPE_API_KEY`
- `STRIPE_WEBHOOK_SECRET`
- `TEAMS_WEBHOOK_URL`
- `DEFAULT_EMAIL_SENDER` (defaults to `hello@wishuponafoodtruck.com`)

## Local setup
1. Create and activate a virtual environment.
   - `python -m venv .venv`
   - `source .venv/bin/activate`
2. Install dependencies.
   - `pip install -r requirements.txt`
3. Run the app locally.
   - `python app.py`

## Deployment / run
1. Set `SECRET_KEY` and any needed integration variables (`STRIPE_API_KEY`, `STRIPE_WEBHOOK_SECRET`, `TEAMS_WEBHOOK_URL`, `DEFAULT_EMAIL_SENDER`).
2. Run with Flask or Gunicorn:
   - Flask (development): `flask run`
   - Gunicorn (production, if added later): `gunicorn "app:create_app()"`

## Verification checklist
- Open the main pages in a browser:
  - `/`
  - `/sponsor`
  - `/food-vendor`
- Exercise API endpoints (expect JSON responses):
  - `/api/stripe/checkout-session`
  - `/api/stripe/webhook`
  - `/api/teams/notify`
  - `/api/email/send`
  - `/api/pipeline/run`
