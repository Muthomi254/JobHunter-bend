from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db,User, Languages, LanguageLevel
from enum import Enum

languages_bp = Blueprint('languages_bp', __name__)

# Create a new language
@languages_bp.route('/languages', methods=['POST'])
@jwt_required()
def create_language():
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
        language = data.get('language')
        additional_info = data.get('additional_info')
        language_level = data.get('language_level')

        # Convert language level to uppercase
        language_level = language_level.upper()
        print("Language Level:", language_level)  # Add this line for debugging

        if not language:
            return jsonify({'message': 'Language is required'}), 400

        new_language = Languages(
            user_id=user.id,  # Use user.id instead of user_id from request
            user_email=user_email,
            language=language,
            additional_info=additional_info,
            language_level=language_level
        )
        db.session.add(new_language)
        db.session.commit()

        return jsonify({'message': 'Language created successfully'}), 201
    except Exception as e:
        print("An error occurred:", e)
        return jsonify({'message': 'An error occurred', 'error': str(e)}), 500



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


# Get all language levels
@languages_bp.route('/language-levels', methods=['GET'])
def get_language_levels():
    language_levels = [level.value for level in LanguageLevel]
    return jsonify(language_levels), 200