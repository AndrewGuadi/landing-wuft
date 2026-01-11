import os

from flask import (
    Blueprint,
    abort,
    current_app,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    send_from_directory,
    url_for,
)
from flask_login import current_user, login_required, login_user, logout_user

from app.extensions import db
from app.forms import (
    FoodVendorApplicationForm,
    LiabilityApplicationForm,
    SponsorshipApplicationForm,
)
from app.models import FoodVendorApplication, LiabilityApplication, SponsorshipApplication
from app.services.notifications import send_placeholder_email
from app.services.uploads import save_uploaded_file
from app.services.auth_store import authenticate_user

main_bp = Blueprint("main", __name__)


@main_bp.get("/")
def home():
    return render_template("home.html")


@main_bp.get("/sponsor")
def sponsor_page():
    return render_template("sponsor-page.html")


@main_bp.get("/downloads/sponsorship-application")
def sponsorship_application_pdf():
    docs_root = os.path.abspath(os.path.join(current_app.root_path, "downloads"))
    filename = "sponsorship_application.pdf"
    return send_from_directory(
        docs_root,
        filename,
        as_attachment=True,
        download_name="sponsorship_application.pdf",
    )


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
            signature_signed_at=db.func.now(),
            signature_ip=request.remote_addr,
            logo_filename=logo_filename,
            insurance_filename=insurance_filename,
            payment_status="pending",
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
            payment_status="pending",
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
            signature_signed_at=db.func.now(),
            signature_ip=request.remote_addr,
        )
        db.session.add(application)
        db.session.commit()
        send_placeholder_email(
            "Liability release received", "liability@wishuponafoodtruck.com"
        )
        flash("Your liability release has been submitted. Thank you!", "success")
        return redirect(url_for("main.liability_application"))
    return render_template("liability-application.html", form=form)


@main_bp.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if current_user.is_authenticated:
        return redirect(url_for("main.admin_dashboard"))

    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        if not email or not password:
            flash("Email and password are required.", "error")
            return render_template("admin-login.html")

        user = authenticate_user(
            current_app,
            email,
            password,
        )
        if not user:
            flash("Invalid login credentials.", "error")
            return render_template("admin-login.html")

        login_user(user)
        flash("Welcome back!", "success")
        return redirect(url_for("main.admin_dashboard"))

    return render_template("admin-login.html")


@main_bp.get("/admin/logout")
@login_required
def admin_logout():
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for("main.admin_login"))


@main_bp.get("/admin/dashboard")
@login_required
def admin_dashboard():
    selected_type = request.args.get("type", "all")
    selected_status = request.args.get("status", "all")

    sponsor_query = SponsorshipApplication.query.order_by(SponsorshipApplication.created_at.desc())
    vendor_query = FoodVendorApplication.query.order_by(FoodVendorApplication.created_at.desc())
    liability_query = LiabilityApplication.query.order_by(LiabilityApplication.created_at.desc())

    if selected_status != "all":
        sponsor_query = sponsor_query.filter_by(status=selected_status)
        vendor_query = vendor_query.filter_by(status=selected_status)
        liability_query = liability_query.filter_by(status=selected_status)

    sponsorships = sponsor_query.all() if selected_type in ("all", "sponsor") else []
    vendors = vendor_query.all() if selected_type in ("all", "vendor") else []
    liabilities = liability_query.all() if selected_type in ("all", "liability") else []

    return render_template(
        "admin-dashboard.html",
        selected_type=selected_type,
        selected_status=selected_status,
        sponsorships=sponsorships,
        vendors=vendors,
        liabilities=liabilities,
    )


@main_bp.get("/admin/application/<string:application_type>/<int:application_id>")
@login_required
def admin_application_detail(application_type: str, application_id: int):
    model_map = {
        "sponsor": SponsorshipApplication,
        "vendor": FoodVendorApplication,
        "liability": LiabilityApplication,
    }
    application = model_map.get(application_type)
    if not application:
        flash("Unknown application type.", "error")
        return redirect(url_for("main.admin_dashboard"))

    application_record = application.query.get_or_404(application_id)
    return render_template(
        "admin-application-detail.html",
        application_type=application_type,
        application=application_record,
        return_url=url_for(
            "main.admin_dashboard",
            type=request.args.get("type", "all"),
            status=request.args.get("status", "all"),
        ),
    )


@main_bp.get("/admin/uploads/<string:category>/<path:filename>")
@login_required
def admin_upload_download(category: str, filename: str):
    allowed_categories = {"food-vendor", "sponsorship"}
    if category not in allowed_categories:
        abort(404)

    upload_root = current_app.config["UPLOAD_FOLDER"]
    directory = os.path.join(upload_root, category)
    return send_from_directory(directory, filename, as_attachment=True)


@main_bp.post("/admin/status/<string:application_type>/<int:application_id>")
@login_required
def admin_update_status(application_type: str, application_id: int):
    status = request.form.get("status", "new")
    model_map = {
        "sponsor": SponsorshipApplication,
        "vendor": FoodVendorApplication,
        "liability": LiabilityApplication,
    }
    model = model_map.get(application_type)
    if not model:
        flash("Unknown application type.", "error")
        return redirect(url_for("main.admin_dashboard"))

    application = model.query.get_or_404(application_id)
    application.status = status
    db.session.commit()
    flash("Status updated.", "success")
    return redirect(
        url_for(
            "main.admin_dashboard",
            type=request.args.get("type", "all"),
            status=request.args.get("status", "all"),
        )
    )
