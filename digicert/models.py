from digicert import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    # Create a table in the db
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
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

    __tablename__ = 'event'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    slug = db.Column(db.String(64), index=True)
    description = db.Column(db.Text)
    logo = db.Column(db.Text)
    mode = db.Column(db.String(32))
    created_date = db.Column(db.Date)
    ending_date = db.Column(db.Date)

    def __init__(self, title, description, logo, mode, ending_date):
        self.title = title
        self.slug = '-'.join(title.split())
        self.description = description
        self.logo = logo
        self.mode = mode
        self.created_date = datetime.utcnow().date()
        self.ending_date = datetime.strptime(ending_date, '%d.%m.%y')


class Certificate(db.Model):
    __tablename__ = 'certificate'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    slug = db.Column(db.String(32), index=True)
    obtained_date = db.Column(db.Date)
    description = db.Column(db.Text)
    cert_img = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, obtained_date, description, cert_img, user_id):
        self.title = title
        self.slug = '-'.join(title.split())
        self.obtained_date = datetime.strptime(obtained_date, '%d.%m.%y')
        self.description = description
        self.cert_img = cert_img
        self.user_id = user_id
