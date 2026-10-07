from utils.db import query_db, execute_db

class Club:
    @staticmethod
    def create(name, description, category, banner_url=None, coordinator_id=None, status='pending'):
        """Create a new club."""
        sql = """
            INSERT INTO clubs (name, description, category, banner_url, coordinator_id, status)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        club_id, _ = execute_db(sql, (name, description, category, banner_url, coordinator_id, status))
        return Club.find_by_id(club_id)

    @staticmethod
    def find_by_id(club_id):
        """Retrieve club with coordinator details and member count."""
        sql = """
            SELECT c.*, 
                   u.full_name AS coordinator_name, 
                   u.email AS coordinator_email,
                   (SELECT COUNT(*) FROM memberships m WHERE m.club_id = c.id AND m.status = 'approved') AS member_count,
                   (SELECT COUNT(*) FROM events e WHERE e.club_id = c.id) AS event_count
            FROM clubs c
            LEFT JOIN users u ON c.coordinator_id = u.id
            WHERE c.id = %s
        """
        return query_db(sql, (club_id,), one=True)

    @staticmethod
    def find_by_coordinator_id(coordinator_id):
        """Retrieve club assigned to a coordinator."""
        sql = """
            SELECT c.*, 
                   (SELECT COUNT(*) FROM memberships m WHERE m.club_id = c.id AND m.status = 'approved') AS member_count,
                   (SELECT COUNT(*) FROM memberships m WHERE m.club_id = c.id AND m.status = 'pending') AS pending_requests_count,
                   (SELECT COUNT(*) FROM events e WHERE e.club_id = c.id) AS event_count,
                   (SELECT COUNT(*) FROM announcements a WHERE a.club_id = c.id) AS announcement_count
            FROM clubs c
            WHERE c.coordinator_id = %s
        """
        return query_db(sql, (coordinator_id,), one=True)

    @staticmethod
    def get_all(status='approved', category=None, search=None):
        """Get clubs with optional status, category, and keyword filters."""
        sql = """
            SELECT c.*, 
                   u.full_name AS coordinator_name,
                   (SELECT COUNT(*) FROM memberships m WHERE m.club_id = c.id AND m.status = 'approved') AS member_count,
                   (SELECT COUNT(*) FROM events e WHERE e.club_id = c.id) AS event_count
            FROM clubs c
            LEFT JOIN users u ON c.coordinator_id = u.id
            WHERE 1=1
        """
        params = []
        if status:
            sql += " AND c.status = %s"
            params.append(status)
        if category and category.lower() != 'all':
            sql += " AND LOWER(c.category) = LOWER(%s)"
            params.append(category)
        if search:
            sql += " AND (c.name LIKE %s OR c.description LIKE %s OR c.category LIKE %s)"
            pattern = f"%{search}%"
            params.extend([pattern, pattern, pattern])

        sql += " ORDER BY c.name ASC"
        return query_db(sql, params)

    @staticmethod
    def update(club_id, name=None, description=None, category=None, banner_url=None, coordinator_id=None):
        """Update club details."""
        updates = []
        params = []
        if name is not None:
            updates.append("name = %s")
            params.append(name)
        if description is not None:
            updates.append("description = %s")
            params.append(description)
        if category is not None:
            updates.append("category = %s")
            params.append(category)
        if banner_url is not None:
            updates.append("banner_url = %s")
            params.append(banner_url)
        if coordinator_id is not None:
            updates.append("coordinator_id = %s")
            params.append(coordinator_id)

        if not updates:
            return True

        sql = f"UPDATE clubs SET {', '.join(updates)} WHERE id = %s"
        params.append(club_id)
        _, count = execute_db(sql, params)
        return count > 0

    @staticmethod
    def update_status(club_id, status):
        """Update club approval status ('pending', 'approved', 'rejected')."""
        sql = "UPDATE clubs SET status = %s WHERE id = %s"
        _, count = execute_db(sql, (status, club_id))
        return count > 0

    @staticmethod
    def get_categories():
        """Get distinct club categories."""
        sql = "SELECT DISTINCT category FROM clubs WHERE status = 'approved' ORDER BY category ASC"
        rows = query_db(sql)
        return [r['category'] for r in rows] if rows else []
