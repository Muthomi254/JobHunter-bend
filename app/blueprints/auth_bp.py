from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token,  jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash
from app.models import db, User, RevokedToken
from sqlalchemy.exc import IntegrityError

auth_blueprint = Blueprint('auth', __name__)

from flask import request, jsonify

@auth_blueprint.route('/register', methods=['POST'])
def register():
    data = request.get_json()  # Get JSON data from request
    print("Request Data:", data)  # Debug print statement

    # Check if JSON data is provided and contains 'email' and 'password' keys
    if not data or 'email' not in data or 'password' not in data:
        return jsonify({'message': 'Email and password are required'}), 400

    email = data['email']
    password = data['password']

    # Check if the email already exists in the database
    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'Email already exists'}), 400

    # Create a new user with the provided email and password
    user = User(email=email)
    user.password = password
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201


@auth_blueprint.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'message': 'Email and password are required'}), 400

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({'message': 'Invalid email or password'}), 401

    access_token = create_access_token(identity=user.email)
    return jsonify({'access_token': access_token}), 200

@auth_blueprint.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    try:
        # Get the current user's identity from the JWT token (email)
        current_user_email = get_jwt_identity()

        # Query the User model to get the user by email
        user = User.query.filter_by(email=current_user_email).first()

        # Extract JTI from the JWT token
        auth_header = request.headers.get('Authorization')
        jti = auth_header.split()[1] if auth_header else None

        if user and jti:
            # Check if the token is already revoked
            existing_token = RevokedToken.query.filter_by(jti=jti).first()
            if existing_token:
                return jsonify({'message': 'User already Logged Out'}), 400

            # Add the JTI to the revoked tokens list
            revoked_token = RevokedToken(jti=jti, user_id=user.id)
            db.session.add(revoked_token)
            db.session.commit()

        return jsonify({'message': 'Logged out successfully'}), 200

    except IntegrityError as e:
        # Handle IntegrityError, which may occur if the JTI is already in the database
        db.session.rollback()
        return jsonify({'message': 'An error occurred while logging out', 'error': str(e)}), 500

    except Exception as e:
        # Handle other common errors
        return jsonify({'message': 'An error occurred while logging out', 'error': str(e)}), 500

