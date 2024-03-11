from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import LargeBinary

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password_hash = db.Column(db.String(255))

    # @property
    # def password(self):
    #     raise AttributeError('password is not a readable attribute')

    # @password.setter
    # def password(self, password):
    #     self.password_hash = generate_password_hash(password)

    # def verify_password(self, password):
    #     return check_password_hash(self.password_hash, password)

class RevokedToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(500), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)        

class BasicInfo(db.Model):
    __tablename__ = 'basic_info'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    user_email = db.Column(db.String(255), db.ForeignKey('user.email'), nullable=False)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    job_title = db.Column(db.String(255))
    date_of_birth = db.Column(db.Date)
    nationality = db.Column(db.String(255))
    passport_id = db.Column(db.String(255))
    gender = db.Column(db.String(255))
    image_data = db.Column(LargeBinary)

class Contact(db.Model):
    __tablename__ = 'contact'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    user_email = db.Column(db.String(255), db.ForeignKey('user.email'), nullable=False)
    phone = db.Column(db.String(20))
    address = db.Column(db.String(255))
    social_links = db.Column(db.String(255))
