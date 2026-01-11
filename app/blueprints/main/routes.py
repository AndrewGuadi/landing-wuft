from flask import Blueprint, flash, jsonify, redirect, render_template, url_for

from app.extensions import db
from app.forms import (
    FoodVendorApplicationForm,
    LiabilityApplicationForm,
    SponsorshipApplicationForm,
)
from app.models import (
    FoodVendorApplication,
    LiabilityApplication,
    SponsorshipApplication,
)
from app.services.notifications import send_placeholder_email
from app.services.uploads import save_uploaded_file

main_bp = Blueprint("main", __name__)


@main_bp.get("/")
def home():
    return render_template("home.html")


@main_bp.get("/sponsor")
def sponsor_page():
    return render_template("sponsor-page.html")


@main_bp.get("/food-vendor")
def food_vendor_page():
    return render_template("food-vendor.html")


@main_bp.get("/health")
def health_check():
    return jsonify({"status": "ok"}), 200


@main_bp.route("/food-vendor-application", methods=["GET", "POST"])
def food_vendor_application():
    form = FoodVendorApplicationForm()
    if form.validate_on_submit():
        logo_filename = save_uploaded_file(form.logo_file.data, "food-vendor")
        insurance_filename = save_uploaded_file(form.insurance_file.data, "food-vendor")
        application = FoodVendorApplication(
            business_name=form.business_name.data,
            contact_name=form.contact_name.data,
            cell_phone=form.cell_phone.data,
            email=form.email.data,
            address=form.address.data,
            facebook=form.facebook.data,
            instagram=form.instagram.data,
            linkedin=form.linkedin.data,
            service_window_location=form.service_window_location.data,
            vehicle_make_model=form.vehicle_make_model.data,
            vehicle_year=form.vehicle_year.data,
            insurance_policy_number=form.insurance_policy_number.data,
            drivers_license=form.drivers_license.data,
            state_issued_id=form.state_issued_id.data,
            additional_vehicle_count=form.additional_vehicle_count.data,
            payment_cash=form.payment_cash.data,
            payment_debit=form.payment_debit.data,
            payment_visa=form.payment_visa.data,
            payment_mastercard=form.payment_mastercard.data,
            payment_amex=form.payment_amex.data,
            payment_discover=form.payment_discover.data,
            payment_other=form.payment_other.data,
            menu_item_1=form.menu_item_1.data,
            menu_item_2=form.menu_item_2.data,
            menu_item_3=form.menu_item_3.data,
            menu_item_4=form.menu_item_4.data,
            menu_item_5=form.menu_item_5.data,
            menu_item_6=form.menu_item_6.data,
            menu_item_7=form.menu_item_7.data,
            menu_item_8=form.menu_item_8.data,
            applicant_signature=form.applicant_signature.data,
            applicant_full_name=form.applicant_full_name.data,
            company_name=form.company_name.data,
            application_date=form.application_date.data,
            initials=form.initials.data,
            logo_filename=logo_filename,
            insurance_filename=insurance_filename,
        )
        db.session.add(application)
        db.session.commit()
        send_placeholder_email("Food vendor application received", form.email.data)
        flash("Your food vendor application was submitted. Please complete the liability release.", "success")
        return redirect(url_for("main.liability_application"))
    return render_template("food-vendor-application.html", form=form)


@main_bp.route("/sponsorship-application", methods=["GET", "POST"])
def sponsorship_application():
    form = SponsorshipApplicationForm()
    if form.validate_on_submit():
        logo_filename = save_uploaded_file(form.logo_file.data, "sponsorship")
        application = SponsorshipApplication(
            business_name=form.business_name.data,
            contact_name=form.contact_name.data,
            cell_phone=form.cell_phone.data,
            email=form.email.data,
            address=form.address.data,
            facebook=form.facebook.data,
            instagram=form.instagram.data,
            linkedin=form.linkedin.data,
            support_level=form.support_level.data,
            logo_filename=logo_filename,
        )
        db.session.add(application)
        db.session.commit()
        send_placeholder_email("Sponsorship application received", form.email.data)
        flash("Thanks for applying to sponsor the festival! We'll follow up soon.", "success")
        return redirect(url_for("main.sponsorship_application"))
    return render_template("sponsorship-application.html", form=form)


@main_bp.route("/liability-application", methods=["GET", "POST"])
def liability_application():
    form = LiabilityApplicationForm()
    if form.validate_on_submit():
        application = LiabilityApplication(
            applicant_signature=form.applicant_signature.data,
            applicant_full_name=form.applicant_full_name.data,
            company_name=form.company_name.data,
            application_date=form.application_date.data,
        )
        db.session.add(application)
        db.session.commit()
        send_placeholder_email(
            "Liability release received", "liability@wishuponafoodtruck.com"
        )
        flash("Your liability release has been submitted. Thank you!", "success")
        return redirect(url_for("main.liability_application"))
    return render_template("liability-application.html", form=form)
