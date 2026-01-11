import os
import unittest

from app import create_app
from app.extensions import db
from app.models import (
    FoodVendorApplication,
    LiabilityApplication,
    SponsorshipApplication,
)


class ApplicationFormTests(unittest.TestCase):
    def setUp(self) -> None:
        os.environ["DATABASE_URL"] = "sqlite:///:memory:"
        self.app = create_app()
        self.app.config.update(
            TESTING=True,
            WTF_CSRF_ENABLED=False,
        )
        with self.app.app_context():
            db.drop_all()
            db.create_all()
        self.client = self.app.test_client()

    def tearDown(self) -> None:
        with self.app.app_context():
            db.drop_all()
        os.environ.pop("DATABASE_URL", None)

    def test_sponsorship_application_submission(self) -> None:
        response = self.client.post(
            "/sponsorship-application",
            data={
                "business_name": "Star LLC",
                "contact_name": "Jane Doe",
                "cell_phone": "555-111-2222",
                "email": "jane@example.com",
            },
        )
        self.assertEqual(response.status_code, 302)
        with self.app.app_context():
            self.assertEqual(SponsorshipApplication.query.count(), 1)

    def test_food_vendor_application_submission(self) -> None:
        response = self.client.post(
            "/food-vendor-application",
            data={
                "business_name": "Truck Co",
                "contact_name": "John Doe",
                "cell_phone": "555-333-4444",
                "email": "john@example.com",
                "service_window_location": "driver",
                "payment_cash": "y",
            },
        )
        self.assertEqual(response.status_code, 302)
        with self.app.app_context():
            self.assertEqual(FoodVendorApplication.query.count(), 1)

    def test_liability_application_submission(self) -> None:
        response = self.client.post(
            "/liability-application",
            data={
                "applicant_signature": "Jane Doe",
                "applicant_full_name": "Jane Doe",
            },
        )
        self.assertEqual(response.status_code, 302)
        with self.app.app_context():
            self.assertEqual(LiabilityApplication.query.count(), 1)
