"""
Tier 3 Logger: Advanced Product Intelligence
Captures content analysis, revenue opportunities, and marketing attribution
"""
from app.db.supabase import execute_query
from typing import Optional, Dict, Any
from datetime import datetime
import json


async def log_tier3(
    # Link to Tier 1
    session_id: str,
    user_id: str,

    # Content Analysis
    key_entities_found: Optional[Dict[str, Any]] = None,
    summary_word_count: Optional[int] = None,
    complexity_score: Optional[int] = None,
    language_detected: str = "en",
    contains_personal_info: Optional[bool] = None,

    # Revenue Opportunities
    referrer_source: Optional[str] = None,
    device_type: Optional[str] = None,
    browser: Optional[str] = None,
    came_from_ad_campaign: bool = False,
    utm_source: Optional[str] = None,
    utm_medium: Optional[str] = None,
    utm_campaign: Optional[str] = None
):
    """
    Log Tier 3 advanced product intelligence

    Args:
        All parameters correspond to table columns
    """
    try:
        # Convert dict to JSONB
        entities_json = json.dumps(
            key_entities_found) if key_entities_found else None

        query = """
            INSERT INTO advanced_analytics_tier3 (
                session_id, user_id,
                key_entities_found, summary_word_count, complexity_score, 
                language_detected, contains_personal_info,
                referrer_source, device_type, browser, came_from_ad_campaign,
                utm_source, utm_medium, utm_campaign,
                timestamp
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15)
        """

        await execute_query(
            query,
            session_id, user_id,
            entities_json, summary_word_count, complexity_score,
            language_detected, contains_personal_info,
            referrer_source, device_type, browser, came_from_ad_campaign,
            utm_source, utm_medium, utm_campaign,
            datetime.now()
        )

    except Exception as e:
        print(f"❌ Tier 3 logging error: {str(e)}")
        import traceback
        traceback.print_exc()
