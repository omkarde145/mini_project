from werkzeug.security import generate_password_hash, check_password_hash
from utils.db import query_db, execute_db

class User:
    @staticmethod
    def create(full_name, email, password, role='student', department=None, student_id=None, phone=None):
        """Create a new user with securely hashed password."""
        password_hash = generate_password_hash(password)
        sql = """
            INSERT INTO users (full_name, email, password_hash, role, is_active, department, student_id, phone)
            VALUES (%s, %s, %s, %s, TRUE, %s, %s, %s)
        """
        user_id, _ = execute_db(sql, (full_name, email.strip().lower(), password_hash, role, department, student_id, phone))
        return User.find_by_id(user_id)

    @staticmethod
    def find_by_email(email):
        """Find user by email address."""
        sql = "SELECT * FROM users WHERE LOWER(email) = LOWER(%s)"
        return query_db(sql, (email.strip(),), one=True)

    @staticmethod
    def find_by_id(user_id):
        """Find user by numeric ID."""
        sql = "SELECT id, full_name, email, role, is_active, department, student_id, phone, created_at FROM users WHERE id = %s"
        return query_db(sql, (user_id,), one=True)

    @staticmethod
    def verify_password(plain_password, password_hash):
        """Verify plain password against stored hash."""
        return check_password_hash(password_hash, plain_password)

    @staticmethod
    def get_all(role=None, search=None):
        """Retrieve users with optional role and keyword filters."""
        sql = "SELECT id, full_name, email, role, is_active, department, student_id, phone, created_at FROM users WHERE 1=1"
        params = []
        if role:
            sql += " AND role = %s"
            params.append(role)
        if search:
            sql += " AND (full_name LIKE %s OR email LIKE %s OR student_id LIKE %s)"
            pattern = f"%{search}%"
            params.extend([pattern, pattern, pattern])
        sql += " ORDER BY id DESC"
        return query_db(sql, params)

    @staticmethod
    def update_status(user_id, is_active):
        """Activate or deactivate user account."""
        sql = "UPDATE users SET is_active = %s WHERE id = %s"
        _, count = execute_db(sql, (1 if is_active else 0, user_id))
        return count > 0

    @staticmethod
    def update_role(user_id, new_role):
        """Assign a new role to user ('student', 'coordinator', 'admin')."""
        sql = "UPDATE users SET role = %s WHERE id = %s"
        _, count = execute_db(sql, (new_role, user_id))
        return count > 0
