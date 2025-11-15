"""
Logging service
Logs request information to SQLite database
"""
from app.db.database import get_db_connection, close_db
from datetime import datetime


async def log_request(file_type: str, page_count: int, text_length: int, explanation: str):
    """
    Log request information to database

    Args:
        file_type: File extension
        page_count: Number of pages
        text_length: Length of extracted text
        explanation: AI-generated explanation
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO request_logs (file_type, page_count, text_length, explanation)
            VALUES (?, ?, ?, ?)
        """, (file_type, page_count, text_length, explanation))

        conn.commit()
        close_db(conn)

    except Exception as e:
        print(f"Error logging request: {str(e)}")
