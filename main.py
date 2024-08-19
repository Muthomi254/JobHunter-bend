from flask import Flask, request, jsonify
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from decouple import config
from flask_jwt_extended import JWTManager
from app.models import db, User, RevokedToken, LanguageLevel
from flask_cors import CORS  # Import CORS


app = Flask(__name__)

# Configure database URI from environment variable
# app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URI')  # cv_app database link (jdbc:postgresql://localhost:5432/postgres) for render('postgresql://jobhunter_user:4t0frPRG3Io18RPn6QKZdyAwAOjlzGGU@dpg-cotsrfgcmk4c73a2lbig-a.oregon-postgres.render.com/jobhunter'

# Configure database URI to use SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///job_hunter.db'  # SQLite database file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['JWT_SECRET_KEY'] = config('JWT_SECRET_KEY')  # Secret key for JWT
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 24 * 3600  # Set expiration time to 1 day (24 hours) in seconds

# Initialize SQLAlchemy with the Flask app
db.init_app(app)
migrate = Migrate(app, db)

# Register JWT extension with Flask app
jwt = JWTManager(app)

# Initialize CORS extension
CORS(app)  # This will allow CORS for all routes. You can customize further if needed.

# importing blueprints
from app.blueprints.auth_bp import auth_blueprint  # Import auth_blueprint from its file
from app.blueprints.basic_info_bp import basic_info_bp
from app.blueprints.contact_bp import contact_bp
from app.blueprints.profile_bp import profile_bp  
from app.blueprints.languages_bp import languages_bp
from app.blueprints.education_bp import education_bp  
from app.blueprints.experience_bp import experience_bp  
from app.blueprints.skills_bp import skills_bp
from app.blueprints.references_bp import references_bp





# Register authentication blueprint with Flask app
app.register_blueprint(auth_blueprint)
app.register_blueprint(basic_info_bp)
app.register_blueprint(contact_bp)
app.register_blueprint(profile_bp) 
app.register_blueprint(languages_bp)
app.register_blueprint(education_bp) 
app.register_blueprint(experience_bp)
app.register_blueprint(skills_bp)
app.register_blueprint(references_bp)







if __name__ == '__main__':
    app.run(debug=True)