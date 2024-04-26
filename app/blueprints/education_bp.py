from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db,User, Education
from datetime import datetime


education_bp = Blueprint('education_bp', __name__)

# Create education entry
@education_bp.route('/education', methods=['POST'])
@jwt_required()  # Require JWT authentication for creating Education
def create_education():
    try:
        # Get user email from JWT token
        user_email = get_jwt_identity()
        
        # Retrieve user based on email
        user = User.query.filter_by(email=user_email).first()
        
        # Check if user exists
        if not user:
            return jsonify({'message': 'User not found'}), 404

        # Proceed with creating education entry
        
        data = request.json
        print(data)
        user_id = user.id  # Use the user ID from the retrieved user

        # If end date is not provided or is in the future, set it to today's date
        end_date = data.get('end_date')
        if not end_date:
            end_date = datetime.today().date()
        else:
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            if end_date > datetime.today().date():
                end_date = datetime.today().date()

        education = Education(
            user_id=user_id,
            user_email=user_email,
            course_title=data.get('course_title'),
            institution=data.get('institution'),
            city=data.get('city'),
            country=data.get('country'),
            start_date=data.get('start_date'),
            end_date=end_date,
            description=data.get('description')
        )
        db.session.add(education)
        db.session.commit()

        return jsonify({'message': 'Education entry created successfully'}), 201
    except Exception as e:
        # Handle exceptions
        return jsonify({'message': 'An error occurred', 'error': str(e)}), 500






# Get all education entries for a user
@education_bp.route('/education', methods=['GET'])
@jwt_required()
def get_all_education():
    current_user_email = get_jwt_identity()

    education_entries = Education.query.filter_by(user_email=current_user_email).all()
    if not education_entries:
        return jsonify({'message': 'No education entries found for the user'}), 404

    education_data = []
    for entry in education_entries:
        education_data.append({
            'id': entry.id,
            'user_id': entry.user_id,
            'user_email': entry.user_email,
            'course_title': entry.course_title,
            'institution': entry.institution,
            'city': entry.city,
            'country': entry.country,
            'start_date': str(entry.start_date),  # Convert date to string for JSON serialization
            'end_date': str(entry.end_date),      # Convert date to string for JSON serialization
            'description': entry.description
        })

    return jsonify(education_data), 200

# Get a specific education entry by its ID
@education_bp.route('/education/<int:education_id>', methods=['GET'])
@jwt_required()
def get_education(education_id):
    current_user_email = get_jwt_identity()

    education_entry = Education.query.get(education_id)
    if not education_entry:
        return jsonify({'message': 'Education entry not found'}), 404

    # Check if the education entry belongs to the current user
    if current_user_email != education_entry.user_email:
        return jsonify({'message': 'Unauthorized'}), 401

    education_data = {
        'id': education_entry.id,
        'user_id': education_entry.user_id,
        'user_email': education_entry.user_email,
        'course_title': education_entry.course_title,
        'institution': education_entry.institution,
        'city': education_entry.city,
        'country': education_entry.country,
        'start_date': str(education_entry.start_date),  # Convert date to string for JSON serialization
        'end_date': str(education_entry.end_date),      # Convert date to string for JSON serialization
        'description': education_entry.description
    }

    return jsonify(education_data), 200

    
# Update education entry
@education_bp.route('/education/<int:education_id>', methods=['PATCH', 'PUT'])
@jwt_required()
def update_education(education_id):
    current_user_email = get_jwt_identity()

    data = request.json

    education_entry = Education.query.get(education_id)
    if not education_entry:
        return jsonify({'message': 'Education entry not found'}), 404

    # Check if the education entry belongs to the current user
    if current_user_email != education_entry.user_email:
        return jsonify({'message': 'Unauthorized'}), 401

    # Update the education entry
    education_entry.course_title = data.get('course_title', education_entry.course_title)
    education_entry.institution = data.get('institution', education_entry.institution)
    education_entry.city = data.get('city', education_entry.city)
    education_entry.country = data.get('country', education_entry.country)
    education_entry.start_date = data.get('start_date', education_entry.start_date)
    education_entry.end_date = data.get('end_date', education_entry.end_date)
    education_entry.description = data.get('description', education_entry.description)

    # Validate start date and end date
    if education_entry.start_date > education_entry.end_date:
        return jsonify(print({'message': 'Start date cannot be greater than end date'})), 400

    db.session.commit()

    return jsonify({'message': 'Education entry updated successfully'}), 200



# Delete education entry
@education_bp.route('/education/<int:education_id>', methods=['DELETE'])
@jwt_required()
def delete_education(education_id):
    current_user_email = get_jwt_identity()

    education_entry = Education.query.get(education_id)
    if not education_entry:
        return jsonify({'message': 'Education entry not found'}), 404

    # Check if the education entry belongs to the current user
    if current_user_email != education_entry.user_email:
        return jsonify({'message': 'Unauthorized'}), 401

    db.session.delete(education_entry)
    db.session.commit()

    return jsonify({'message': 'Education entry deleted successfully'}), 200
