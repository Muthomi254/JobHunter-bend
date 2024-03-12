from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db,User, Languages, LanguageLevel
from enum import Enum

languages_bp = Blueprint('languages_bp', __name__)

# Create a new language
@languages_bp.route('/languages', methods=['POST'])
@jwt_required()
def create_language():
    current_user_email = get_jwt_identity()

    data = request.json
    user_id = data.get('user_id')
    user_email = data.get('user_email')
    language = data.get('language')
    additional_info = data.get('additional_info')
    language_level = data.get('language_level')

    if not user_id or not user_email or not language:
        return jsonify({'message': 'User ID, email, and language are required'}), 400

    # Check if user id and email match the current user
    if current_user_email != user_email:
        return jsonify({'message': 'Unauthorized'}), 401

    # Check if user id and email exist in the database
    user = User.query.filter_by(id=user_id, email=user_email).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404

    new_language = Languages(
        user_id=user_id,
        user_email=user_email,
        language=language,
        additional_info=additional_info,
        language_level=language_level
    )
    db.session.add(new_language)
    db.session.commit()

    return jsonify({'message': 'Language created successfully'}), 201

# Get all languages for a user
@languages_bp.route('/languages', methods=['GET'])
@jwt_required()
def get_all_languages():
    current_user_email = get_jwt_identity()

    languages = Languages.query.filter_by(user_email=current_user_email).all()
    if not languages:
        return jsonify({'message': 'No languages found for the user'}), 404

    languages_data = []
    for language in languages:
        languages_data.append({
            'id': language.id,
            'user_id': language.user_id,
            'user_email': language.user_email,
            'language': language.language,
            'additional_info': language.additional_info,
            'language_level': language.language_level.value  # Convert enum to its value (string)
        })

    return jsonify(languages_data), 200

# Get a specific language by its ID
@languages_bp.route('/languages/<int:language_id>', methods=['GET'])
@jwt_required()
def get_language(language_id):
    current_user_email = get_jwt_identity()

    language = Languages.query.get(language_id)
    if not language:
        return jsonify({'message': 'Language not found'}), 404

    if current_user_email != language.user_email:
        return jsonify({'message': 'Unauthorized'}), 401

    language_data = {
        'id': language.id,
        'user_id': language.user_id,
        'user_email': language.user_email,
        'language': language.language,
        'additional_info': language.additional_info,
        'language_level': language.language_level.value  # Convert enum to its value (string)
    }

    return jsonify(language_data), 200

    
# Update a language
@languages_bp.route('/languages/<int:language_id>', methods=['PATCH' ,'PUT'])
@jwt_required()
def update_language(language_id):
    current_user_email = get_jwt_identity()

    language = Languages.query.get(language_id)
    if not language:
        return jsonify({'message': 'Language not found'}), 404

    if current_user_email != language.user_email:
        return jsonify({'message': 'Unauthorized'}), 401

    data = request.json
    language.language = data.get('language', language.language)
    language.additional_info = data.get('additional_info', language.additional_info)
    language.language_level = data.get('language_level', language.language_level)

    db.session.commit()

    return jsonify({'message': 'Language updated successfully'}), 200

# Delete a language
@languages_bp.route('/languages/<int:language_id>', methods=['DELETE'])
@jwt_required()
def delete_language(language_id):
    current_user_email = get_jwt_identity()

    language = Languages.query.get(language_id)
    if not language:
        return jsonify({'message': 'Language not found'}), 404

    if current_user_email != language.user_email:
        return jsonify({'message': 'Unauthorized'}), 401

    db.session.delete(language)
    db.session.commit()

    return jsonify({'message': 'Language deleted successfully'}), 200
