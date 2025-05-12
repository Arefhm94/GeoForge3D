from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from models import User
from utils import create_token

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    new_user = User(
        username=data['username'],
        password=generate_password_hash(data['password'], method='sha256')
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and check_password_hash(user.password, data['password']):
        token = create_token(user.id)
        return jsonify({'token': token}), 200
    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/profile', methods=['GET'])
def profile():
    token = request.headers.get('Authorization').split(" ")[1]
    user_id = verify_token(token)  # Assuming a function to verify token
    user = User.query.get(user_id)
    return jsonify({'username': user.username}), 200

if __name__ == '__main__':
    app.run(debug=True)