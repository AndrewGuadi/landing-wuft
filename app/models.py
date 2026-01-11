from datetime import datetime, date
from .extensions import db

# 1. Create a Mixin for shared columns
# This works like inheritance. Any model that inherits this will get these columns.
class ContactInfoMixin:
    business_name = db.Column(db.String(255), nullable=False)
    contact_name = db.Column(db.String(255), nullable=False)
    cell_phone = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255))
    facebook = db.Column(db.String(255))
    instagram = db.Column(db.String(255))
    linkedin = db.Column(db.String(255))

class SponsorshipApplication(ContactInfoMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # ContactInfoMixin columns are automatically added here
    
    support_level = db.Column(db.String(50))
    logo_filename = db.Column(db.String(255))
    status = db.Column(db.String(50), default="new", nullable=False)
    payment_status = db.Column(db.String(50), default="pending", nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

class FoodVendorApplication(ContactInfoMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # ContactInfoMixin columns are automatically added here

    service_window_location = db.Column(db.String(50))
    vehicle_make_model = db.Column(db.String(255))
    
    # CHANGED: String -> Integer to match Form
    vehicle_year = db.Column(db.Integer) 
    
    insurance_policy_number = db.Column(db.String(255))
    drivers_license = db.Column(db.String(255))
    state_issued_id = db.Column(db.String(255))
    additional_vehicle_count = db.Column(db.Integer)
    
    # Payments
    payment_cash = db.Column(db.Boolean, default=False, nullable=False)
    payment_debit = db.Column(db.Boolean, default=False, nullable=False)
    payment_visa = db.Column(db.Boolean, default=False, nullable=False)
    payment_mastercard = db.Column(db.Boolean, default=False, nullable=False)
    payment_amex = db.Column(db.Boolean, default=False, nullable=False)
    payment_discover = db.Column(db.Boolean, default=False, nullable=False)
    payment_other = db.Column(db.String(255))
    
    # Menu Items
    menu_item_1 = db.Column(db.String(255))
    menu_item_2 = db.Column(db.String(255))
    menu_item_3 = db.Column(db.String(255))
    menu_item_4 = db.Column(db.String(255))
    menu_item_5 = db.Column(db.String(255))
    menu_item_6 = db.Column(db.String(255))
    menu_item_7 = db.Column(db.String(255))
    menu_item_8 = db.Column(db.String(255))
    
    # Signatures
    applicant_signature = db.Column(db.String(255))
    applicant_full_name = db.Column(db.String(255))
    company_name = db.Column(db.String(255))
    
    # CHANGED: String -> Date to match Form
    application_date = db.Column(db.Date)
    
    initials = db.Column(db.String(20))
    signature_signed_at = db.Column(db.DateTime)
    signature_ip = db.Column(db.String(50))
    
    # Files
    logo_filename = db.Column(db.String(255))
    insurance_filename = db.Column(db.String(255))
    
    status = db.Column(db.String(50), default="new", nullable=False)
    payment_status = db.Column(db.String(50), default="pending", nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

class LiabilityApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    applicant_signature = db.Column(db.String(255), nullable=False)
    applicant_full_name = db.Column(db.String(255), nullable=False)
    company_name = db.Column(db.String(255))
    
    # CHANGED: String -> Date to match Form
    application_date = db.Column(db.Date)
    
    signature_signed_at = db.Column(db.DateTime)
    signature_ip = db.Column(db.String(50))
    status = db.Column(db.String(50), default="new", nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)