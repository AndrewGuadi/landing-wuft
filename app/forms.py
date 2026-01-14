from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import (
    BooleanField,
    IntegerField,
    RadioField,
    StringField,
    SubmitField,
    DateField,
    TextAreaField
)
from wtforms.validators import Email, Optional, DataRequired, NumberRange

# Removed 'esp' (typo) and 'svg' (security risk)
ALLOWED_UPLOAD_EXTENSIONS = ["png", "jpg", "jpeg", "eps", "webp"]

class BaseContactForm(FlaskForm):
    """
    Base class containing fields common to all business applications.
    """
    business_name = StringField("Business Name", validators=[DataRequired()])
    contact_name = StringField("Contact Name", validators=[DataRequired()])
    cell_phone = StringField("Cell Phone", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    address = StringField("Address", validators=[Optional()])
    facebook = StringField("Facebook Handle | URL", validators=[Optional()])
    instagram = StringField("Instagram Handle | URL", validators=[Optional()])
    linkedin = StringField("LinkedIn Handle | URL", validators=[Optional()])

class SponsorshipApplicationForm(BaseContactForm):
    support_level = RadioField(
        "Select Your Support",
        choices=[
            ("wish_granter", "Wish Granter ($10,000)"),
            ("wonders_wishes", "Wonders & Wishes Sponsor ($5,000)"),
            ("food_truck_champion", "Food Truck Champion ($3,500)"),
            ("dream_maker", "Dream Maker Sponsor ($2,500)"),
            ("wish_builder", "Wish Builder Sponsor ($1,000)"),
            ("hope_helper", "Hope Helper Sponsor ($500)"),
            ("joy_giver", "Joy Giver Sponsor ($250)"),
        ],
        validators=[DataRequired()],
    )
    submit = SubmitField("Complete Application")

class FoodVendorApplicationForm(BaseContactForm):
    service_window_location = RadioField(
        "Service Window Location",
        choices=[
            ("driver", "Driver’s Side"),
            ("passenger", "Passenger’s Side"),
            ("back", "Back of Truck"),
        ],
        validators=[DataRequired()],
    )
    vehicle_make_model = StringField("Make/Model", validators=[DataRequired()])
    
    # Changed to IntegerField with Range
    vehicle_year = IntegerField(
        "Year", 
        validators=[DataRequired(), NumberRange(min=1900, max=2100)]
    )
    
    insurance_policy_number = StringField("Insurance Policy Number", validators=[DataRequired()])
    drivers_license = StringField("Driver’s License Number", validators=[Optional()])
    state_issued_id = StringField("State Issued ID", validators=[Optional()])
    
    additional_vehicle_count = IntegerField(
        "Additional Vehicles", 
        validators=[Optional(), NumberRange(min=0)]
    )

    # Payments
    payment_cash = BooleanField("Cash", validators=[Optional()])
    payment_debit = BooleanField("Debit", validators=[Optional()])
    payment_visa = BooleanField("VISA", validators=[Optional()])
    payment_mastercard = BooleanField("MasterCard", validators=[Optional()])
    payment_amex = BooleanField("AMEX", validators=[Optional()])
    payment_discover = BooleanField("Discover", validators=[Optional()])
    payment_other = StringField("Other Payment", validators=[Optional()])

    # Menu Items
    menu_item_1 = StringField("Item 1", validators=[Optional()])
    menu_item_2 = StringField("Item 2", validators=[Optional()])
    menu_item_3 = StringField("Item 3", validators=[Optional()])
    menu_item_4 = StringField("Item 4", validators=[Optional()])
    menu_item_5 = StringField("Item 5", validators=[Optional()])
    menu_item_6 = StringField("Item 6", validators=[Optional()])
    menu_item_7 = StringField("Item 7", validators=[Optional()])
    menu_item_8 = StringField("Item 8", validators=[Optional()])

    # Signatures
    applicant_signature = StringField("Applicant Signature", validators=[DataRequired()])
    applicant_full_name = StringField("Applicant Full Name", validators=[DataRequired()])
    company_name = StringField("Company Name", validators=[DataRequired()])
    
    # Changed to DateField
    application_date = DateField("Date", format='%Y-%m-%d', validators=[DataRequired()])
    
    initials = StringField("Initials", validators=[DataRequired()])
    
    logo_file = FileField(
        "Upload Your Logos",
        validators=[
            FileRequired(),
            FileAllowed(ALLOWED_UPLOAD_EXTENSIONS, "Upload a valid logo file."),
        ],
    )
    insurance_file = FileField(
        "Upload Your Certificate of Insurance",
        validators=[
            FileRequired(),
            FileAllowed(ALLOWED_UPLOAD_EXTENSIONS, "Upload a valid certificate file."),
        ],
    )
    submit = SubmitField("Complete Application")

    def validate(self, **kwargs):
        """
        Custom validation for complex interdependent fields.
        Using **kwargs is the modern WTForms signature.
        """
        # Run standard validators first
        if not super().validate(**kwargs):
            return False

        # 1. ID Validation
        if not (self.drivers_license.data or self.state_issued_id.data):
            msg = "Provide a driver's license number or state-issued ID."
            self.drivers_license.errors.append(msg)
            self.state_issued_id.errors.append(msg)
            return False

        # 2. Payment Method Validation
        payment_methods = [
            self.payment_cash.data,
            self.payment_debit.data,
            self.payment_visa.data,
            self.payment_mastercard.data,
            self.payment_amex.data,
            self.payment_discover.data,
            bool(self.payment_other.data and self.payment_other.data.strip())
        ]
        
        if not any(payment_methods):
            self.payment_cash.errors.append("Select at least one payment method.")
            return False

        # 3. Menu Item Validation (At least 6 items)
        menu_items = [
            self.menu_item_1.data, self.menu_item_2.data, self.menu_item_3.data,
            self.menu_item_4.data, self.menu_item_5.data, self.menu_item_6.data,
            self.menu_item_7.data, self.menu_item_8.data
        ]
        
        # Filter out None and empty strings
        filled_items = [item for item in menu_items if item and item.strip()]
        
        if len(filled_items) < 6:
            self.menu_item_1.errors.append("Please list at least six menu items.")
            return False

        return True

class LiabilityApplicationForm(FlaskForm):
    applicant_signature = StringField("Applicant Signature", validators=[DataRequired()])
    applicant_full_name = StringField("Applicant Full Name", validators=[DataRequired()])
    company_name = StringField("Company Name", validators=[Optional()])
    # Changed to DateField
    application_date = DateField("Date", format='%Y-%m-%d', validators=[Optional()])
    submit = SubmitField("Complete Application")
