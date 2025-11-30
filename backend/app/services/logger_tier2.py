"""
Tier 2 Logger: User Behavior & Conversion Analytics
Tracks user actions, quality signals, and conversion events
"""
from app.db.supabase import execute_query
from typing import Optional
from datetime import datetime


async def log_tier2(
    # Link to Tier 1
    session_id: str,
    user_id: str,

    # User Behavior Events
    translation_requested: bool = False,
    pdf_downloaded: bool = False,
    shared_result: bool = False,
    time_on_result_page: Optional[int] = None,
    scroll_depth_percentage: Optional[int] = None,
    abandoned_at_step: Optional[str] = None,

    # Quality Signals
    file_size_bytes: Optional[int] = None,
    image_quality_score: Optional[float] = None,
    text_confidence_score: Optional[float] = None,
    contains_tables: Optional[bool] = None
):
    """
    Log Tier 2 user behavior and conversion metrics

    Args:
        All parameters correspond to table columns
    """
    try:
        query = """
            INSERT INTO user_behavior_tier2 (
                session_id, user_id,
                translation_requested, pdf_downloaded, shared_result,
                time_on_result_page, scroll_depth_percentage, abandoned_at_step,
                file_size_bytes, image_quality_score, text_confidence_score, contains_tables,
                timestamp
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13)
        """

        await execute_query(
            query,
            session_id, user_id,
            translation_requested, pdf_downloaded, shared_result,
            time_on_result_page, scroll_depth_percentage, abandoned_at_step,
            file_size_bytes, image_quality_score, text_confidence_score, contains_tables,
            datetime.now()
        )

    except Exception as e:
        print(f"❌ Tier 2 logging error: {str(e)}")


async def update_tier2_event(
    session_id: str,
    event_type: str,
    value: any = True
):
    """
    Update a specific event in Tier 2 (e.g., when user downloads PDF)

    Args:
        session_id: Session identifier
        event_type: Event column name (e.g., 'pdf_downloaded', 'translation_requested')
        value: Value to set (default: True for boolean events)
    """
    try:
        # Dynamically build query based on event type
        query = f"""
            UPDATE user_behavior_tier2 
            SET {event_type} = $1
            WHERE session_id = $2
        """

        await execute_query(query, value, session_id)

    except Exception as e:
        print(f"❌ Tier 2 event update error: {str(e)}")
