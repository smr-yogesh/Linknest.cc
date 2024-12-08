from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
    flash,
    session,
    abort,
)
from utils.db import db
from datetime import datetime
from model.short import short as sh
from routes.user import generate_random_code

short = Blueprint("short", __name__)


# url shortner adding route
@short.route("/short")
def shor_t():
    if "user" in session:
        shorts = sh.query.filter_by(user_id=session["user_id"]).all()
        return render_template("shortner.html", shorts=shorts)
    session["track"] = "posts_B.a_p"
    flash("! Please login first !")
    return redirect(url_for("B_user.register", mode="login"))


@short.route("/st", methods=["POST"])  # URL shortner
def st():
    user_id = session["user_id"]
    title = request.form["title"]
    url = request.form["url"]
    short = generate_random_code()

    send = sh(user_id=user_id, title=title, url=url, short=short)
    db.session.add(send)
    db.session.commit()

    return redirect(url_for("admin_B.admin"))


@short.route("/s/<sht>")
def short_link(sht):
    # Fetch links for the username
    short_url = sh.query.filter_by(short=sht).one_or_none()
    url = short_url.url

    # If user does not exist, return 404 error
    if not short_url:
        abort(404)

    # Render the template with user links
    return redirect(url)
