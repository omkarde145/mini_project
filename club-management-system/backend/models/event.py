from utils.db import query_db, execute_db

class Event:
    @staticmethod
    def create(club_id, title, description, event_date, location):
        """Create a new event for a club."""
        sql = """
            INSERT INTO events (club_id, title, description, event_date, location)
            VALUES (%s, %s, %s, %s, %s)
        """
        event_id, _ = execute_db(sql, (club_id, title, description, event_date, location))
        return Event.find_by_id(event_id)

    @staticmethod
    def find_by_id(event_id):
        """Retrieve single event by ID with club details."""
        sql = """
            SELECT e.*, c.name AS club_name, c.category AS club_category
            FROM events e
            JOIN clubs c ON e.club_id = c.id
            WHERE e.id = %s
        """
        return query_db(sql, (event_id,), one=True)

    @staticmethod
    def get_by_club(club_id):
        """Retrieve all events of a specific club."""
        sql = """
            SELECT * FROM events 
            WHERE club_id = %s 
            ORDER BY event_date DESC
        """
        return query_db(sql, (club_id,))

    @staticmethod
    def get_upcoming_by_club(club_id):
        """Retrieve upcoming events for a club."""
        sql = """
            SELECT * FROM events 
            WHERE club_id = %s AND event_date >= CURRENT_TIMESTAMP
            ORDER BY event_date ASC
        """
        return query_db(sql, (club_id,))

    @staticmethod
    def get_past_by_club(club_id):
        """Retrieve past events for a club."""
        sql = """
            SELECT * FROM events 
            WHERE club_id = %s AND event_date < CURRENT_TIMESTAMP
            ORDER BY event_date DESC
        """
        return query_db(sql, (club_id,))

    @staticmethod
    def get_all_upcoming(limit=10):
        """Retrieve upcoming events across all approved clubs."""
        sql = """
            SELECT e.*, c.name AS club_name, c.category AS club_category, c.banner_url
            FROM events e
            JOIN clubs c ON e.club_id = c.id
            WHERE c.status = 'approved' AND e.event_date >= CURRENT_TIMESTAMP
            ORDER BY e.event_date ASC
            LIMIT %s
        """
        return query_db(sql, (limit,))

    @staticmethod
    def get_events_for_student(user_id):
        """Retrieve upcoming events for clubs the student has joined."""
        sql = """
            SELECT e.*, c.name AS club_name, c.category AS club_category
            FROM events e
            JOIN clubs c ON e.club_id = c.id
            JOIN memberships m ON m.club_id = c.id
            WHERE m.user_id = %s AND m.status = 'approved' AND e.event_date >= CURRENT_TIMESTAMP
            ORDER BY e.event_date ASC
        """
        return query_db(sql, (user_id,))

    @staticmethod
    def update(event_id, title=None, description=None, event_date=None, location=None):
        """Update event details."""
        updates = []
        params = []
        if title is not None:
            updates.append("title = %s")
            params.append(title)
        if description is not None:
            updates.append("description = %s")
            params.append(description)
        if event_date is not None:
            updates.append("event_date = %s")
            params.append(event_date)
        if location is not None:
            updates.append("location = %s")
            params.append(location)

        if not updates:
            return True

        sql = f"UPDATE events SET {', '.join(updates)} WHERE id = %s"
        params.append(event_id)
        _, count = execute_db(sql, params)
        return count > 0

    @staticmethod
    def delete(event_id):
        """Delete an event."""
        sql = "DELETE FROM events WHERE id = %s"
        _, count = execute_db(sql, (event_id,))
        return count > 0
