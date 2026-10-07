from datetime import datetime
from utils.db import query_db, execute_db

class Membership:
    @staticmethod
    def create_request(user_id, club_id):
        """Submit a membership join request for a student."""
        # Check if membership already exists
        existing = Membership.find_by_user_and_club(user_id, club_id)
        if existing:
            if existing['status'] == 'rejected':
                # Allow re-applying if previously rejected
                sql = "UPDATE memberships SET status = 'pending', applied_at = CURRENT_TIMESTAMP, reviewed_at = NULL WHERE id = %s"
                execute_db(sql, (existing['id'],))
                return Membership.find_by_id(existing['id'])
            return existing

        sql = """
            INSERT INTO memberships (user_id, club_id, status)
            VALUES (%s, %s, 'pending')
        """
        mem_id, _ = execute_db(sql, (user_id, club_id))
        return Membership.find_by_id(mem_id)

    @staticmethod
    def find_by_id(membership_id):
        """Retrieve single membership by ID."""
        sql = """
            SELECT m.*, c.name AS club_name, c.category AS club_category, c.banner_url,
                   u.full_name AS student_name, u.email AS student_email, u.department, u.student_id
            FROM memberships m
            JOIN clubs c ON m.club_id = c.id
            JOIN users u ON m.user_id = u.id
            WHERE m.id = %s
        """
        return query_db(sql, (membership_id,), one=True)

    @staticmethod
    def find_by_user_and_club(user_id, club_id):
        """Retrieve membership for specific user and club."""
        sql = "SELECT * FROM memberships WHERE user_id = %s AND club_id = %s"
        return query_db(sql, (user_id, club_id), one=True)

    @staticmethod
    def get_user_memberships(user_id):
        """List all memberships of a student with club information."""
        sql = """
            SELECT m.id, m.club_id, m.status, m.applied_at, m.reviewed_at,
                   c.name AS club_name, c.category AS club_category, c.banner_url, c.description AS club_description,
                   u.full_name AS coordinator_name, u.email AS coordinator_email
            FROM memberships m
            JOIN clubs c ON m.club_id = c.id
            LEFT JOIN users u ON c.coordinator_id = u.id
            WHERE m.user_id = %s
            ORDER BY m.applied_at DESC
        """
        return query_db(sql, (user_id,))

    @staticmethod
    def get_club_members(club_id):
        """Retrieve all approved members of a club (active roster)."""
        sql = """
            SELECT m.id AS membership_id, m.applied_at, m.reviewed_at,
                   u.id AS user_id, u.full_name, u.email, u.department, u.student_id, u.phone
            FROM memberships m
            JOIN users u ON m.user_id = u.id
            WHERE m.club_id = %s AND m.status = 'approved'
            ORDER BY u.full_name ASC
        """
        return query_db(sql, (club_id,))

    @staticmethod
    def get_club_pending_requests(club_id):
        """Retrieve all pending membership join requests for coordinator review."""
        sql = """
            SELECT m.id AS membership_id, m.applied_at,
                   u.id AS user_id, u.full_name, u.email, u.department, u.student_id, u.phone
            FROM memberships m
            JOIN users u ON m.user_id = u.id
            WHERE m.club_id = %s AND m.status = 'pending'
            ORDER BY m.applied_at ASC
        """
        return query_db(sql, (club_id,))

    @staticmethod
    def update_status(membership_id, status):
        """Approve or reject a membership request."""
        sql = "UPDATE memberships SET status = %s, reviewed_at = CURRENT_TIMESTAMP WHERE id = %s"
        _, count = execute_db(sql, (status, membership_id))
        return count > 0

    @staticmethod
    def remove_member(club_id, user_id):
        """Remove an approved member from club roster."""
        sql = "DELETE FROM memberships WHERE club_id = %s AND user_id = %s"
        _, count = execute_db(sql, (club_id, user_id))
        return count > 0
