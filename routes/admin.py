from flask import render_template, request, redirect, url_for, Blueprint, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from utils.db import db
from datetime import datetime
from model.links import links
from model.user import user as u
from model.otp import otp
from routes.validator import send_mail
from routes.user import generate_random_code
import os

admin_B = Blueprint("admin_B", __name__)


def getid():
    # Retrieves the current user's ID from the session
    uid = session["user_id"]
    return uid


@admin_B.route("/dashboard")  # Admin URL rename to dashboard
def admin():
    # Checks if a user is logged in
    if "user" in session:
        # Retrieves all blog posts for the logged-in user
        posts = links.query.filter_by(user_id=getid()).all()
        # Renders the dashboard page with the user's posts and session user info
        return render_template("dashboard.html", posts=posts, user=session["user"])

    # If not logged in, flashes a warning and redirects to login
    flash("! Please login first !")
    return redirect(url_for("B_user.register", mode="login"))


@admin_B.route("/settings")  # User settings
def settings():
    # Fetches the current user's data from the database
    user = u.query.filter_by(id=getid()).one_or_none()

    # Updates the session with the user's name
    session["user"] = user.name

    # Renders the settings page if the user is logged in
    if "user" in session:
        return render_template("settings.html", user=user)

    # If not logged in, flashes a warning and redirects to login
    flash("! Please login first !")
    return redirect(url_for("B_user.register", mode="login"))


@admin_B.route("/update", methods=["POST"])
def update():
    # Query the user to be updated
    user = u.query.filter_by(id=getid()).one_or_none()
    link = links.query.filter_by(id=getid()).one_or_none()

    # Updates the session with the user's name
    session["user"] = user.name

    # Handles the case where the user does not exist
    if not user:
        flash("User not found!", "message-error")
        return redirect(url_for("admin_B.admin"))

    # Updates the user's name if provided
    name = request.form.get("name")
    if name:
        user.name = name
        link.author = name

    # Updates the user's email if provided
    email = request.form.get("email")
    if email:
        user.email = email
        code = generate_random_code()
        if send_mail(email, code):
            OTP = otp.query.filter_by(id=getid()).one_or_none()
            OTP.otp = code
            user = u.query.filter_by(id=getid()).one_or_none()
            user.is_verified = "no"
            if db.session.commit():
                flash("Relogin and verify the email, code sent!", "message-success")

    # Updates the user's password if provided and the current password matches
    password = request.form.get("new_password")
    c_password = request.form.get("current_password")
    if password:
        # Verifies the current password before updating
        if check_password_hash(user.pswd, c_password):
            user.pswd = generate_password_hash(password)
        else:
            flash("Incorrect current password!!")
            return redirect(url_for("admin_B.settings"))

    # Saves the changes to the database
    db.session.commit()
    flash("Updated successfully!!", "message-success")
    return redirect(url_for("admin_B.settings"))
