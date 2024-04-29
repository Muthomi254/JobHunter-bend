from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db,User, Skills

skills_bp = Blueprint('skills_bp', __name__)

# Create a new skill
@skills_bp.route('/skills', methods=['POST'])
@jwt_required()
def create_skill():
    try:
        current_user_email = get_jwt_identity()

        # Retrieve user based on email
        user = User.query.filter_by(email=current_user_email).first()
        
        # Check if user exists
        if not user:
            return jsonify({'message': 'User not found'}), 404

        data = request.json
        print(data)
        user_email = current_user_email  # Using current user's email
        skill = data.get('skill')
        info = data.get('info')
        skill_level = data.get('skill_level')

        if not skill:
            return jsonify({'message': 'Skill is required'}), 400

        new_skill = Skills(user_email=user_email, skill=skill, info=info, skill_level=skill_level)
        db.session.add(new_skill)
        db.session.commit()

        return jsonify({'message': 'Skill created successfully'}), 201

    except Exception as e:
        print(str(e))
        return jsonify({'message': str(e)}), 500


# Fetch all skills for the current user
@skills_bp.route('/skills', methods=['GET'])
@jwt_required()
def get_all_skills():
    current_user_email = get_jwt_identity()
    skills = Skills.query.filter_by(user_email=current_user_email).all()

    if not skills:
        return jsonify({'message': 'No skills found for the user'}), 404

    skills_data = [{
        'id': skill.id,
        'user_email': skill.user_email,
        'skill': skill.skill,
        'info': skill.info,
        'skill_level': skill.skill_level
    } for skill in skills]

    return jsonify(skills_data), 200

# Fetch a specific skill by its ID
@skills_bp.route('/skills/<int:skill_id>', methods=['GET'])
@jwt_required()
def get_skill(skill_id):
    current_user_email = get_jwt_identity()
    skill = Skills.query.get(skill_id)

    if not skill:
        return jsonify({'message': 'Skill not found'}), 404

    if current_user_email != skill.user_email:
        return jsonify({'message': 'Unauthorized'}), 401

    skill_data = {
        'id': skill.id,
        'user_email': skill.user_email,
        'skill': skill.skill,
        'info': skill.info,
        'skill_level': skill.skill_level
    }

    return jsonify(skill_data), 200

# Update a skill
@skills_bp.route('/skills/<int:skill_id>', methods=['PATCH', 'PUT'])
@jwt_required()
def update_skill(skill_id):
    current_user_email = get_jwt_identity()
    data = request.json
    skill = Skills.query.get(skill_id)

    if not skill:
        return jsonify({'message': 'Skill not found'}), 404

    if current_user_email != skill.user_email:
        return jsonify({'message': 'Unauthorized'}), 401

    # Update the skill
    if 'skill' in data:
        skill.skill = data['skill']
    if 'info' in data:
        skill.info = data['info']
    if 'skill_level' in data:
        skill.skill_level = data['skill_level']

    db.session.commit()

    return jsonify({'message': 'Skill updated successfully'}), 200

# Delete a skill
@skills_bp.route('/skills/<int:skill_id>', methods=['DELETE'])
@jwt_required()
def delete_skill(skill_id):
    current_user_email = get_jwt_identity()
    skill = Skills.query.get(skill_id)

    if not skill:
        return jsonify({'message': 'Skill not found'}), 404

    if current_user_email != skill.user_email:
        return jsonify({'message': 'Unauthorized'}), 401

    db.session.delete(skill)
    db.session.commit()

    return jsonify({'message': 'Skill deleted successfully'}), 200
