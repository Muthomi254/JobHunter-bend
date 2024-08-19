from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db, Contact, User
from sqlalchemy.exc import IntegrityError
import json

contact_bp = Blueprint('contact_bp', __name__)

# Route for creating a new contact
@contact_bp.route('/contacts', methods=['POST'])
@jwt_required()
def create_contact():
    # Extract data from request JSON
    data = request.json
    user_email = get_jwt_identity()
    user = User.query.filter_by(email=user_email).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404

    try:
        # Extract platform names and social links separately
        platforms = [platform_data['platform_name'] for platform_data in data.get('social_media', [])]
        social_links = [platform_data['social_links'] for platform_data in data.get('social_media', [])]

        # Concatenate all platform names into a single string
        platform_name = ','.join(platforms)

        # Concatenate all social links into a single string
        social_links_str = ','.join(social_links)
        
        # Create a new contact with concatenated platform names and social links
        contact = Contact(
            user_id=user.id,
            user_email=user.email,
            cv_email=data.get('cv_email'),
            phone=data.get('phone'),
            address=data.get('address'),
            platform_name=platform_name,
            social_links=social_links_str
        )
        db.session.add(contact)
        db.session.commit()
        return jsonify({'message': 'Contact created successfully'}), 201
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({'message': 'An error occurred while creating contact', 'error': str(e)}), 500

# Route for updating an existing contact
@contact_bp.route('/contacts/<int:contact_id>', methods=['PATCH', 'PUT'])
@jwt_required()
def update_contact(contact_id):
    # Extract data from request JSON
    data = request.json
    print(data)
    user_email = get_jwt_identity()
    user = User.query.filter_by(email=user_email).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404

    try:
        contact = Contact.query.get(contact_id)
        if not contact:
            return jsonify({'message': 'Contact not found'}), 404

        # Ensure the user owns the contact
        if contact.user_id != user.id:
            return jsonify({'message': 'Unauthorized'}), 401

        # Extract platform names and social links separately
        platforms = [platform_data['platform_name'] for platform_data in data.get('social_media', [])]
        social_links = [platform_data['social_links'] for platform_data in data.get('social_media', [])]

        # Concatenate all platform names into a single string
        platform_name = ','.join(platforms)

        # Concatenate all social links into a single string
        social_links_str = ','.join(social_links)

        # Update the contact fields
        contact.cv_email = data.get('cv_email', contact.cv_email)
        contact.phone = data.get('phone', contact.phone)
        contact.address = data.get('address', contact.address)
        contact.platform_name = platform_name
        contact.social_links = social_links_str

        db.session.commit()
        return jsonify({'message': 'Contact updated successfully'}), 200
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({'message': 'An error occurred while updating contact', 'error': str(e)}), 500

# Route for fetching a single contact
@contact_bp.route('/contacts/<int:contact_id>', methods=['GET'])
@jwt_required()
def get_contact(contact_id):
    # Fetch user and contact data
    user_email = get_jwt_identity()
    user = User.query.filter_by(email=user_email).first()
    if not user:
        return jsonify({'message': 'User not found'}), 200

    contact = Contact.query.get(contact_id)
    if not contact:
        return jsonify({'message': 'Contact not found'}), 404

    # Construct response data
    contact_data = {
        'id': contact.id,
        'cv_email': contact.cv_email,
        'phone': contact.phone,
        'address': contact.address,
        'platform_name': contact.platform_name,
        'social_links': contact.social_links
    }

    # print(contact_data)

    return jsonify(contact_data), 200

# Route for fetching all contacts by user email
@contact_bp.route('/contacts', methods=['GET'])
@jwt_required()
def get_contacts():
    # Fetch user and contact data
    user_email = get_jwt_identity()
    user = User.query.filter_by(email=user_email).first()
    if not user:
        return jsonify({'message': 'User not found'}), 200

    contacts = Contact.query.filter_by(user_email=user.email).all()

    # Construct response data
    contacts_data = []
    for contact in contacts:
        contact_data = {
            'id': contact.id,
            'cv_email': contact.cv_email,
            'phone': contact.phone,
            'address': contact.address,
            'platform_name': contact.platform_name,
            'social_links': contact.social_links,
            'user_id': contact.user_id,
            'user_email': contact.user_email
        }
        contacts_data.append(contact_data)
        # print(contact_data)

    return jsonify(contacts_data), 200


# Route for deleting a contact
@contact_bp.route('/contacts/<int:contact_id>', methods=['DELETE'])
@jwt_required()
def delete_contact(contact_id):
    user_email = get_jwt_identity()

    # Retrieve the user associated with the JWT token
    user = User.query.filter_by(email=user_email).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404

    # Retrieve the contact to be deleted
    contact = Contact.query.get(contact_id)
    if not contact:
        return jsonify({'message': 'Contact not found'}), 404

    # Ensure the user owns the contact
    if contact.user_id != user.id:
        return jsonify({'message': 'Unauthorized'}), 401

    try:
        # Delete the contact
        db.session.delete(contact)
        db.session.commit()
        return jsonify({'message': 'Contact deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'An error occurred while deleting contact', 'error': str(e)}), 500
