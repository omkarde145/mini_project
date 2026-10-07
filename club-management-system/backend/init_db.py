import os
import sys

# Ensure backend root is in Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import Config
from utils.db import execute_script, is_mysql_available, get_db_mode
import pymysql

def init_database(force_mode=None):
    """
    Run schema.sql and seed.sql against MySQL or SQLite.
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    schema_path = os.path.join(base_dir, 'database', 'schema.sql')
    seed_path = os.path.join(base_dir, 'database', 'seed.sql')

    mode = force_mode or get_db_mode()
    print(f"[*] Initializing database in mode: {mode.upper()}")

    with open(schema_path, 'r', encoding='utf-8') as f:
        schema_sql = f.read()

    with open(seed_path, 'r', encoding='utf-8') as f:
        seed_sql = f.read()

    if mode == 'mysql':
        print(f"[*] Connecting to MySQL at {Config.DB_HOST}:{Config.DB_PORT} as '{Config.DB_USER}'...")
        # Create database first if not exists
        conn = pymysql.connect(
            host=Config.DB_HOST,
            port=Config.DB_PORT,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            charset='utf8mb4'
        )
        try:
            with conn.cursor() as cursor:
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{Config.DB_NAME}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
            conn.commit()
        finally:
            conn.close()

        print("[*] Executing schema.sql...")
        execute_script(schema_sql)
        print("[*] Executing seed.sql...")
        execute_script(seed_sql)
        print("[+] MySQL database setup & seed completed successfully!")

    else:
        print(f"[*] Setting up SQLite database at: {Config.SQLITE_PATH}")
        if os.path.exists(Config.SQLITE_PATH):
            os.remove(Config.SQLITE_PATH)
        print("[*] Executing schema.sql...")
        execute_script(schema_sql)
        print("[*] Executing seed.sql...")
        execute_script(seed_sql)
        print("[+] SQLite database setup & seed completed successfully!")

if __name__ == '__main__':
    mode_arg = sys.argv[1].replace('--', '') if len(sys.argv) > 1 else None
    init_database(force_mode=mode_arg)
