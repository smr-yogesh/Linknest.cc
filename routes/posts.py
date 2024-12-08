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
from model.links import links

posts_B = Blueprint("posts_B", __name__)


# This returns posts after being selected on index or from admin page.
@posts_B.route("/post/<int:post_id>")
def post(post_id):
    post = links.query.filter_by(id=post_id).one()
    try:
        return render_template("post.html", post=post)
    except:
        return render_template("post.html", post=post)


# post adding route
@posts_B.route("/addpost")
def a_p():
    if "user" in session:
        return render_template("addpost.html")
    session["track"] = "posts_B.a_p"
    flash("! Please login first !")
    return redirect(url_for("B_user.register", mode="login"))


# sends post to database.
@posts_B.route("/ap", methods=["POST"])
def ap():
    title = request.form["title"]
    author = request.form["author"]
    content = request.form["url"]
    media = request.form["media"]
    uid = session["user_id"]

    post = links(
        title=title,
        author=author,
        content=content,
        media=media,
        date_posted=datetime.now(),
        updated=None,
        user_id=uid,
    )

    db.session.add(post)
    db.session.commit()

    return redirect(url_for("admin_B.admin"))


# Post editing route.
@posts_B.route("/edit/", methods=["POST", "GET"])
def edit():
    try:
        post_id = request.form["edit_id"]
        post_to_edit = links.query.filter_by(id=post_id).one()
        return render_template("updatepost.html", post=post_to_edit)
    except:
        return redirect("/404")


# Updates/edits post
@posts_B.route("/update", methods=["POST"])
def update():
    post_id = request.form["edit_id"]
    title = request.form["title"]
    author = request.form["author"]
    content = request.form["url"]
    media = request.form["media"]
    word = content.split()

    post = links.query.filter_by(id=post_id).one()
    post.title = title
    post.author = author
    post.content = content
    post.media = media
    post.updated = datetime.now()
    db.session.commit()
    flash("Edited successfully!!", "message-success")
    return redirect(url_for("admin_B.admin"))


# Delete post
@posts_B.route("/delete", methods=["POST"])
def delete():
    id = request.form["del_id"]
    post_to_del = links.query.get_or_404(id)
    try:
        db.session.delete(post_to_del)
        db.session.commit()
        flash("Deleted successfully!!", "message-success")
    except:
        flash("something went wrong!!")
    return redirect(url_for("admin_B.admin"))


# This retuns the content based on the URL(Username probably)


@posts_B.route("/<username>")
def user_links(username):
    # Fetch links for the username
    posts = links.query.filter_by(author=username).all()

    # If user does not exist, return 404 error
    if not posts:
        abort(404)

    # Render the template with user links
    return render_template("user_links.html", username=username, posts=posts)
