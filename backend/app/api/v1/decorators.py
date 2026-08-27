from flask import request
from functools import wraps
from flask import jsonify
import os
import jwt

def jwt_required(func):
    @wraps(func)
    def verify_token(*args, **kwargs):
        authorization_request = request.headers.get('Authorization')
        if authorization_request:
            header_prefix, separator, token = authorization_request.partition(' ')
            if header_prefix == 'Bearer' and token:
                try:
                    decoded_payload = jwt.decode(token, os.environ.get('SECRET_KEY'), algorithms=['HS256'])
                    user_id = decoded_payload['user_id']
                    result = func(user_id, *args, **kwargs)
                    return result
                except jwt.ExpiredSignatureError:
                    return jsonify({'error': 'Expired or Invalid Token'}), 401
                except jwt.InvalidTokenError:
                    return jsonify({'error': 'Expired or Invalid Token'}), 401
            else:
                return jsonify({'error': 'Missing token'}), 401
        else:
            return jsonify({'error': 'Missing header'}), 401

    return verify_token
