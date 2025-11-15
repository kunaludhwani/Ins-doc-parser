"""
SQLite database setup and connection
"""
import sqlite3
from app.config import settings


def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect(settings.DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize database with required tables"""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create logs table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS request_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            file_type TEXT NOT NULL,
            page_count INTEGER,
            text_length INTEGER,
            explanation TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()
    print("Database initialized successfully")


def close_db(conn):
    """Close database connection"""
    if conn:
        conn.close()
