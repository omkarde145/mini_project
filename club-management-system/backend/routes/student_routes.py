from flask import Blueprint, request, jsonify
from models.club import Club
from models.membership import Membership
from models.event import Event
from models.announcement import Announcement
from utils.decorators import login_required, role_required

student_bp = Blueprint('student', __name__, url_prefix='/api/student')

@student_bp.route('/categories', methods=['GET'])
def get_categories():
    """Retrieve distinct categories of campus clubs."""
    categories = Club.get_categories()
    return jsonify({'success': True, 'categories': categories}), 200

@student_bp.route('/clubs', methods=['GET'])
def browse_clubs():
    """Explore, search, and filter approved campus clubs."""
    category = request.args.get('category', None)
    search = request.args.get('search', None)
    
    clubs = Club.get_all(status='approved', category=category, search=search)
    return jsonify({
        'success': True,
        'count': len(clubs),
        'clubs': clubs
    }), 200

@student_bp.route('/clubs/<int:club_id>', methods=['GET'])
def get_club_details(club_id):
    """Retrieve full details of a club including events, announcements, and user membership status."""
    club = Club.find_by_id(club_id)
    if not club:
        return jsonify({'success': False, 'message': 'Club not found'}), 404

    # Fetch events & announcements
    upcoming_events = Event.get_upcoming_by_club(club_id)
    past_events = Event.get_past_by_club(club_id)
    announcements = Announcement.get_by_club(club_id)

    # Check membership status if user token is provided
    user_membership = None
    auth_header = request.headers.get('Authorization', None)
    if auth_header and auth_header.startswith('Bearer '):
        from utils.decorators import decode_token
        payload = decode_token(auth_header.split(' ')[1])
        if payload:
            user_membership = Membership.find_by_user_and_club(payload['user_id'], club_id)

    return jsonify({
        'success': True,
        'club': club,
        'upcoming_events': upcoming_events,
        'past_events': past_events,
        'announcements': announcements,
        'membership': user_membership
    }), 200

@student_bp.route('/clubs/<int:club_id>/join', methods=['POST'])
@login_required
@role_required('student')
def request_join_club(club_id):
    """Submit a membership join request with status tracking."""
    user_id = request.user['id']
    club = Club.find_by_id(club_id)

    if not club:
        return jsonify({'success': False, 'message': 'Club not found'}), 404

    if club['status'] != 'approved':
        return jsonify({'success': False, 'message': 'Cannot join unapproved club'}), 400

    existing = Membership.find_by_user_and_club(user_id, club_id)
    if existing:
        if existing['status'] == 'approved':
            return jsonify({'success': False, 'message': 'You are already an approved member of this club'}), 400
        elif existing['status'] == 'pending':
            return jsonify({'success': False, 'message': 'Your membership request is currently pending review'}), 400

    membership = Membership.create_request(user_id, club_id)
    return jsonify({
        'success': True,
        'message': 'Membership request submitted successfully',
        'membership': membership
    }), 201

@student_bp.route('/memberships', methods=['GET'])
@login_required
@role_required('student')
def get_my_memberships():
    """Retrieve list of clubs student has requested or joined with status tracking."""
    user_id = request.user['id']
    memberships = Membership.get_user_memberships(user_id)
    return jsonify({
        'success': True,
        'count': len(memberships),
        'memberships': memberships
    }), 200

@student_bp.route('/memberships/<int:club_id>', methods=['DELETE'])
@login_required
@role_required('student')
def leave_or_cancel_membership(club_id):
    """Cancel pending request or leave an approved club."""
    user_id = request.user['id']
    existing = Membership.find_by_user_and_club(user_id, club_id)
    if not existing:
        return jsonify({'success': False, 'message': 'No membership record found'}), 404

    Membership.remove_member(club_id, user_id)
    return jsonify({'success': True, 'message': 'Membership removed successfully'}), 200

@student_bp.route('/feed', methods=['GET'])
@login_required
@role_required('student')
def get_student_feed():
    """Aggregated announcements and events for clubs the student belongs to."""
    user_id = request.user['id']
    announcements = Announcement.get_announcements_for_student(user_id)
    events = Event.get_events_for_student(user_id)
    return jsonify({
        'success': True,
        'announcements': announcements,
        'upcoming_events': events
    }), 200
