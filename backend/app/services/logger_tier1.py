"""
Tier 1 Logger: Business-Critical Analytics
Logs core metrics for product decisions and performance monitoring
"""
from app.db.supabase import execute_query
from typing import Optional
from datetime import datetime


async def log_tier1(
    # User & Session
    user_id: str,
    session_id: str,
    user_country: Optional[str] = None,
    user_language_preference: str = "english",
    is_returning_user: bool = False,

    # Document Intelligence
    file_type: str = "",
    document_type: Optional[str] = None,
    insurance_confidence_score: Optional[float] = None,
    rejection_reason: Optional[str] = None,
    validation_failure_reason: Optional[str] = None,
    extraction_method: str = "text",

    # Performance Metrics
    page_count: int = 1,
    text_length: int = 0,
    processing_time_total: Optional[int] = None,
    processing_time_extraction: Optional[int] = None,
    processing_time_classification: Optional[int] = None,
    processing_time_explanation: Optional[int] = None,
    cache_hit: bool = False,
    api_cost_estimate: Optional[float] = None,

    # Core Data
    explanation: str = "",
    request_status: str = "processing"
):
    """
    Log Tier 1 business-critical analytics

    Args:
        All parameters correspond to table columns
    """
    try:
        query = """
            INSERT INTO request_logs_tier1 (
                user_id, session_id, user_country, user_language_preference, is_returning_user,
                file_type, document_type, insurance_confidence_score, rejection_reason, 
                validation_failure_reason, extraction_method,
                page_count, text_length, processing_time_total, processing_time_extraction,
                processing_time_classification, processing_time_explanation, cache_hit, api_cost_estimate,
                explanation, request_status, timestamp
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18, $19, $20, $21, $22)
        """

        await execute_query(
            query,
            user_id, session_id, user_country, user_language_preference, is_returning_user,
            file_type, document_type, insurance_confidence_score, rejection_reason,
            validation_failure_reason, extraction_method,
            page_count, text_length, processing_time_total, processing_time_extraction,
            processing_time_classification, processing_time_explanation, cache_hit, api_cost_estimate,
            explanation, request_status, datetime.now()
        )

    except Exception as e:
        # Don't crash the app if logging fails
        print(f"❌ Tier 1 logging error: {str(e)}")
        import traceback
        traceback.print_exc()


async def update_tier1_status(
    session_id: str,
    request_status: str,
    processing_time_total: Optional[int] = None,
    explanation: Optional[str] = None
):
    """
    Update the status of an existing tier1 log entry

    Args:
        session_id: Session identifier
        request_status: New status ('completed', 'failed', 'rejected', 'abandoned')
        processing_time_total: Updated total processing time
        explanation: Final explanation text (if completed)
    """
    try:
        # Build params list correctly
        params = [request_status]
        updates = ["request_status = $1"]
        param_index = 2

        if processing_time_total is not None:
            updates.append(f"processing_time_total = ${param_index}")
            params.append(processing_time_total)
            param_index += 1

        if explanation is not None:
            updates.append(f"explanation = ${param_index}")
            params.append(explanation)
            param_index += 1

        # Add session_id as last parameter for WHERE clause
        params.append(session_id)

        query = f"""
            UPDATE request_logs_tier1 
            SET {', '.join(updates)}
            WHERE session_id = ${param_index}
            AND request_status = 'processing'
        """

        print(
            f"🔄 Updating tier1 status to '{request_status}' for session {session_id}")
        await execute_query(query, *params)
        print(f"✅ Tier1 status updated successfully")

    except Exception as e:
        print(f"❌ Tier 1 status update error: {str(e)}")
        import traceback
        traceback.print_exc()
