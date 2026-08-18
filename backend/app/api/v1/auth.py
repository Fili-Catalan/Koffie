from flask import Blueprint
from flask import request
from flask import jsonify
import jwt
import os
import datetime

"""

We define our routes and other app components so they can be registered onto a Flask app later for
our authentication scheme.

"""

auth_bp = Blueprint('auth',__name__)

@auth_bp.route('/register', methods=['POST'])
def register():

    # Import statements located within function to prevent circular imports.
    from app import db
    from app.models.user import User
    from app import bcrypt

    # This is how incoming JSON data from a POST request is accessed. We get the JSON in the form of a dictionary.
    data = request.get_json()

    # Check that all inputs are provided.
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')

    if not email or not username or not password:
        return jsonify({'error': 'Password, email, and username are all required'}), 400

    # Query database to ensure that email and username have not been used/is available.
    email_check = User.query.filter_by(email=email).first()
    username_check = User.query.filter_by(username=username).first()

    if email_check is not None: return jsonify({'error': 'Account using this email already exists'}), 400
    if username_check is not None: return jsonify({'error': 'Username has already been used'}), 400

    # Hash the password. Converts bytes to string to store in database.
    password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    # Create a user account using our User SQLAlchemy model and store it in postgres
    new_user = User(email=email, username=username, password_hash=password_hash)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'success': 'Account successfully created'}), 201


@auth_bp.route('/login', methods=['POST'])
def login():

    from app import db
    from app.models.user import User
    from app import bcrypt

    data = request.get_json()

    # Check that all inputs are provided.
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Password and email are all required'}), 400

    # Check if there is a user account with that email.
    user = User.query.filter_by(email=email).first()
    if not user: return jsonify({'error': 'Invalid email or password'}), 401

    # Getting the password hash from the User object we accessed from the database.
    password_hash = user.password_hash

    # Password check.
    password_check = bcrypt.check_password_hash(password_hash, password)
    if not password_check:  return jsonify({'error':'Invalid email or password'}), 401

    # Return JWT.
    return jsonify({'token':jwt.encode(
        {'user_id': str(user.id), 'exp':datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=24)},
        os.environ.get('SECRET_KEY'),
        algorithm='HS256'
    )}), 200
