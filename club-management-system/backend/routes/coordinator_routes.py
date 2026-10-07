from flask import Blueprint, request, jsonify
from models.club import Club
from models.membership import Membership
from models.event import Event
from models.announcement import Announcement
from utils.decorators import login_required, role_required

coordinator_bp = Blueprint('coordinator', __name__, url_prefix='/api/coordinator')

def _get_coordinator_club(user_id):
    """Helper to fetch club assigned to coordinator."""
    return Club.find_by_coordinator_id(user_id)

@coordinator_bp.route('/club', methods=['GET'])
@login_required
@role_required('coordinator')
def get_club():
    """Retrieve details and statistics for coordinator's club."""
    user_id = request.user['id']
    club = _get_coordinator_club(user_id)
    if not club:
        return jsonify({'success': False, 'message': 'No club is currently assigned to your account'}), 404

    return jsonify({'success': True, 'club': club}), 200

@coordinator_bp.route('/club', methods=['PUT'])
@login_required
@role_required('coordinator')
def update_club():
    """Update club details (name, description, category, banner_url)."""
    user_id = request.user['id']
    club = _get_coordinator_club(user_id)
    if not club:
        return jsonify({'success': False, 'message': 'No assigned club found to update'}), 404

    data = request.get_json() or {}
    name = data.get('name')
    description = data.get('description')
    category = data.get('category')
    banner_url = data.get('banner_url')

    Club.update(
        club['id'],
        name=name.strip() if name else None,
        description=description.strip() if description else None,
        category=category.strip() if category else None,
        banner_url=banner_url.strip() if banner_url else None
    )

    updated_club = Club.find_by_id(club['id'])
    return jsonify({
        'success': True,
        'message': 'Club profile updated successfully',
        'club': updated_club
    }), 200

@coordinator_bp.route('/requests', methods=['GET'])
@login_required
@role_required('coordinator')
def get_pending_requests():
    """Review incoming student membership requests."""
    user_id = request.user['id']
    club = _get_coordinator_club(user_id)
    if not club:
        return jsonify({'success': False, 'message': 'No assigned club found'}), 404

    requests_list = Membership.get_club_pending_requests(club['id'])
    return jsonify({
        'success': True,
        'count': len(requests_list),
        'requests': requests_list
    }), 200

@coordinator_bp.route('/requests/<int:membership_id>/action', methods=['POST'])
@login_required
@role_required('coordinator')
def action_membership_request(membership_id):
    """Approve or reject incoming student membership request."""
    user_id = request.user['id']
    club = _get_coordinator_club(user_id)
    if not club:
        return jsonify({'success': False, 'message': 'No assigned club found'}), 404

    membership = Membership.find_by_id(membership_id)
    if not membership or membership['club_id'] != club['id']:
        return jsonify({'success': False, 'message': 'Membership request not found for your club'}), 404

    data = request.get_json() or {}
    action = data.get('action', '').strip().lower()

    if action not in ['approved', 'rejected']:
        return jsonify({'success': False, 'message': 'Action must be approved or rejected'}), 400

    Membership.update_status(membership_id, action)
    return jsonify({
        'success': True,
        'message': f'Membership request has been {action}'
    }), 200

@coordinator_bp.route('/members', methods=['GET'])
@login_required
@role_required('coordinator')
def get_member_roster():
    """Retrieve active member roster for the coordinator's club."""
    user_id = request.user['id']
    club = _get_coordinator_club(user_id)
    if not club:
        return jsonify({'success': False, 'message': 'No assigned club found'}), 404

    members = Membership.get_club_members(club['id'])
    return jsonify({
        'success': True,
        'count': len(members),
        'members': members
    }), 200

@coordinator_bp.route('/members/<int:student_id>', methods=['DELETE'])
@login_required
@role_required('coordinator')
def remove_club_member(student_id):
    """Remove a member from the active club roster."""
    user_id = request.user['id']
    club = _get_coordinator_club(user_id)
    if not club:
        return jsonify({'success': False, 'message': 'No assigned club found'}), 404

    removed = Membership.remove_member(club['id'], student_id)
    if not removed:
        return jsonify({'success': False, 'message': 'Student not found in club roster'}), 404

    return jsonify({'success': True, 'message': 'Member removed from club successfully'}), 200

# ----------------- EVENTS MANAGEMENT -----------------

@coordinator_bp.route('/events', methods=['GET'])
@login_required
@role_required('coordinator')
def list_events():
    """List all events for the coordinator's club."""
    user_id = request.user['id']
    club = _get_coordinator_club(user_id)
    if not club:
        return jsonify({'success': False, 'message': 'No assigned club found'}), 404

    events = Event.get_by_club(club['id'])
    return jsonify({'success': True, 'events': events}), 200

@coordinator_bp.route('/events', methods=['POST'])
@login_required
@role_required('coordinator')
def create_event():
    """Create a new event for the club."""
    user_id = request.user['id']
    club = _get_coordinator_club(user_id)
    if not club:
        return jsonify({'success': False, 'message': 'No assigned club found'}), 404

    data = request.get_json() or {}
    title = data.get('title', '').strip()
    description = data.get('description', '').strip()
    event_date = data.get('event_date', '').strip()
    location = data.get('location', '').strip()

    if not title or not description or not event_date or not location:
        return jsonify({'success': False, 'message': 'Title, description, event date, and location are required'}), 400

    new_event = Event.create(club['id'], title, description, event_date, location)
    return jsonify({
        'success': True,
        'message': 'Event created successfully',
        'event': new_event
    }), 201

@coordinator_bp.route('/events/<int:event_id>', methods=['PUT'])
@login_required
@role_required('coordinator')
def update_event(event_id):
    """Edit an existing club event."""
    user_id = request.user['id']
    club = _get_coordinator_club(user_id)
    if not club:
        return jsonify({'success': False, 'message': 'No assigned club found'}), 404

    event = Event.find_by_id(event_id)
    if not event or event['club_id'] != club['id']:
        return jsonify({'success': False, 'message': 'Event not found in your club'}), 404

    data = request.get_json() or {}
    Event.update(
        event_id,
        title=data.get('title'),
        description=data.get('description'),
        event_date=data.get('event_date'),
        location=data.get('location')
    )
    updated = Event.find_by_id(event_id)
    return jsonify({'success': True, 'message': 'Event updated successfully', 'event': updated}), 200

@coordinator_bp.route('/events/<int:event_id>', methods=['DELETE'])
@login_required
@role_required('coordinator')
def delete_event(event_id):
    """Delete a club event."""
    user_id = request.user['id']
    club = _get_coordinator_club(user_id)
    if not club:
        return jsonify({'success': False, 'message': 'No assigned club found'}), 404

    event = Event.find_by_id(event_id)
    if not event or event['club_id'] != club['id']:
        return jsonify({'success': False, 'message': 'Event not found in your club'}), 404

    Event.delete(event_id)
    return jsonify({'success': True, 'message': 'Event deleted successfully'}), 200

# ----------------- ANNOUNCEMENTS MANAGEMENT -----------------

@coordinator_bp.route('/announcements', methods=['GET'])
@login_required
@role_required('coordinator')
def list_announcements():
    """List all announcements for the coordinator's club."""
    user_id = request.user['id']
    club = _get_coordinator_club(user_id)
    if not club:
        return jsonify({'success': False, 'message': 'No assigned club found'}), 404

    announcements = Announcement.get_by_club(club['id'])
    return jsonify({'success': True, 'announcements': announcements}), 200

@coordinator_bp.route('/announcements', methods=['POST'])
@login_required
@role_required('coordinator')
def create_announcement():
    """Post a new club announcement."""
    user_id = request.user['id']
    club = _get_coordinator_club(user_id)
    if not club:
        return jsonify({'success': False, 'message': 'No assigned club found'}), 404

    data = request.get_json() or {}
    title = data.get('title', '').strip()
    content = data.get('content', '').strip()

    if not title or not content:
        return jsonify({'success': False, 'message': 'Title and content are required'}), 400

    new_ann = Announcement.create(club['id'], title, content)
    return jsonify({
        'success': True,
        'message': 'Announcement posted successfully',
        'announcement': new_ann
    }), 201

@coordinator_bp.route('/announcements/<int:ann_id>', methods=['PUT'])
@login_required
@role_required('coordinator')
def update_announcement(ann_id):
    """Edit a club announcement."""
    user_id = request.user['id']
    club = _get_coordinator_club(user_id)
    if not club:
        return jsonify({'success': False, 'message': 'No assigned club found'}), 404

    ann = Announcement.find_by_id(ann_id)
    if not ann or ann['club_id'] != club['id']:
        return jsonify({'success': False, 'message': 'Announcement not found in your club'}), 404

    data = request.get_json() or {}
    Announcement.update(ann_id, title=data.get('title'), content=data.get('content'))
    updated = Announcement.find_by_id(ann_id)
    return jsonify({'success': True, 'message': 'Announcement updated successfully', 'announcement': updated}), 200

@coordinator_bp.route('/announcements/<int:ann_id>', methods=['DELETE'])
@login_required
@role_required('coordinator')
def delete_announcement(ann_id):
    """Delete a club announcement."""
    user_id = request.user['id']
    club = _get_coordinator_club(user_id)
    if not club:
        return jsonify({'success': False, 'message': 'No assigned club found'}), 404

    ann = Announcement.find_by_id(ann_id)
    if not ann or ann['club_id'] != club['id']:
        return jsonify({'success': False, 'message': 'Announcement not found in your club'}), 404

    Announcement.delete(ann_id)
    return jsonify({'success': True, 'message': 'Announcement deleted successfully'}), 200
