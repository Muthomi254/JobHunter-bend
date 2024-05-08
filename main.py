from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from decouple import config
from flask_jwt_extended import JWTManager
from app.models import db, User, RevokedToken, LanguageLevel
from flask_cors import CORS  # Import CORS
from flask_restful import Resource, Api
from flask_swagger_ui import get_swaggerui_blueprint
import json
from app.blueprints.auth_bp import Register, ForgotPassword, Login, Logout, DeleteAccount
from app.blueprints.basic_info_bp import BasicInfo


app = Flask(__name__)
api = Api(app)


# Configure database URI from environment variable
app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URI')
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


# Add resources to the API
#auth
api.add_resource(Register, '/register')
api.add_resource(ForgotPassword, '/forgot-password')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(DeleteAccount, '/delete-account')
# BasicInfo
# api.add_resource(BasicInfo, '/basic-info', '/basic-info/<int:basic_info_id>')


# importing blueprints
from app.blueprints.auth_bp import auth_blueprint  # Import auth_blueprint from its file
from app.blueprints.basic_info_bp import basic_info_bp, BasicInfo
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


SWAGGER_URL = '/swagger'
API_URL = '/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': "Job HunterAPI Documentation"}
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)



@app.route('/swagger.json')
def swagger():
    with open('swagger.json', 'r') as f:
        return jsonify(json.load(f))




if __name__ == '__main__':
    app.run(debug=True)