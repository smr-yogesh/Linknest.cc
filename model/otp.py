from utils.db import db
from datetime import datetime


class otp(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    otp = db.Column(db.String(8))
    user_id = db.Column(db.Integer)
