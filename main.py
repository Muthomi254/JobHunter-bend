from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from decouple import config
from flask_jwt_extended import JWTManager
from app.models import db, User, RevokedToken
from flask_cors import CORS  # Import CORS


app = Flask(__name__)

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

# importing blueprints
from app.blueprints.auth_bp import auth_blueprint  # Import auth_blueprint from its file

# Register authentication blueprint with Flask app
app.register_blueprint(auth_blueprint)

if __name__ == '__main__':
    app.run(debug=True)