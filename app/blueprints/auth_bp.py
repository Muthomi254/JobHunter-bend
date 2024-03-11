from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token,  jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash, generate_password_hash
from app.models import db, User, RevokedToken
from sqlalchemy.exc import IntegrityError


auth_blueprint = Blueprint('auth', __name__)


@auth_blueprint.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or 'email' not in data or 'password' not in data:
        return jsonify({'message': 'Email and password are required'}), 400

    email = data['email']
    password = data['password']

    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'Email already exists'}), 400

    hashed_password = generate_password_hash(password)
    user = User(email=email, password_hash=hashed_password)
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201

@auth_blueprint.route('/forgot-password', methods=['POST'])
def forgot_password():
    data = request.json
    email = data.get('email')
    new_password = data.get('new_password')
    confirm_password = data.get('confirm_password')

    if not email:
        return jsonify({'message': 'Email address is required'}), 400

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({'message': 'User with that email address does not exist'}), 404

    if new_password != confirm_password:
        return jsonify({'message': 'Passwords do not match'}), 400

    hashed_password = generate_password_hash(new_password)
    user.password_hash = hashed_password
    db.session.commit()

    return jsonify({'message': 'Password reset successfully'}), 200

@auth_blueprint.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'message': 'Email and password are required'}), 400

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({'message': 'Invalid email or password'}), 401

    if not check_password_hash(user.password_hash, password):
        return jsonify({'message': 'Invalid email or password'}), 401

    access_token = create_access_token(identity=user.email)
    return jsonify({'access_token': access_token}), 200

@auth_blueprint.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    try:
        current_user_email = get_jwt_identity()
        user = User.query.filter_by(email=current_user_email).first()
        auth_header = request.headers.get('Authorization')
        jti = auth_header.split()[1] if auth_header else None

        if user and jti:
            existing_token = RevokedToken.query.filter_by(jti=jti).first()
            if existing_token:
                return jsonify({'message': 'User already Logged Out'}), 400

            revoked_token = RevokedToken(jti=jti, user_id=user.id)
            db.session.add(revoked_token)
            db.session.commit()

        return jsonify({'message': 'Logged out successfully'}), 200

    except IntegrityError as e:
        db.session.rollback()
        return jsonify({'message': 'An error occurred while logging out', 'error': str(e)}), 500

    except Exception as e:
        return jsonify({'message': 'An error occurred while logging out', 'error': str(e)}), 500

@auth_blueprint.route('/delete-account', methods=['DELETE'])
@jwt_required()
def delete_account():
    try:
        current_user_email = get_jwt_identity()
        user = User.query.filter_by(email=current_user_email).first()

        if not user:
            return jsonify({'message': 'User not found'}), 404

        # Delete associated revoked tokens
        RevokedToken.query.filter_by(user_id=user.id).delete()
        
        db.session.delete(user)
        db.session.commit()

        return jsonify({'message': 'User account deleted successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'An error occurred while deleting the user account', 'error': str(e)}), 500
