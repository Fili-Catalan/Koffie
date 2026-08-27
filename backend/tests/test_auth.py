from app import create_app
from app import db
from app.models.user import User
import jwt
import pytest
import os
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
import uuid

# Load environment variables first before creating the test Flask app, since we don't want to 
# accidentally run our tests on our actual development database due to an ordering trap.
load_dotenv()

flask_app = create_app(database_url=os.environ.get('TEST_DATABASE_URL'), redis_url=os.environ.get('TEST_REDIS_URL'))
sample_register_credentials = {'email':'joe@koffie.com', 'password':'lemon', 'username':'Joe'}
sample_login_credentials = {'email':'joe@koffie.com', 'password':'lemon'}

@pytest.fixture
def tester():
    test_client = flask_app.test_client()
    with flask_app.app_context():
        db.drop_all()
        db.create_all()
    yield test_client

def test_no_header(tester):
    response = tester.get('/api/v1/auth/me')
    assert response.status_code == 401
    assert response.get_json() == {'error': 'Missing header'}

def test_valid_token(tester):
    future_time = datetime.now(timezone.utc) + timedelta(days=7, hours=3, minutes=30)
    test_payload = {'user_id':'test_user', 'exp':future_time}
    token = jwt.encode(payload=test_payload, key=os.environ.get('SECRET_KEY'), algorithm='HS256')
    response = tester.get('/api/v1/auth/me', headers={'Authorization':f'Bearer {token}'})
    assert response.status_code == 200
    assert response.get_json() == {'success': 'test_user is valid'}

def test_garbage_token(tester):
    response = tester.get('/api/v1/auth/me', headers={'Authorization':'Bearer garbage'})
    assert response.status_code == 401
    assert response.get_json() == {'error': 'Expired or Invalid Token'}

def test_register_missing_field(tester):
    credentials_json = {'email':'joe@koffie.com', 'password':'lemon'}
    response = tester.post('/api/v1/auth/register',json=credentials_json)
    assert response.status_code == 400
    assert response.get_json() == {'error': 'Password, email, and username are all required'}

def test_register_email_in_use(tester):
    # Create new user in test database
    credentials_json = {'email':'joe@koffie.com', 'password':'lemon', 'username':'Joe'}
    tester.post('/api/v1/auth/register',json=credentials_json)
    new_user_credentials_json = {'email':'joe@koffie.com', 'password':'lemon', 'username':'Java'}
    response = tester.post('/api/v1/auth/register',json=new_user_credentials_json)
    assert response.status_code == 400
    assert response.get_json() == {'error': 'Account using this email already exists'}

def test_register_username_in_use(tester):
    # Create new user in test database
    credentials_json = {'email':'joe@koffie.com', 'password':'lemon', 'username':'Joe'}
    tester.post('/api/v1/auth/register',json=credentials_json)
    new_user_credentials_json = {'email':'java@koffie.com', 'password':'lemon', 'username':'Joe'}
    response = tester.post('/api/v1/auth/register',json=new_user_credentials_json)
    assert response.status_code == 400
    assert response.get_json() == {'error':'Username has already been used'}

def test_register_successful_registration(tester):
    # Create new user in test database
    credentials_json = {'email':'joe@koffie.com', 'password':'lemon', 'username':'Joe'}
    response = tester.post('/api/v1/auth/register',json=credentials_json)
    assert response.status_code == 201
    assert response.get_json() == {'success': 'Account successfully created'}

def test_login_missing_field(tester):
    credentials_json = {'email':'joe@koffie.com'}
    response = tester.post('/api/v1/auth/login',json=credentials_json)
    assert response.status_code == 400
    assert response.get_json() == {'error': 'Password and email are all required'}

def test_login_unassociated_email(tester):
    credentials_json = {'email':'joe@koffie.com', 'password':'lemon'}
    response = tester.post('/api/v1/auth/login',json=credentials_json)
    assert response.status_code == 401
    assert response.get_json() == {'error': 'Invalid email or password'}

def test_login_wrong_password(tester):
    credentials_json = {'email':'joe@koffie.com', 'password':'lemon', 'username':'Joe'}
    tester.post('/api/v1/auth/register',json=credentials_json)
    credentials_wrong_password_json = {'email':'joe@koffie.com', 'password':'apple'}
    response = tester.post('/api/v1/auth/login', json=credentials_wrong_password_json)
    assert response.status_code == 401
    assert response.get_json() == {'error':'Invalid email or password'}

def test_login_successful_login(tester):
    credentials_json = {'email':'joe@koffie.com', 'password':'lemon', 'username':'Joe'}
    tester.post('/api/v1/auth/register',json=credentials_json)
    correct_credentials_json = {'email':'joe@koffie.com', 'password':'lemon'}
    response = tester.post('/api/v1/auth/login', json=correct_credentials_json)
    assert response.status_code == 200
    with flask_app.app_context():
        user = User.query.filter_by(email='joe@koffie.com').first()
        token = response.get_json()['token']
        decoded_payload = jwt.decode(token, os.environ.get('SECRET_KEY'), algorithms=['HS256'])
        assert uuid.UUID(decoded_payload['user_id']) == user.id

def test_refresh_invalid_token(tester):
    register_credentials_json = {'email':'joe@koffie.com', 'password':'lemon', 'username':'Joe'}
    tester.post('/api/v1/auth/register',json=register_credentials_json)
    credentials_json = {'email':'joe@koffie.com', 'password':'lemon'}
    tester.post('/api/v1/auth/login', json=credentials_json)
    refresh_credentials = {'refresh_token':'garbage refresh token'}
    response = tester.post('/api/v1/auth/refresh', json=refresh_credentials)
    assert response.status_code == 401
    assert response.get_json() == {'error': 'Invalid token'}

def test_refresh_valid_token(tester):
    register_credentials_json = {'email':'joe@koffie.com', 'password':'lemon', 'username':'Joe'}
    tester.post('/api/v1/auth/register',json=register_credentials_json)
    credentials_json = {'email':'joe@koffie.com', 'password':'lemon'}
    login_response = tester.post('/api/v1/auth/login', json=credentials_json)
    with flask_app.app_context():
        user = User.query.filter_by(email='joe@koffie.com').first()
        refresh_token = login_response.get_json()['refresh_token']
        refresh_credentials = {'refresh_token':refresh_token}
        refresh_response = tester.post('/api/v1/auth/refresh', json=refresh_credentials)
        token = refresh_response.get_json()['token']
        decoded_payload = jwt.decode(token, os.environ.get('SECRET_KEY'), algorithms=['HS256'])
        assert refresh_response.status_code == 200
        assert uuid.UUID(decoded_payload['user_id']) == user.id

def test_refresh_old_token_invalidated(tester):
    register_credentials_json = {'email':'joe@koffie.com', 'password':'lemon', 'username':'Joe'}
    tester.post('/api/v1/auth/register',json=register_credentials_json)
    credentials_json = {'email':'joe@koffie.com', 'password':'lemon'}
    login_response = tester.post('/api/v1/auth/login', json=credentials_json)

    # Old token post and response.
    old_refresh_token = login_response.get_json()['refresh_token']
    refresh_credentials = {'refresh_token':old_refresh_token}
    tester.post('/api/v1/auth/refresh', json=refresh_credentials)

    # Attempt to refresh with old token.
    response = tester.post('/api/v1/auth/refresh', json=refresh_credentials)
    assert response.status_code == 401
    assert response.get_json() == {'error':'Invalid token'}
    
def test_refresh_new_token_valid(tester):
    register_credentials_json = {'email':'joe@koffie.com', 'password':'lemon', 'username':'Joe'}
    tester.post('/api/v1/auth/register',json=register_credentials_json)
    credentials_json = {'email':'joe@koffie.com', 'password':'lemon'}
    login_response = tester.post('/api/v1/auth/login', json=credentials_json)

    # Old token post and response.
    old_refresh_token = login_response.get_json()['refresh_token']
    refresh_credentials = {'refresh_token':old_refresh_token}
    refresh_response = tester.post('/api/v1/auth/refresh', json=refresh_credentials)

    # Refresh with new token.
    with flask_app.app_context():
        user = User.query.filter_by(email='joe@koffie.com').first()
        new_refresh_token = refresh_response.get_json()['refresh_token']
        new_refresh_credentials = {'refresh_token':new_refresh_token}
        latest_refresh_response = tester.post('/api/v1/auth/refresh',json=new_refresh_credentials)
        token = latest_refresh_response.get_json()['token']
        decoded_payload = jwt.decode(token, os.environ.get('SECRET_KEY'),algorithms=['HS256'])
        assert latest_refresh_response.status_code == 200
        assert uuid.UUID(decoded_payload['user_id']) == user.id
