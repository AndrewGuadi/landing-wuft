from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import (
    BooleanField,
    IntegerField,
    RadioField,
    StringField,
    SubmitField,
)
from wtforms.validators import Email, Optional, DataRequired

ALLOWED_UPLOAD_EXTENSIONS = ["svg", "png", "jpg", "jpeg", "eps", "esp", "webp"]


class SponsorshipApplicationForm(FlaskForm):
    business_name = StringField("Business Name", validators=[DataRequired()])
    contact_name = StringField("Contact Name", validators=[DataRequired()])
    cell_phone = StringField("Cell Phone", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    address = StringField("Address", validators=[Optional()])
    facebook = StringField("Facebook Handle | URL", validators=[Optional()])
    instagram = StringField("Instagram Handle | URL", validators=[Optional()])
    linkedin = StringField("LinkedIn Handle | URL", validators=[Optional()])
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
    logo_file = FileField(
        "Upload Your Logos",
        validators=[
            FileRequired(),
            FileAllowed(ALLOWED_UPLOAD_EXTENSIONS, "Upload a valid logo file."),
        ],
    )
    submit = SubmitField("Complete Application")


class FoodVendorApplicationForm(FlaskForm):
    business_name = StringField("Business Name", validators=[DataRequired()])
    contact_name = StringField("Contact Name", validators=[DataRequired()])
    cell_phone = StringField("Cell Phone", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    address = StringField("Address", validators=[Optional()])
    facebook = StringField("Facebook Handle | URL", validators=[Optional()])
    instagram = StringField("Instagram Handle | URL", validators=[Optional()])
    linkedin = StringField("LinkedIn Handle | URL", validators=[Optional()])
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
    vehicle_year = StringField("Year", validators=[DataRequired()])
    insurance_policy_number = StringField("Insurance Policy Number", validators=[DataRequired()])
    drivers_license = StringField("Driver’s License Number", validators=[Optional()])
    state_issued_id = StringField("State Issued ID", validators=[Optional()])
    additional_vehicle_count = IntegerField("Additional Vehicles", validators=[Optional()])
    payment_cash = BooleanField("Cash", validators=[Optional()])
    payment_debit = BooleanField("Debit", validators=[Optional()])
    payment_visa = BooleanField("VISA", validators=[Optional()])
    payment_mastercard = BooleanField("MasterCard", validators=[Optional()])
    payment_amex = BooleanField("AMEX", validators=[Optional()])
    payment_discover = BooleanField("Discover", validators=[Optional()])
    payment_other = StringField("Other Payment", validators=[Optional()])
    menu_item_1 = StringField("Item 1", validators=[Optional()])
    menu_item_2 = StringField("Item 2", validators=[Optional()])
    menu_item_3 = StringField("Item 3", validators=[Optional()])
    menu_item_4 = StringField("Item 4", validators=[Optional()])
    menu_item_5 = StringField("Item 5", validators=[Optional()])
    menu_item_6 = StringField("Item 6", validators=[Optional()])
    menu_item_7 = StringField("Item 7", validators=[Optional()])
    menu_item_8 = StringField("Item 8", validators=[Optional()])
    applicant_signature = StringField("Applicant Signature", validators=[DataRequired()])
    applicant_full_name = StringField("Applicant Full Name", validators=[DataRequired()])
    company_name = StringField("Company Name", validators=[DataRequired()])
    application_date = StringField("Date", validators=[DataRequired()])
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

    def validate(self, extra_validators=None):
        is_valid = super().validate(extra_validators=extra_validators)
        if not is_valid:
            return False

        if not (self.drivers_license.data or self.state_issued_id.data):
            message = "Provide a driver's license number or state-issued ID."
            self.drivers_license.errors.append(message)
            self.state_issued_id.errors.append(message)
            is_valid = False

        payment_selected = any(
            [
                self.payment_cash.data,
                self.payment_debit.data,
                self.payment_visa.data,
                self.payment_mastercard.data,
                self.payment_amex.data,
                self.payment_discover.data,
                bool(self.payment_other.data),
            ]
        )
        if not payment_selected:
            self.payment_cash.errors.append("Select at least one payment method.")
            is_valid = False

        menu_items = [
            self.menu_item_1.data,
            self.menu_item_2.data,
            self.menu_item_3.data,
            self.menu_item_4.data,
            self.menu_item_5.data,
            self.menu_item_6.data,
            self.menu_item_7.data,
            self.menu_item_8.data,
        ]
        filled_items = [item for item in menu_items if (item or "").strip()]
        if len(filled_items) < 6:
            self.menu_item_1.errors.append("Please list at least six menu items.")
            is_valid = False

        return is_valid


class LiabilityApplicationForm(FlaskForm):
    applicant_signature = StringField("Applicant Signature", validators=[DataRequired()])
    applicant_full_name = StringField("Applicant Full Name", validators=[DataRequired()])
    company_name = StringField("Company Name", validators=[Optional()])
    application_date = StringField("Date", validators=[Optional()])
    submit = SubmitField("Complete Application")
