from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db, User, References

references_bp = Blueprint('references_bp', __name__)

# Create a new reference
@references_bp.route('/references', methods=['POST'])
@jwt_required()
def create_reference():
    try:
        current_user_email = get_jwt_identity()

        # Retrieve user based on email
        user = User.query.filter_by(email=current_user_email).first()
        
        # Check if user exists
        if not user:
            return jsonify({'message': 'User not found'}), 404

        data = request.json
        user_id = user.id

        reference = References(
            user_id=user_id,
            user_email=current_user_email,
            name=data.get('name'),
            job_title=data.get('job_title'),
            organization=data.get('organization'),
            email=data.get('email'),
            phone=data.get('phone')
        )
        db.session.add(reference)
        db.session.commit()

        return jsonify({'message': 'Reference created successfully'}), 201
    except Exception as e:
        return jsonify({'message': str(e)}), 500

# Update an existing reference
@references_bp.route('/references/<int:reference_id>', methods=['PATCH', 'PUT'])
@jwt_required()
def update_reference(reference_id):
    try:
        current_user_email = get_jwt_identity()

        # Retrieve reference based on id
        reference = References.query.get(reference_id)
        if not reference:
            return jsonify({'message': 'Reference not found'}), 404

        # Check if the reference belongs to the current user
        if current_user_email != reference.user_email:
            return jsonify({'message': 'Unauthorized'}), 401

        data = request.json
        reference.name = data.get('name', reference.name)
        reference.job_title = data.get('job_title', reference.job_title)
        reference.organization = data.get('organization', reference.organization)
        reference.email = data.get('email', reference.email)
        reference.phone = data.get('phone', reference.phone)

        db.session.commit()

        return jsonify({'message': 'Reference updated successfully'}), 201
    except Exception as e:
        return jsonify({'message': str(e)}), 500

# Delete a reference
@references_bp.route('/references/<int:reference_id>', methods=['DELETE'])
@jwt_required()
def delete_reference(reference_id):
    try:
        current_user_email = get_jwt_identity()

        # Retrieve reference based on id
        reference = References.query.get(reference_id)
        if not reference:
            return jsonify({'message': 'Reference not found'}), 404

        # Check if the reference belongs to the current user
        if current_user_email != reference.user_email:
            return jsonify({'message': 'Unauthorized'}), 401

        db.session.delete(reference)
        db.session.commit()

        return jsonify({'message': 'Reference deleted successfully'}), 201
    except Exception as e:
        return jsonify({'message': str(e)}), 500

# Get a specific reference by its ID
@references_bp.route('/references/<int:reference_id>', methods=['GET'])
@jwt_required()
def get_reference(reference_id):
    try:
        current_user_email = get_jwt_identity()

        # Retrieve reference based on id
        reference = References.query.get(reference_id)
        if not reference:
            return jsonify({'message': 'Reference not found'}), 404

        # Check if the reference belongs to the current user
        if current_user_email != reference.user_email:
            return jsonify({'message': 'Unauthorized'}), 401

        reference_data = {
            'id': reference.id,
            'user_id': reference.user_id,
            'user_email': reference.user_email,
            'name': reference.name,
            'job_title': reference.job_title,
            'organization': reference.organization,
            'email': reference.email,
            'phone': reference.phone
        }

        return jsonify(reference_data), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500

# Get all references for the current user
@references_bp.route('/references', methods=['GET'])
@jwt_required()
def get_all_references():
    try:
        current_user_email = get_jwt_identity()

        references = References.query.filter_by(user_email=current_user_email).all()
        if not references:
            return jsonify({'message': 'No references found for the user'}), 404

        references_data = []
        for reference in references:
            references_data.append({
                'id': reference.id,
                'user_id': reference.user_id,
                'user_email': reference.user_email,
                'name': reference.name,
                'job_title': reference.job_title,
                'organization': reference.organization,
                'email': reference.email,
                'phone': reference.phone
            })

        return jsonify(references_data), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500
