import jwt
from datetime import datetime, timedelta, timezone
from functools import wraps
from flask import request, jsonify
from config import Config
from utils.db import query_db

def generate_token(user):
    """Generate a JWT token for an authenticated user."""
    payload = {
        'user_id': user['id'],
        'email': user['email'],
        'role': user['role'],
        'full_name': user['full_name'],
        'exp': datetime.now(timezone.utc) + timedelta(hours=Config.JWT_EXPIRES_HOURS),
        'iat': datetime.now(timezone.utc)
    }
    return jwt.encode(payload, Config.JWT_SECRET, algorithm=Config.JWT_ALGORITHM)

def decode_token(token):
    """Decode and validate a JWT token."""
    try:
        payload = jwt.decode(token, Config.JWT_SECRET, algorithms=[Config.JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def login_required(f):
    """Decorator to require a valid authenticated user session/token."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization', None)
        token = None

        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
        elif request.headers.get('x-access-token'):
            token = request.headers.get('x-access-token')

        if not token:
            return jsonify({'success': False, 'message': 'Authentication token is missing'}), 401

        payload = decode_token(token)
        if not payload:
            return jsonify({'success': False, 'message': 'Token is invalid or has expired'}), 401

        # Verify user exists and is active in database
        user = query_db('SELECT id, full_name, email, role, is_active FROM users WHERE id = %s', (payload['user_id'],), one=True)
        if not user:
            return jsonify({'success': False, 'message': 'User no longer exists'}), 401

        if not user.get('is_active', True):
            return jsonify({'success': False, 'message': 'Account has been deactivated. Please contact administrator.'}), 403

        # Attach authenticated user to request context
        request.user = user
        return f(*args, **kwargs)
    return decorated_function

def role_required(*roles):
    """Decorator to enforce role-based access control."""
    def decorator(f):
        @wraps(f)
        @login_required
        def decorated_function(*args, **kwargs):
            user_role = request.user.get('role')
            if user_role not in roles:
                return jsonify({
                    'success': False, 
                    'message': f"Access forbidden. Required role: {', '.join(roles)}. Your role: {user_role}"
                }), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator
