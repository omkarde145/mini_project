import os
import pymysql
import pymysql.cursors
import sqlite3
import re
from config import Config

def get_mysql_connection():
    """Establish and return a PyMySQL connection with dictionary cursor."""
    return pymysql.connect(
        host=Config.DB_HOST,
        port=Config.DB_PORT,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        database=Config.DB_NAME,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=False
    )

def _get_sqlite_connection():
    """Establish and return an SQLite connection with dictionary row factory."""
    conn = sqlite3.connect(Config.SQLITE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def is_mysql_available():
    """Check if the configured MySQL server is reachable."""
    try:
        conn = pymysql.connect(
            host=Config.DB_HOST,
            port=Config.DB_PORT,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            connect_timeout=2
        )
        conn.close()
        return True
    except Exception:
        return False

def get_db_mode():
    """Determine whether to use MySQL or SQLite fallback."""
    if Config.DB_MODE == 'sqlite':
        return 'sqlite'
    if is_mysql_available():
        return 'mysql'
    # Fallback if MySQL is not running on localhost
    return 'sqlite'

def query_db(query, args=(), one=False):
    """
    Execute a SELECT query and return dictionary result(s).
    Supports standard MySQL parameter placeholder '%s'.
    """
    mode = get_db_mode()
    if mode == 'mysql':
        conn = get_mysql_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, args)
                result = cursor.fetchall()
                return (result[0] if result else None) if one else result
        finally:
            conn.close()
    else:
        # SQLite mode: convert %s to ?
        sqlite_query = query.replace('%s', '?')
        conn = _get_sqlite_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(sqlite_query, args)
            rows = cursor.fetchall()
            dict_rows = [dict(row) for row in rows]
            return (dict_rows[0] if dict_rows else None) if one else dict_rows
        finally:
            conn.close()

def execute_db(query, args=(), commit=True):
    """
    Execute an INSERT, UPDATE, or DELETE query.
    Returns (lastrowid, rowcount).
    """
    mode = get_db_mode()
    if mode == 'mysql':
        conn = get_mysql_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, args)
                last_id = cursor.lastrowid
                row_count = cursor.rowcount
            if commit:
                conn.commit()
            return last_id, row_count
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
    else:
        sqlite_query = query.replace('%s', '?')
        conn = _get_sqlite_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(sqlite_query, args)
            last_id = cursor.lastrowid
            row_count = cursor.rowcount
            if commit:
                conn.commit()
            return last_id, row_count
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

def execute_script(sql_content):
    """Execute raw SQL statements sequentially."""
    mode = get_db_mode()
    if mode == 'mysql':
        conn = pymysql.connect(
            host=Config.DB_HOST,
            port=Config.DB_PORT,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        try:
            with conn.cursor() as cursor:
                statements = [stmt.strip() for stmt in sql_content.split(';') if stmt.strip()]
                for stmt in statements:
                    cursor.execute(stmt)
            conn.commit()
        finally:
            conn.close()
    else:
        # Clean MySQL-specific syntax for SQLite
        clean_sql = re.sub(r'ENGINE\s*=\s*InnoDB', '', sql_content, flags=re.IGNORECASE)
        clean_sql = re.sub(r'DEFAULT\s+CHARSET\s*=\s*[a-zA-Z0-9]+', '', clean_sql, flags=re.IGNORECASE)
        clean_sql = re.sub(r'COLLATE\s*=\s*[a-zA-Z0-9_]+', '', clean_sql, flags=re.IGNORECASE)
        clean_sql = re.sub(r'CHARACTER\s+SET\s+[a-zA-Z0-9]+', '', clean_sql, flags=re.IGNORECASE)
        clean_sql = re.sub(r'COLLATE\s+[a-zA-Z0-9_]+', '', clean_sql, flags=re.IGNORECASE)
        clean_sql = re.sub(r'INT\s+AUTO_INCREMENT\s+PRIMARY\s+KEY', 'INTEGER PRIMARY KEY AUTOINCREMENT', clean_sql, flags=re.IGNORECASE)
        clean_sql = re.sub(r'ENUM\([^)]+\)', 'TEXT', clean_sql, flags=re.IGNORECASE)
        clean_sql = re.sub(r'SET\s+FOREIGN_KEY_CHECKS\s*=\s*[01];', '', clean_sql, flags=re.IGNORECASE)
        clean_sql = re.sub(r'CREATE\s+DATABASE[^;]+;', '', clean_sql, flags=re.IGNORECASE)
        clean_sql = re.sub(r'USE\s+[^;]+;', '', clean_sql, flags=re.IGNORECASE)

        conn = _get_sqlite_connection()
        try:
            conn.executescript(clean_sql)
            conn.commit()
        finally:
            conn.close()
