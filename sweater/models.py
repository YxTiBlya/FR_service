from sweater import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)

class Contacts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(15), nullable=False)
    operator_code = db.Column(db.Integer, nullable=False)
    tag = db.Column(db.String(100), nullable=True)
    time_zone = db.Column(db.String(10), nullable=True)  # +time from GMT


class Mailings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False)
    message = db.Column(db.Text, nullable=False)
    filters = db.Column(db.String(200), nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)


class Messages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), nullable=True)
    mailing_id = db.Column(db.Integer, nullable=False)
    contact_id = db.Column(db.Integer, nullable=False)
