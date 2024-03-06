from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import db, User, Profile, Languages, Courses, ProfessionalExperience, Skills, References
from decouple import config



# Initialize Flask application
app = Flask(__name__)

# Configure database URI from environment variable
app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy with the Flask app
db.init_app(app)
migrate = Migrate(app, db)



if __name__ == '__main__':
    app.run(debug=True)
