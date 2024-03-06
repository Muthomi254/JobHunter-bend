from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    email = db.Column(db.String(255), primary_key=True)
    password_hash = db.Column(db.String(255))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

class BasicInfo(db.Model):
    __tablename__ = 'basic_info'
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(255), db.ForeignKey('user.email'), nullable=False)
    full_name = db.Column(db.String(255))
    job_title = db.Column(db.String(255))
    date_of_birth = db.Column(db.Date)
    nationality = db.Column(db.String(255))
    passport_id = db.Column(db.String(255))
    gender = db.Column(db.String(255))

class Contact(db.Model):
    __tablename__ = 'contact'
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(255), db.ForeignKey('user.email'), nullable=False)
    email = db.Column(db.String(255), unique=True)
    phone = db.Column(db.String(20))
    address = db.Column(db.String(255))
    social_links = db.Column(db.String(255))
