import os
from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'club-management-system-super-secret-key-2026')
    JWT_SECRET = os.getenv('JWT_SECRET', 'jwt-super-secret-key-campus-club-2026')
    JWT_ALGORITHM = 'HS256'
    JWT_EXPIRES_HOURS = int(os.getenv('JWT_EXPIRES_HOURS', '24'))

    # MySQL Database Configuration
    DB_HOST = os.getenv('DB_HOST', '127.0.0.1')
    DB_PORT = int(os.getenv('DB_PORT', '3306'))
    DB_USER = os.getenv('DB_USER', 'root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')
    DB_NAME = os.getenv('DB_NAME', 'club_management_db')
    
    # DB Backend Mode: 'mysql' (default) or 'sqlite' (for standalone zero-server testing)
    DB_MODE = os.getenv('DB_MODE', 'mysql').lower()
    SQLITE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'club_system.db')

    # CORS Configuration
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*')
