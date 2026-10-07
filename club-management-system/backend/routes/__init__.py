from routes.auth_routes import auth_bp
from routes.student_routes import student_bp
from routes.coordinator_routes import coordinator_bp
from routes.admin_routes import admin_bp

__all__ = ['auth_bp', 'student_bp', 'coordinator_bp', 'admin_bp']
