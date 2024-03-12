from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db, Profile

profile_bp = Blueprint('profile_bp', __name__)

@profile_bp.route('/profile', methods=['POST'])
@jwt_required()
def create_profile():
    current_user_email = get_jwt_identity()

    data = request.json
    user_id = data.get('user_id')
    user_email = data.get('user_email')
    description = data.get('description')

    if not user_id or not user_email:
        return jsonify({'message': 'User ID and email are required'}), 400

    if current_user_email != user_email:
        return jsonify({'message': 'Unauthorized'}), 401

    profile = Profile(user_id=user_id, user_email=user_email, description=description)
    db.session.add(profile)
    db.session.commit()

    return jsonify({'message': 'Profile created successfully'}), 201


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
