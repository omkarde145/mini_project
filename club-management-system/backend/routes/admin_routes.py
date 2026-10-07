from flask import Blueprint, request, jsonify
from models.user import User
from models.club import Club
from utils.db import query_db
from utils.decorators import login_required, role_required

admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')

@admin_bp.route('/overview', methods=['GET'])
@login_required
@role_required('admin')
def get_overview():
    """Platform metrics: total clubs, students, coordinators, events, pending approvals."""
    total_clubs = query_db("SELECT COUNT(*) AS count FROM clubs", one=True)['count']
    approved_clubs = query_db("SELECT COUNT(*) AS count FROM clubs WHERE status = 'approved'", one=True)['count']
    pending_clubs = query_db("SELECT COUNT(*) AS count FROM clubs WHERE status = 'pending'", one=True)['count']
    total_students = query_db("SELECT COUNT(*) AS count FROM users WHERE role = 'student'", one=True)['count']
    total_coordinators = query_db("SELECT COUNT(*) AS count FROM users WHERE role = 'coordinator'", one=True)['count']
    total_events = query_db("SELECT COUNT(*) AS count FROM events", one=True)['count']
    pending_memberships = query_db("SELECT COUNT(*) AS count FROM memberships WHERE status = 'pending'", one=True)['count']

    return jsonify({
        'success': True,
        'metrics': {
            'total_clubs': total_clubs,
            'approved_clubs': approved_clubs,
            'pending_clubs': pending_clubs,
            'total_students': total_students,
            'total_coordinators': total_coordinators,
            'total_events': total_events,
            'pending_memberships': pending_memberships
        }
    }), 200

@admin_bp.route('/clubs', methods=['GET'])
@login_required
@role_required('admin')
def list_clubs():
    """List all clubs across statuses (pending, approved, rejected)."""
    status = request.args.get('status', None)
    search = request.args.get('search', None)
    category = request.args.get('category', None)

    clubs = Club.get_all(status=status, category=category, search=search)
    return jsonify({
        'success': True,
        'count': len(clubs),
        'clubs': clubs
    }), 200

@admin_bp.route('/clubs/<int:club_id>/status', methods=['POST'])
@login_required
@role_required('admin')
def review_club(club_id):
    """Approve or reject a club registration."""
    club = Club.find_by_id(club_id)
    if not club:
        return jsonify({'success': False, 'message': 'Club not found'}), 404

    data = request.get_json() or {}
    new_status = data.get('status', '').strip().lower()

    if new_status not in ['approved', 'rejected', 'pending']:
        return jsonify({'success': False, 'message': 'Status must be approved, rejected, or pending'}), 400

    Club.update_status(club_id, new_status)
    return jsonify({
        'success': True,
        'message': f'Club status changed to {new_status}'
    }), 200

@admin_bp.route('/clubs', methods=['POST'])
@login_required
@role_required('admin')
def create_club():
    """Create a new club directly from admin console."""
    data = request.get_json() or {}
    name = data.get('name', '').strip()
    description = data.get('description', '').strip()
    category = data.get('category', '').strip()
    banner_url = data.get('banner_url', '').strip() or None
    coordinator_id = data.get('coordinator_id', None)
    status = data.get('status', 'approved').strip().lower()

    if not name or not description or not category:
        return jsonify({'success': False, 'message': 'Name, description, and category are required'}), 400

    new_club = Club.create(
        name=name,
        description=description,
        category=category,
        banner_url=banner_url,
        coordinator_id=coordinator_id,
        status=status
    )

    return jsonify({
        'success': True,
        'message': 'Club created successfully',
        'club': new_club
    }), 201

@admin_bp.route('/users', methods=['GET'])
@login_required
@role_required('admin')
def list_users():
    """List system users with optional role and search filters."""
    role = request.args.get('role', None)
    search = request.args.get('search', None)

    users = User.get_all(role=role, search=search)
    return jsonify({
        'success': True,
        'count': len(users),
        'users': users
    }), 200

@admin_bp.route('/users/<int:user_id>/toggle-status', methods=['POST'])
@login_required
@role_required('admin')
def toggle_user_status(user_id):
    """Activate or deactivate user account."""
    user = User.find_by_id(user_id)
    if not user:
        return jsonify({'success': False, 'message': 'User not found'}), 404

    # Prevent deactivating oneself
    if user['id'] == request.user['id']:
        return jsonify({'success': False, 'message': 'Cannot deactivate your own admin account'}), 400

    current_status = bool(user.get('is_active', True))
    new_status = not current_status
    User.update_status(user_id, new_status)

    return jsonify({
        'success': True,
        'message': f"User account has been {'activated' if new_status else 'deactivated'}",
        'is_active': new_status
    }), 200

@admin_bp.route('/users/<int:user_id>/role', methods=['POST'])
@login_required
@role_required('admin')
def change_user_role(user_id):
    """Assign a new role to user (student, coordinator, admin)."""
    user = User.find_by_id(user_id)
    if not user:
        return jsonify({'success': False, 'message': 'User not found'}), 404

    data = request.get_json() or {}
    new_role = data.get('role', '').strip().lower()

    if new_role not in ['student', 'coordinator', 'admin']:
        return jsonify({'success': False, 'message': 'Invalid role'}), 400

    User.update_role(user_id, new_role)
    return jsonify({
        'success': True,
        'message': f'Role updated to {new_role}'
    }), 200

@admin_bp.route('/coordinators', methods=['GET'])
@login_required
@role_required('admin')
def list_coordinators():
    """List all coordinators available for club assignment."""
    coordinators = User.get_all(role='coordinator')
    return jsonify({'success': True, 'coordinators': coordinators}), 200
