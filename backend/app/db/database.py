"""
SQLite database setup and connection - Optimized for performance
"""
import sqlite3
from app.config import settings


def get_db_connection():
    """
    Get optimized database connection with performance tuning

    Returns:
        sqlite3.Connection: Database connection with optimizations
    """
    conn = sqlite3.connect(
        settings.DATABASE_PATH,
        check_same_thread=False,  # Allow connection sharing (FastAPI async)
        timeout=10.0  # 10 second timeout for busy database
    )
    conn.row_factory = sqlite3.Row

    # Enable WAL mode for better concurrent access
    conn.execute("PRAGMA journal_mode=WAL")
    # Optimize for faster writes
    conn.execute("PRAGMA synchronous=NORMAL")
    # Increase cache size (10MB)
    conn.execute("PRAGMA cache_size=-10000")

    return conn


def init_db():
    """Initialize database with required tables and indexes"""
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

    # Create indexes for faster queries
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_timestamp 
        ON request_logs(timestamp DESC)
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_file_type 
        ON request_logs(file_type)
    """)

    conn.commit()
    conn.close()
    print("Database initialized successfully with optimized indexes")


def close_db(conn):
    """Close database connection"""
    if conn:
        conn.close()
