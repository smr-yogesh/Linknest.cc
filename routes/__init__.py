import re
from flask import Flask
from utils.db import db

app = Flask(__name__)


app = Flask(__name__, static_url_path="", static_folder=r"../static")

app.template_folder = "../templates"
app.secret_key = "super secret key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog.db"

# Email configuration
app.config["MAIL_SERVER"] = "smtp.gmail.com"  # mail server
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = "your_email@gmail.com"
app.config["MAIL_PASSWORD"] = "your_password"


db.init_app(app)
