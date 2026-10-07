from utils.db import query_db, execute_db

class Announcement:
    @staticmethod
    def create(club_id, title, content):
        """Post a new announcement for a club."""
        sql = """
            INSERT INTO announcements (club_id, title, content)
            VALUES (%s, %s, %s)
        """
        ann_id, _ = execute_db(sql, (club_id, title, content))
        return Announcement.find_by_id(ann_id)

    @staticmethod
    def find_by_id(announcement_id):
        """Retrieve single announcement with club name."""
        sql = """
            SELECT a.*, c.name AS club_name, c.category AS club_category
            FROM announcements a
            JOIN clubs c ON a.club_id = c.id
            WHERE a.id = %s
        """
        return query_db(sql, (announcement_id,), one=True)

    @staticmethod
    def get_by_club(club_id):
        """Retrieve announcements for a specific club."""
        sql = """
            SELECT * FROM announcements 
            WHERE club_id = %s 
            ORDER BY posted_at DESC
        """
        return query_db(sql, (club_id,))

    @staticmethod
    def get_announcements_for_student(user_id):
        """Retrieve latest announcements from clubs the student has joined."""
        sql = """
            SELECT a.*, c.name AS club_name, c.category AS club_category, c.banner_url
            FROM announcements a
            JOIN clubs c ON a.club_id = c.id
            JOIN memberships m ON m.club_id = c.id
            WHERE m.user_id = %s AND m.status = 'approved'
            ORDER BY a.posted_at DESC
            LIMIT 20
        """
        return query_db(sql, (user_id,))

    @staticmethod
    def update(announcement_id, title=None, content=None):
        """Update announcement title and content."""
        updates = []
        params = []
        if title is not None:
            updates.append("title = %s")
            params.append(title)
        if content is not None:
            updates.append("content = %s")
            params.append(content)

        if not updates:
            return True

        sql = f"UPDATE announcements SET {', '.join(updates)} WHERE id = %s"
        params.append(announcement_id)
        _, count = execute_db(sql, params)
        return count > 0

    @staticmethod
    def delete(announcement_id):
        """Delete an announcement."""
        sql = "DELETE FROM announcements WHERE id = %s"
        _, count = execute_db(sql, (announcement_id,))
        return count > 0
