from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import LargeBinary
from enum import Enum

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password_hash = db.Column(db.String(255))

  

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
    cv_email = db.Column(db.String(255))
    phone = db.Column(db.String(20))
    address = db.Column(db.String(255))
    social_links = db.Column(db.String(255))

class Profile(db.Model):
    __tablename__ = 'profile'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    user_email = db.Column(db.String(255), db.ForeignKey('user.email'), nullable=False)
    description = db.Column(db.Text)


class LanguageLevel(Enum):
    NOVICE = 'Novice'
    INTERMEDIATE = 'Intermediate'
    FLUENT = 'Fluent'
    ADVANCED = 'Advanced'

class Languages(db.Model):
    __tablename__ = 'languages'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False) 
    user_email = db.Column(db.String(255), db.ForeignKey('user.email'), nullable=False)
    language = db.Column(db.String(255))
    additional_info = db.Column(db.Text)
    language_level = db.Column(db.Enum(LanguageLevel), nullable=False)

class Education(db.Model):
    __tablename__ = 'education'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    user_email = db.Column(db.String(255), db.ForeignKey('user.email'), nullable=False)
    course_title = db.Column(db.String(255))
    institution = db.Column(db.String(255))
    city = db.Column(db.String(255))
    country = db.Column(db.String(255))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    description = db.Column(db.Text)

class ProfessionalExperience(db.Model):
    __tablename__ = 'professional_experience'
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(255), db.ForeignKey('user.email'), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    employer = db.Column(db.String(255))
    job_title = db.Column(db.String(255))
    city = db.Column(db.String(255))
    country = db.Column(db.String(255))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    description = db.Column(db.Text)

class Skills(db.Model): #In the frontend, it will be a drop down with fixed values
    __tablename__ = 'skills'
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(255), db.ForeignKey('user.email'), nullable=False)
    skill = db.Column(db.String(255))
    info = db.Column(db.Text)
    skill_level = db.Column(db.String(255))

class References(db.Model):
    __tablename__ = 'references'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    user_email = db.Column(db.String(255), db.ForeignKey('user.email'), nullable=False)
    name = db.Column(db.String(255))
    job_title = db.Column(db.String(255))
    organization = db.Column(db.String(255))
    email = db.Column(db.String(255))
    phone = db.Column(db.String(20))

