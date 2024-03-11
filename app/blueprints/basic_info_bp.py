from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db, BasicInfo, User
from sqlalchemy.exc import IntegrityError
import base64
import binascii


basic_info_bp = Blueprint('basic_info_bp', __name__)


# Route for creating BasicInfo
@basic_info_bp.route('/basic-info', methods=['POST'])
@jwt_required()  # Require JWT authentication for creating BasicInfo
def create_basic_info():
    data = request.json
    user_email = get_jwt_identity()  # Get user email from JWT token
    user = User.query.filter_by(email=user_email).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404

    # Check if BasicInfo already exists for the user
    if BasicInfo.query.filter_by(user_id=user.id).first():
        return jsonify({'message': 'BasicInfo already exists for this user'}), 400

    try:
        image_data_str = data.get('image_data', '')
        try:
            # Decode base64-encoded image data
            image_data = base64.b64decode(image_data_str)
        except binascii.Error as e:
            return jsonify({'message': 'Invalid image data', 'error': str(e)}), 400

        basic_info = BasicInfo(
            user_id=user.id,
            user_email=user.email,
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            job_title=data.get('job_title'),
            date_of_birth=data.get('date_of_birth'),
            nationality=data.get('nationality'),
            passport_id=data.get('passport_id'),
            gender=data.get('gender'),
            image_data=image_data
        )
        db.session.add(basic_info)
        db.session.commit()
        return jsonify({'message': 'BasicInfo created successfully'}), 201
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({'message': 'An error occurred while creating BasicInfo', 'error': str(e)}), 500


# Route for updating BasicInfo
@basic_info_bp.route('/basic-info/<int:basic_info_id>', methods=['PATCH', 'PUT'])
@jwt_required()  # Require JWT authentication for updating BasicInfo
def update_basic_info(basic_info_id):
    data = request.json
    basic_info = BasicInfo.query.get(basic_info_id)
    if not basic_info:
        return jsonify({'message': 'BasicInfo not found'}), 404

    try:
        # Only allow updates if the user owns the BasicInfo
        if basic_info.user_email != get_jwt_identity():
            return jsonify({'message': 'Unauthorized'}), 401

        basic_info.first_name = data.get('first_name', basic_info.first_name)
        basic_info.last_name = data.get('last_name', basic_info.last_name)
        basic_info.job_title = data.get('job_title', basic_info.job_title)
        basic_info.date_of_birth = data.get('date_of_birth', basic_info.date_of_birth)
        basic_info.nationality = data.get('nationality', basic_info.nationality)
        basic_info.passport_id = data.get('passport_id', basic_info.passport_id)
        basic_info.gender = data.get('gender', basic_info.gender)
        basic_info.image_data = base64.b64decode(data.get('image_data', ''))  # Decode base64-encoded image data

        db.session.commit()
        return jsonify({'message': 'BasicInfo updated successfully'}), 200
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({'message': 'An error occurred while updating BasicInfo', 'error': str(e)}), 500


# Route for fetching basic info
@basic_info_bp.route('/basic-info/<int:basic_info_id>', methods=['GET'])
@jwt_required()  # Require JWT authentication for fetching BasicInfo
def fetch_basic_info(basic_info_id):
    # Get the user email from the JWT token
    user_email = get_jwt_identity()
    
    # Retrieve the basic info by ID
    basic_info = BasicInfo.query.filter_by(id=basic_info_id).first()
    if not basic_info:
        return jsonify({'message': 'BasicInfo not found'}), 404

    # Ensure that the user owns the basic info
    if basic_info.user_email != user_email:
        return jsonify({'message': 'Unauthorized'}), 401

    # Convert binary image data to base64-encoded string
    image_data_base64 = base64.b64encode(basic_info.image_data).decode('utf-8') if basic_info.image_data else None

    # Return the basic info along with the user email and base64-encoded image data
    return jsonify({
        'user_email': basic_info.user_email,
        'first_name': basic_info.first_name,
        'last_name': basic_info.last_name,
        'job_title': basic_info.job_title,
        'date_of_birth': str(basic_info.date_of_birth),  # Convert date to string for JSON serialization
        'nationality': basic_info.nationality,
        'passport_id': basic_info.passport_id,
        'gender': basic_info.gender,
        'image_data': image_data_base64
    }), 200