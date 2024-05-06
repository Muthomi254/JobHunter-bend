from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db, User, ProfessionalExperience

experience_bp = Blueprint('experience_bp', __name__)

# Create experience entry
@experience_bp.route('/experience', methods=['POST'])
@jwt_required()
def create_experience():
    try:
        # Get user email from JWT token
        user_email = get_jwt_identity()
        
        # Retrieve user based on email
        user = User.query.filter_by(email=user_email).first()
        
        # Check if user exists
        if not user:
            return jsonify({'message': 'User not found'}), 404

        data = request.json
        print(data)

     

        experience = ProfessionalExperience(
            user_email=user_email,
            user_id=user.id,
            employer=data.get('employer'),
            job_title=data.get('job_title'),
            city=data.get('city'),
            country=data.get('country'),
            start_date=data.get('start_date'),
            end_date=data.get('end_date'),
            description=data.get('description')
        )
        db.session.add(experience)
        db.session.commit()

        return jsonify({'message': 'ProfessionalExperience entry created successfully'}), 201

    except Exception as e:
        print("An error occurred:", str(e))
        return jsonify({'message': 'An error occurred', 'error': str(e)}), 500


# Get all experience entries for a user
@experience_bp.route('/experience', methods=['GET'])
@jwt_required()
def get_all_experience():
    current_user_email = get_jwt_identity()

    experience_entries = ProfessionalExperience.query.filter_by(user_email=current_user_email).all()
    if not experience_entries:
        return jsonify({'message': 'No experience entries found for the user'}), 404

    experience_data = []
    for entry in experience_entries:
        experience_data.append({
            'id': entry.id,
            'user_email': entry.user_email,
            'user_id': entry.user_id,
            'employer': entry.employer,
            'job_title': entry.job_title,
            'city': entry.city,
            'country': entry.country,
            'start_date': str(entry.start_date),  # Convert date to string for JSON serialization
            'end_date': str(entry.end_date),      # Convert date to string for JSON serialization
            'description': entry.description
        })

    return jsonify(experience_data), 200

# Get a specific experience entry by its ID
@experience_bp.route('/experience/<int:experience_id>', methods=['GET'])
@jwt_required()
def get_experience(experience_id):
    current_user_email = get_jwt_identity()

    experience_entry = ProfessionalExperience.query.get(experience_id)
    if not experience_entry:
        return jsonify({'message': 'ProfessionalExperience entry not found'}), 404

    # Check if the experience entry belongs to the current user
    if current_user_email != experience_entry.user_email:
        return jsonify({'message': 'Unauthorized'}), 401

    experience_data = {
        'id': experience_entry.id,
        'user_email': experience_entry.user_email,
        'user_id': experience_entry.user_id,
        'employer': experience_entry.employer,
        'job_title': experience_entry.job_title,
        'city': experience_entry.city,
        'country': experience_entry.country,
        'start_date': str(experience_entry.start_date),  # Convert date to string for JSON serialization
        'end_date': str(experience_entry.end_date),      # Convert date to string for JSON serialization
        'description': experience_entry.description
    }

    return jsonify(experience_data), 200

# Update experience entry
@experience_bp.route('/experience/<int:experience_id>', methods=['PATCH', 'PUT'])
@jwt_required()
def update_experience(experience_id):
    current_user_email = get_jwt_identity()

    data = request.json

    experience_entry = ProfessionalExperience.query.get(experience_id)
    if not experience_entry:
        return jsonify({'message': 'ProfessionalExperience entry not found'}), 404

    # Check if the experience entry belongs to the current user
    if current_user_email != experience_entry.user_email:
        return jsonify({'message': 'Unauthorized'}), 401

    # Update the experience entry
    experience_entry.employer = data.get('employer', experience_entry.employer)
    experience_entry.job_title = data.get('job_title', experience_entry.job_title)
    experience_entry.city = data.get('city', experience_entry.city)
    experience_entry.country = data.get('country', experience_entry.country)
    experience_entry.start_date = data.get('start_date', experience_entry.start_date)
    experience_entry.end_date = data.get('end_date', experience_entry.end_date)
    experience_entry.description = data.get('description', experience_entry.description)

    db.session.commit()

    return jsonify({'message': 'ProfessionalExperience entry updated successfully'}), 200

# Delete experience entry
@experience_bp.route('/experience/<int:experience_id>', methods=['DELETE'])
@jwt_required()
def delete_experience(experience_id):
    current_user_email = get_jwt_identity()

    experience_entry = ProfessionalExperience.query.get(experience_id)
    if not experience_entry:
        return jsonify({'message': 'ProfessionalExperience entry not found'}), 404

    # Check if the experience entry belongs to the current user
    if current_user_email != experience_entry.user_email:
        return jsonify({'message': 'Unauthorized'}), 401

    db.session.delete(experience_entry)
    db.session.commit()

    return jsonify({'message': 'ProfessionalExperience entry deleted successfully'}), 200
