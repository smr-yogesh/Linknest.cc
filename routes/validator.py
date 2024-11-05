from flask import jsonify, request, Blueprint
from model.user import user as u

validator = Blueprint("validator", __name__)


# Check if email is taken
@validator.route("/check_email", methods=["POST"])
def check_email():
    email = request.json.get("email")
    user = u.query.filter_by(email=email).first()
    if user:
        return jsonify({"exists": True, "message": "Email is already in use."})
    return jsonify({"exists": False, "message": "Email is available."})


# Check if name is taken
@validator.route("/check_name", methods=["POST"])
def check_name():
    name = request.json.get("name")
    user = u.query.filter_by(name=name).first()
    if user:
        return jsonify({"exists": True, "message": "Name is already in use."})
    return jsonify({"exists": False, "message": "Name is available."})
