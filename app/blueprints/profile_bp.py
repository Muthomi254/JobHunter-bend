from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db, User, Profile

profile_bp = Blueprint('profile_bp', __name__)

@profile_bp.route('/profile', methods=['POST'])
@jwt_required()
def create_profile():
    try:
        # Get user email from JWT token
        user_email = get_jwt_identity()
        
        # Retrieve user based on email
        user = User.query.filter_by(email=user_email).first()
        
        # Check if user exists
        if not user:
            return jsonify({'message': 'User not found'}), 404

        data = request.json
        description = data.get('description')

        # Check if description is provided
        if not description:
            return jsonify({'message': 'Description is required'}), 400

        # Check if the user_email matches the email associated with the retrieved user
        if user_email != user.email:
            return jsonify({'message': 'Unauthorized'}), 401

        # Create a new profile
        profile = Profile(user_id=user.id, user_email=user_email, description=description)
        db.session.add(profile)
        db.session.commit()

        return jsonify({'message': 'Profile created successfully'}), 201

    except Exception as e:
        print("An error occurred:", e)
        return jsonify({'message': 'An error occurred'}), 500




@profile_bp.route('/profile/<int:profile_id>', methods=['GET'])
@jwt_required()
def get_profile(profile_id):
    current_user_email = get_jwt_identity()

    profile = Profile.query.get(profile_id)
    if not profile:
        return jsonify({'message': 'Profile not found'}), 404

    if current_user_email != profile.user_email:
        return jsonify({'message': 'Unauthorized'}), 401

    profile_data = {
        'id': profile.id,
        'user_id': profile.user_id,
        'user_email': profile.user_email,
        'description': profile.description
    }

    return jsonify(profile_data), 200

@profile_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profiles():
    try:
        current_user_email = get_jwt_identity()

        # Retrieve profiles belonging to the current user
        profiles = Profile.query.filter_by(user_email=current_user_email).all()

        # Check if any profiles exist for the user
        if not profiles:
            return jsonify({'message': 'No profiles found for the user'}), 404

        # Prepare profile data
        profile_data = []
        for profile in profiles:
            profile_data.append({
                'id': profile.id,
                'user_id': profile.user_id,
                'user_email': profile.user_email,
                'description': profile.description
            })

        return jsonify(profile_data), 200

    except Exception as e:
        print("An error occurred:", e)
        return jsonify({'message': 'Unauthorized'}), 401



@profile_bp.route('/profile/<int:profile_id>', methods=['PATCH', 'PUT'])
@jwt_required()
def update_profile(profile_id):
    current_user_email = get_jwt_identity()

    profile = Profile.query.get(profile_id)
    if not profile:
        return jsonify({'message': 'Profile not found'}), 404

    if current_user_email != profile.user_email:
        return jsonify({'message': 'Unauthorized'}), 401

    data = request.json
    description = data.get('description')

    if description:
        profile.description = description
        db.session.commit()
        return jsonify({'message': 'Profile updated successfully'}), 200
    else:
        return jsonify({'message': 'No data provided for updating'}), 400

@profile_bp.route('/profile/<int:profile_id>', methods=['DELETE'])
@jwt_required()
def delete_profile(profile_id):
    current_user_email = get_jwt_identity()

    profile = Profile.query.get(profile_id)
    if not profile:
        return jsonify({'message': 'Profile not found'}), 404

    if current_user_email != profile.user_email:
        return jsonify({'message': 'Unauthorized'}), 401

    db.session.delete(profile)
    db.session.commit()
    return jsonify({'message': 'Profile deleted successfully'}), 200
