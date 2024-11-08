from flask import render_template, request, redirect, url_for, Blueprint, session, flash
from werkzeug.security import check_password_hash
from utils.db import db
from model.user import user as user_data
from model.post import blogpost
from model.otp import otp as o
import random, string

B_user = Blueprint("B_user", __name__)


def users_count():
    total = 0
    userss = (user_data.query.order_by(user_data.user_id.desc())).all()
    for each in userss:
        if each.user_id > total:
            total = each.user_id

    return total


def generate_random_code():
    # Define the characters to choose from (letters and digits)
    characters = string.ascii_letters + string.digits
    # Generate a random 8-character code
    random_code = "".join(random.choice(characters) for _ in range(8))
    return random_code


@B_user.route("/")
def index():
    db.create_all()
    if "user" in session:
        return redirect(url_for("admin_B.admin"))
    return render_template("index.html")


@B_user.route("/register", methods=["POST", "GET"])
def register():
    if "user" in session:
        return redirect(url_for("B_user.index"))
    return render_template("sign_in.html")


@B_user.route("/signup", methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        email = request.form["email"]
        name = request.form["name"]
        password = request.form["password"]
        is_verified = "no"

        existing_user = user_data.query.filter_by(email=email).first()
        if existing_user:
            flash("User with this email already exists.")
        else:
            # Check if a user with the same name already exists
            existing_user_by_name = user_data.query.filter_by(name=name).first()
            if existing_user_by_name:
                flash("User with this name already exists.")
                return redirect(url_for("B_user.signup"))
            else:
                user_id = 1 + users_count()
                code = generate_random_code()
                session["user_id"] = user_id
                users = user_data(email, password, user_id, name, is_verified)
                OTP = o(otp=code, user_id=user_id)
                db.session.add(users)
                db.session.commit()
                db.session.add(OTP)
                db.session.commit()

            return redirect(url_for("B_user.is_verified"))

    return redirect(url_for("B_user.register", mode="signup"))


@B_user.route("/login", methods=["POST", "GET"])
def signin():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        try:
            user = user_data.query.filter_by(email=email).first()
            if check_password_hash(user.pswd, password):
                session["user_id"] = user.user_id
                if user.is_verified == "yes":
                    session["user"] = user.name
                    if "track" in session:
                        return redirect(url_for(session["track"]))
                    return redirect(url_for("B_user.index"))
                else:
                    return redirect(url_for("B_user.is_verified"))
            else:
                flash("Invalid credentials ")
                return redirect(url_for("B_user.register", mode="login"))
        except:
            flash("User doesn't exist! ")
            return redirect(url_for("B_user.register", mode="signup"))

    return redirect(url_for("B_user.register", mode="login"))


@B_user.route("/is_verified", methods=["POST", "GET"])
def is_verified():
    if "user_id" in session:
        user_id = session["user_id"]
        if request.method == "POST":
            R_code = request.form["code"]
            try:
                code = o.query.filter_by(user_id=user_id).first()
                if code.otp == R_code:
                    user = user_data.query.filter_by(user_id=user_id).first()
                    user.is_verified = "yes"
                    db.session.commit()
                    flash("Account verified")
                    return redirect(url_for("B_user.register", mode="login"))
                else:
                    flash("That didn't work, try again")
            except:
                return "something went wrong"
        return render_template("verify.html")
    return redirect(url_for("B_user.register", mode="login"))


@B_user.route("/logout")
def logout():
    session.pop("user", None)
    session.pop("user_id", None)
    session.pop("message", None)
    session.pop("track", None)
    return redirect(url_for("B_user.index"))


@B_user.route("/contact")
def contact():
    return render_template("contact.html")
