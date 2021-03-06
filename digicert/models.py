from digicert import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), unique=True, index=True, nullable=False)
    username = db.Column(db.String(64), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False, default=datetime.now())
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    profile_pic = db.Column(db.Text, nullable=True)
    certificates = db.relationship("Certificate")

    def __init__(self, first_name, last_name, email, username, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Event(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    slug = db.Column(db.String(64), index=True, unique=True)
    description = db.Column(db.Text)
    logo = db.Column(db.Text)
    logo_mimetype = db.Column(db.Text)
    mode = db.Column(db.String(32))
    created_date = db.Column(db.Date)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)

    def __init__(self, title, description, logo, logo_mimetype, mode, end_date, start_date):
        self.title = title
        self.slug = ('-'.join(title.split())).lower() + '-' + datetime.now().strftime('%m-%d-%Y-%H-%M-%S')
        self.description = description
        self.logo = logo
        self.logo_mimetype = logo_mimetype
        self.mode = mode
        self.created_date = datetime.utcnow().date()
        self.start_date = start_date
        self.end_date = end_date


class Certificate(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    slug = db.Column(db.String(32), index=True, unique=True)
    obtained_date = db.Column(db.Date)
    description = db.Column(db.Text)
    cert_img = db.Column(db.Text)
    cert_img_mimetype = db.Column(db.Text)
    cert_type = db.Column(db.String(16))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, obtained_date, description, cert_img, cert_img_mimetype, cert_type, user_id):
        self.title = title
        self.slug = ('-'.join(title.split())).lower() + '-' + datetime.now().strftime('%m-%d-%Y-%H-%M-%S')
        self.obtained_date = obtained_date
        self.description = description
        self.cert_img = cert_img
        self.cert_img_mimetype = cert_img_mimetype
        self.cert_type = cert_type
        self.user_id = user_id
