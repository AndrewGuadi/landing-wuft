from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    IntegerField,
    RadioField,
    StringField,
    SubmitField,
)
from wtforms.validators import Email, Optional, DataRequired


class SponsorshipApplicationForm(FlaskForm):
    business_name = StringField("Business Name", validators=[DataRequired()])
    contact_name = StringField("Contact Name", validators=[DataRequired()])
    cell_phone = StringField("Cell Phone", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    address = StringField("Address", validators=[Optional()])
    facebook = StringField("Facebook Handle | URL", validators=[Optional()])
    instagram = StringField("Instagram Handle | URL", validators=[Optional()])
    linkedin = StringField("LinkedIn Handle | URL", validators=[Optional()])
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
        validators=[Optional()],
    )
    vehicle_make_model = StringField("Make/Model", validators=[Optional()])
    vehicle_year = StringField("Year", validators=[Optional()])
    insurance_policy_number = StringField("Insurance Policy Number", validators=[Optional()])
    drivers_license = StringField("Driver’s License Number & State Issued", validators=[Optional()])
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
    applicant_signature = StringField("Applicant Signature", validators=[Optional()])
    applicant_full_name = StringField("Applicant Full Name", validators=[Optional()])
    company_name = StringField("Company Name", validators=[Optional()])
    application_date = StringField("Date", validators=[Optional()])
    initials = StringField("Initials", validators=[Optional()])
    submit = SubmitField("Complete Application")


class LiabilityApplicationForm(FlaskForm):
    applicant_signature = StringField("Applicant Signature", validators=[DataRequired()])
    applicant_full_name = StringField("Applicant Full Name", validators=[DataRequired()])
    company_name = StringField("Company Name", validators=[Optional()])
    application_date = StringField("Date", validators=[Optional()])
    submit = SubmitField("Complete Application")
