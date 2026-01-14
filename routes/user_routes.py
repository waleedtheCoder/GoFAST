from flask import Blueprint, request, jsonify
from models import User

user_routes = Blueprint('user_routes', __name__)

@user_routes.route('/register', methods=['POST'])
def register_user():
    data = request.json
    try:
        User.create_user(
            name=data['name'],
            email=data['email'],
            password=data['password'],
            role=data['role'],
            carDetails=data.get('carDetails'),
            license=data.get('license')
        )
        return jsonify({'message': 'User registered successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@user_routes.route('/users', methods=['GET'])
def get_users():
    try:
        users = User.get_all_users()
        return jsonify([dict(zip([column[0] for column in users.description], row)) for row in users]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
