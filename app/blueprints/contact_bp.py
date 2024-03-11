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
    data = request.json
    user_email = get_jwt_identity()  # Get user email from JWT token
    user = User.query.filter_by(email=user_email).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404

    cv_email = data.get('cv_email')
    phone = data.get('phone')
    address = data.get('address')
    social_links = json.dumps(data.get('social_links'))  # Serialize the dictionary to JSON string

    try:
        contact = Contact(
            user_id=user.id,
            user_email=user.email,
            cv_email=cv_email,
            phone=phone,
            address=address,
            social_links=social_links
        )
        db.session.add(contact)
        db.session.commit()
        return jsonify({'message': 'Contact created successfully'}), 201
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({'message': 'An error occurred while creating contact', 'error': str(e)}), 500


# Route for updating an existing contact
import json

# Route for updating an existing contact
@contact_bp.route('/contacts/<int:contact_id>', methods=['PATCH', 'PUT'])
@jwt_required()
def update_contact(contact_id):
    data = request.json
    user_email = get_jwt_identity()

    # Retrieve the user associated with the JWT token
    user = User.query.filter_by(email=user_email).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404

    # Retrieve the contact to be updated
    contact = Contact.query.get(contact_id)
    if not contact:
        return jsonify({'message': 'Contact not found'}), 404

    # Ensure the user owns the contact
    if contact.user_id != user.id:
        return jsonify({'message': 'Unauthorized'}), 401

    # Update the contact fields
    try:
        # Convert social_links to JSON string
        social_links = json.dumps(data.get('social_links', {}))

        contact.cv_email = data.get('cv_email', contact.cv_email)
        contact.phone = data.get('phone', contact.phone)
        contact.address = data.get('address', contact.address)
        contact.social_links = social_links  # Assign the JSON string

        db.session.commit()
        return jsonify({'message': 'Contact updated successfully'}), 200
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({'message': 'An error occurred while updating contact', 'error': str(e)}), 500

# Route for fetching a single contact
@contact_bp.route('/contacts/<int:contact_id>', methods=['GET'])
@jwt_required()
def get_contact(contact_id):
    user_email = get_jwt_identity()

    # Retrieve the user associated with the JWT token
    user = User.query.filter_by(email=user_email).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404

    # Retrieve the contact
    contact = Contact.query.filter_by(id=contact_id, user_id=user.id).first()
    if not contact:
        return jsonify({'message': 'Contact not found'}), 404

    # Construct the response
    contact_data = {
        'id': contact.id,
        'cv_email': contact.cv_email,
        'phone': contact.phone,
        'address': contact.address,
        'social_links': json.loads(contact.social_links) if contact.social_links else {},
        'user_id': contact.user_id,
        'user_email': contact.user_email

    }

    return jsonify(contact_data), 200
