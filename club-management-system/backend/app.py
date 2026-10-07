import os
import sys

# Ensure backend root is in Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from config import Config
from routes import auth_bp, student_bp, coordinator_bp, admin_bp
from utils.db import get_db_mode, execute_script, is_mysql_available

def create_app():
    # Frontend directory path (sibling folder)
    frontend_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'frontend')
    
    app = Flask(__name__, static_folder=frontend_dir, static_url_path='')
    app.config.from_object(Config)

    # Enable CORS for decoupled frontend or cross-origin dev servers
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(coordinator_bp)
    app.register_blueprint(admin_bp)

    # Health check endpoint
    @app.route('/api/health', methods=['GET'])
    def health():
        mode = get_db_mode()
        return jsonify({
            'status': 'healthy',
            'service': 'Club Management System API',
            'database_mode': mode,
            'mysql_connected': is_mysql_available()
        }), 200

    # Serve Frontend HTML & Assets directly if accessed via Flask port 5000
    @app.route('/', methods=['GET'])
    def serve_index():
        return send_from_directory(frontend_dir, 'index.html')

    @app.route('/<path:path>', methods=['GET'])
    def serve_static(path):
        target = os.path.join(frontend_dir, path)
        if os.path.exists(target):
            return send_from_directory(frontend_dir, path)
        return send_from_directory(frontend_dir, 'index.html')

    @app.errorhandler(404)
    def handle_not_found(e):
        return jsonify({'success': False, 'message': 'Resource not found'}), 404

    @app.errorhandler(500)
    def handle_server_error(e):
        return jsonify({'success': False, 'message': 'Internal server error'}), 500

    return app

if __name__ == '__main__':
    # Auto-initialize SQLite database if running in standalone test mode without existing DB
    if get_db_mode() == 'sqlite' and not os.path.exists(Config.SQLITE_PATH):
        print("[INFO] Initializing local database from schema.sql & seed.sql...")
        db_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'database')
        schema_path = os.path.join(db_dir, 'schema.sql')
        seed_path = os.path.join(db_dir, 'seed.sql')
        if os.path.exists(schema_path):
            with open(schema_path, 'r', encoding='utf-8') as f:
                execute_script(f.read())
        if os.path.exists(seed_path):
            with open(seed_path, 'r', encoding='utf-8') as f:
                execute_script(f.read())
        print("[INFO] Standalone local database initialized successfully!")

    app = create_app()
    port = int(os.getenv('PORT', 5000))
    print(f"🚀 Club Management System backend listening on http://127.0.0.1:{port}")
    app.run(host='0.0.0.0', port=port, debug=True)
