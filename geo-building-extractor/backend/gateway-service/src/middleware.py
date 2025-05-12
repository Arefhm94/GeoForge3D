from flask import request, jsonify
from functools import wraps

def require_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Authentication token is missing!'}), 401
        # Here you would typically verify the token
        return f(*args, **kwargs)
    return decorated_function

def limit_request_size(max_size):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if request.content_length > max_size:
                return jsonify({'message': 'Request size exceeds limit!'}), 413
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def log_request_info(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        print(f'Request Path: {request.path}')
        print(f'Request Method: {request.method}')
        return f(*args, **kwargs)
    return decorated_function