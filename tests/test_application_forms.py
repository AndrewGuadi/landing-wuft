import io
import os
import tempfile
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
        self.uploads_dir = tempfile.TemporaryDirectory()
        self.app.config.update(
            TESTING=True,
            WTF_CSRF_ENABLED=False,
            UPLOAD_FOLDER=self.uploads_dir.name,
        )
        with self.app.app_context():
            db.drop_all()
            db.create_all()
        self.client = self.app.test_client()

    def tearDown(self) -> None:
        with self.app.app_context():
            db.drop_all()
        self.uploads_dir.cleanup()
        os.environ.pop("DATABASE_URL", None)

    def test_sponsorship_application_submission(self) -> None:
        response = self.client.post(
            "/sponsorship-application",
            data={
                "business_name": "Star LLC",
                "contact_name": "Jane Doe",
                "cell_phone": "555-111-2222",
                "email": "jane@example.com",
                "support_level": "wish_granter",
                "logo_file": (io.BytesIO(b"logo"), "logo.png"),
            },
            content_type="multipart/form-data",
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
                "vehicle_make_model": "Big Truck",
                "vehicle_year": "2020",
                "insurance_policy_number": "POLICY-123",
                "drivers_license": "D1234567",
                "payment_cash": "y",
                "menu_item_1": "Tacos",
                "menu_item_2": "Burritos",
                "menu_item_3": "Nachos",
                "menu_item_4": "Quesadilla",
                "menu_item_5": "Churros",
                "menu_item_6": "Soda",
                "applicant_signature": "John Doe",
                "applicant_full_name": "John Doe",
                "company_name": "Truck Co",
                "application_date": "2026-03-01",
                "initials": "JD",
                "logo_file": (io.BytesIO(b"logo"), "logo.png"),
                "insurance_file": (io.BytesIO(b"insurance"), "insurance.png"),
            },
            content_type="multipart/form-data",
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
