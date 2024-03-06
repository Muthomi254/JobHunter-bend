from sqlalchemy import create_engine, Column, Integer, String, Date, Text, ForeignKey
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, validates
from flask_login import UserMixin


db = SQLAlchemy()


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    # Add other user fields as needed

    @validates('email')
    def validate_email(self, key, email):
        # Check if email is already registered
        if User.query.filter(User.email == email).first():
            raise ValueError('Email is already registered.')
        return email

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        try:
            self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        except Exception as e:
            raise ValueError('Error occurred while hashing password: {}'.format(str(e)))

    def verify_password(self, password):
        try:
            return bcrypt.check_password_hash(self.password_hash, password)
        except Exception as e:
            raise ValueError('Error occurred while verifying password: {}'.format(str(e)))


class Profile(db.Model, UserMixin):
    __tablename__ = 'profile'

    profile_id = Column(Integer, primary_key=True)
    full_name = Column(String(100), nullable=False)
    job_title = Column(String(100))
    email = Column(String(100))
    phone = Column(String(20))
    address = Column(String(255))
    date_of_birth = Column(Date)
    nationality = Column(String(50))
    passport_id = Column(String(20))
    gender = Column(String(10))
    social_links = Column(Text)  # Store as JSONB or TEXT
    description = Column(Text)
    image = Column(String(255))  # Path to the image file or URL

    languages = relationship("Languages", back_populates="profile")
    courses = relationship("Courses", back_populates="profile")
    professional_experience = relationship("ProfessionalExperience", back_populates="profile")
    skills = relationship("Skills", back_populates="profile")
    references = relationship("References", back_populates="profile")

class Languages(db.Model, UserMixin):
    __tablename__ = 'languages'

    language_id = Column(Integer, primary_key=True)
    profile_id = Column(Integer, ForeignKey('profile.profile_id'))
    language = Column(String(50))
    additional_info = Column(Text)
    language_level = Column(String(20))

    profile = relationship("Profile", back_populates="languages")

class Courses(db.Model, UserMixin):
    __tablename__ = 'courses'

    course_id = Column(Integer, primary_key=True)
    profile_id = Column(Integer, ForeignKey('profile.profile_id'))
    course_title = Column(String(100))
    institution = Column(String(100))
    city = Column(String(100))
    country = Column(String(100))
    start_date = Column(Date)
    end_date = Column(Date)
    description = Column(Text)

    profile = relationship("Profile", back_populates="courses")

class ProfessionalExperience(db.Model, UserMixin):
    __tablename__ = 'professional_experience'

    experience_id = Column(Integer, primary_key=True)
    profile_id = Column(Integer, ForeignKey('profile.profile_id'))
    employer = Column(String(100))
    job_title = Column(String(100))
    city = Column(String(100))
    country = Column(String(100))
    start_date = Column(Date)
    end_date = Column(Date)
    description = Column(Text)

    profile = relationship("Profile", back_populates="professional_experience")

class Skills(db.Model, UserMixin):
    __tablename__ = 'skills'

    skill_id = Column(Integer, primary_key=True)
    profile_id = Column(Integer, ForeignKey('profile.profile_id'))
    skill = Column(String(100))
    info = Column(Text)
    skill_level = Column(String(20))

    profile = relationship("Profile", back_populates="skills")

class References(db.Model, UserMixin):
    __tablename__ = 'references'

    reference_id = Column(Integer, primary_key=True)
    profile_id = Column(Integer, ForeignKey('profile.profile_id'))
    name = Column(String(100))
    job_title = Column(String(100))
    organization = Column(String(100))
    email = Column(String(100))
    phone = Column(String(20))

    profile = relationship("Profile", back_populates="references")

# Example usage:
# engine = create_engine('postgresql://username:password@localhost:5432/database_name')
# Base.metadata.create_all(engine)