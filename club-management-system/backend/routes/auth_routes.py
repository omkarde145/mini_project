from flask import Blueprint, request, jsonify
from models.user import User
from models.club import Club
from utils.decorators import login_required, generate_token

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new student or coordinator."""
    data = request.get_json() or {}
    full_name = data.get('full_name', '').strip()
    email = data.get('email', '').strip()
    password = data.get('password', '').strip()
    role = data.get('role', 'student').strip().lower()
    department = data.get('department', '').strip() or None
    student_id = data.get('student_id', '').strip() or None
    phone = data.get('phone', '').strip() or None
    club_name = data.get('club_name', '').strip() or None
    club_category = data.get('club_category', 'General').strip() or 'General'
    club_description = data.get('club_description', '').strip() or 'A student-led community club.'

    # Validation
    if not full_name or not email or not password:
        return jsonify({'success': False, 'message': 'Full name, email, and password are required'}), 400

    if role not in ['student', 'coordinator']:
        return jsonify({'success': False, 'message': 'Role must be student or coordinator'}), 400

    if len(password) < 6:
        return jsonify({'success': False, 'message': 'Password must be at least 6 characters long'}), 400

    existing_user = User.find_by_email(email)
    if existing_user:
        return jsonify({'success': False, 'message': 'An account with this email already exists'}), 409

    try:
        user = User.create(
            full_name=full_name,
            email=email,
            password=password,
            role=role,
            department=department,
            student_id=student_id,
            phone=phone
        )

        club_info = None
        # If registering as coordinator with proposed club name, register a pending club
        if role == 'coordinator' and club_name:
            club_info = Club.create(
                name=club_name,
                description=club_description,
                category=club_category,
                coordinator_id=user['id'],
                status='pending'
            )

        token = generate_token(user)

        return jsonify({
            'success': True,
            'message': 'Registration successful',
            'token': token,
            'user': {
                'id': user['id'],
                'full_name': user['full_name'],
                'email': user['email'],
                'role': user['role'],
                'department': user.get('department'),
                'student_id': user.get('student_id'),
                'phone': user.get('phone')
            },
            'club': club_info
        }), 201

    except Exception as e:
        return jsonify({'success': False, 'message': f'Registration failed: {str(e)}'}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """Authenticate a user and return a JWT access token."""
    data = request.get_json() or {}
    email = data.get('email', '').strip()
    password = data.get('password', '').strip()

    if not email or not password:
        return jsonify({'success': False, 'message': 'Email and password are required'}), 400

    user = User.find_by_email(email)
    if not user or not User.verify_password(password, user['password_hash']):
        return jsonify({'success': False, 'message': 'Invalid email or password'}), 401

    if not user.get('is_active', True):
        return jsonify({'success': False, 'message': 'This account has been deactivated. Please contact an admin.'}), 403

    token = generate_token(user)

    # Check for coordinator club affiliation
    club_info = None
    if user['role'] == 'coordinator':
        club_info = Club.find_by_coordinator_id(user['id'])

    return jsonify({
        'success': True,
        'message': 'Login successful',
        'token': token,
        'user': {
            'id': user['id'],
            'full_name': user['full_name'],
            'email': user['email'],
            'role': user['role'],
            'department': user.get('department'),
            'student_id': user.get('student_id'),
            'phone': user.get('phone')
        },
        'club': club_info
    }), 200

@auth_bp.route('/me', methods=['GET'])
@login_required
def me():
    """Return profile of the currently authenticated user."""
    user = request.user
    full_user = User.find_by_id(user['id'])
    club_info = None
    if user['role'] == 'coordinator':
        club_info = Club.find_by_coordinator_id(user['id'])

    return jsonify({
        'success': True,
        'user': {
            'id': full_user['id'],
            'full_name': full_user['full_name'],
            'email': full_user['email'],
            'role': full_user['role'],
            'department': full_user.get('department'),
            'student_id': full_user.get('student_id'),
            'phone': full_user.get('phone'),
            'created_at': str(full_user.get('created_at', ''))
        },
        'club': club_info
    }), 200

@auth_bp.route('/logout', methods=['POST'])
def logout():
    """Client-side token invalidation acknowledgment."""
    return jsonify({'success': True, 'message': 'Logged out successfully'}), 200
