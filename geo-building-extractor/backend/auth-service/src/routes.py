from flask import Blueprint, request, jsonify
from .models import User
from .utils import create_user, authenticate_user

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if create_user(username, password):
        return jsonify({"message": "User created successfully"}), 201
    return jsonify({"message": "User already exists"}), 400

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    token = authenticate_user(username, password)
    if token:
        return jsonify({"token": token}), 200
    return jsonify({"message": "Invalid credentials"}), 401

@auth_bp.route('/profile', methods=['GET'])
def profile():
    # This is a placeholder for user profile retrieval logic
    return jsonify({"message": "User profile data"}), 200