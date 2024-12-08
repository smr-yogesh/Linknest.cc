from utils.db import db
from datetime import datetime


class short(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    title = db.Column(db.String(300))
    url = db.Column(db.String(300))
    short = db.Column(db.String(8))
