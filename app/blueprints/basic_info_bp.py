from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db, BasicInfo, User
import base64
import binascii
from sqlalchemy.exc import IntegrityError, ProgrammingError
import logging

basic_info_bp = Blueprint('basic_info_bp', __name__)


@basic_info_bp.route('/basic-info', methods=['POST'])
@jwt_required()  # Require JWT authentication for creating BasicInfo
def create_basic_info():
    try:
        data = request.json
        print("Received data:", data)  # Print received data
        # Ensure all required fields are present in the request JSON data
        required_fields = ['first_name', 'last_name', 'job_title', 'date_of_birth', 'nationality', 'passport_id', 'gender', 'image_data']
        if not all(field in data for field in required_fields):
            return jsonify({'message': 'Required fields are missing in the request data'}), 400

        user_email = get_jwt_identity()  # Get user email from JWT token
        user = User.query.filter_by(email=user_email).first()
        if not user:
            return jsonify({'message': 'User not found'}), 404

        # Check if BasicInfo already exists for the user
        if BasicInfo.query.filter_by(user_id=user.id).first():
            return jsonify({'message': 'BasicInfo already exists for this user'}), 400

        image_data_str = data.get('image_data', '')  # Get the image data as a string
        print("Received image data:", image_data_str)  # Print received image data
        try:
            # Decode base64-encoded image data
            image_data = base64.b64decode(image_data_str)
            print("Decoded image data length:", len(image_data))  # Print length of decoded image data
        except binascii.Error as e:
            print("An error occurred:", e)
            return jsonify({'message': 'Invalid image data: ' + str(e)}), 400
           

        basic_info = BasicInfo(
            user_id=user.id,
            user_email=user.email,
            first_name=data['first_name'],
            last_name=data['last_name'],
            job_title=data['job_title'],
            date_of_birth=data['date_of_birth'],
            nationality=data['nationality'],
            passport_id=data['passport_id'],
            gender=data['gender'],
            image_data=image_data
        )
        db.session.add(basic_info)
        db.session.commit()
        return jsonify({'message': 'BasicInfo created successfully'}), 201
    except IntegrityError as e:
        db.session.rollback()
        error_message = 'An error occurred while creating BasicInfo: {}'.format(str(e))
        logging.error(error_message)  # Log the error
        return jsonify({'message': error_message}), 500
    except ProgrammingError as e:
        error_message = 'An error occurred while executing the SQL query: {}'.format(str(e))
        print(str(e))  
        return jsonify({'message': error_message}), 500



# Route for updating BasicInfo
@basic_info_bp.route('/basic-info', methods=['PATCH', 'PUT'])
@jwt_required()  # Require JWT authentication for updating BasicInfo
def update_basic_info():
    try:
        data = request.json
        image_data_str = data.get('image_data', '')
        try:
            # Decode base64-encoded image data
            image_data = base64.b64decode(image_data_str)
        except binascii.Error as e:
            return jsonify({'message': 'Invalid image data: ' + str(e)}), 400

        print('Decoded image data:', image_data)  # Log the decoded image data

        user_email = get_jwt_identity()

        basic_info = BasicInfo.query.filter_by(user_email=user_email).first()
        if not basic_info:
            return jsonify({'message': 'BasicInfo not found'}), 404

        # Ensure all required fields are present in the request form data
        required_fields = ['first_name', 'last_name', 'job_title', 'date_of_birth', 'nationality', 'passport_id', 'gender']
        if not all(field in data for field in required_fields):
            return jsonify({'message': 'Required fields are missing in the request data'}), 400

        # Update BasicInfo fields with the received data
        basic_info.first_name = data.get('first_name', basic_info.first_name)
        basic_info.last_name = data.get('last_name', basic_info.last_name)
        basic_info.job_title = data.get('job_title', basic_info.job_title)
        basic_info.date_of_birth = data.get('date_of_birth', basic_info.date_of_birth)
        basic_info.nationality = data.get('nationality', basic_info.nationality)
        basic_info.passport_id = data.get('passport_id', basic_info.passport_id)
        basic_info.gender = data.get('gender', basic_info.gender)

        if image_data:
            # Assign the decoded image data to the basic_info object
            basic_info.image_data = image_data

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

# Route for fetching basic info by user email
@basic_info_bp.route('/basic-info', methods=['GET'])
@jwt_required()  # Require JWT authentication for fetching BasicInfo
def fetch_basic_info_by_email():
    # Get the user email from the JWT token
    user_email = get_jwt_identity()
    
    # Retrieve the basic info associated with the user's email
    basic_info = BasicInfo.query.filter_by(user_email=user_email).first()
    if not basic_info:
        return jsonify({'message': 'BasicInfo not found'}), 404

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
