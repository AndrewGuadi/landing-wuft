from flask import Blueprint, render_template

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


@main_bp.get("/food-vendor-application")
def food_vendor_application():
    return render_template("food-vendor-application.html")


@main_bp.get("/sponsorship-application")
def sponsorship_application():
    return render_template("sponsorship-application.html")


@main_bp.get("/liability-application")
def liability_application():
    return render_template("liability-application.html")
