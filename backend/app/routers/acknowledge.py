"""
Acknowledgment router - Track when users actually view results
"""
from fastapi import APIRouter, Request, Header
from pydantic import BaseModel
from typing import Optional
from app.services.logger_tier1 import update_tier1_status
from app.services.logger_tier2 import update_tier2_event

router = APIRouter()


class AcknowledgmentRequest(BaseModel):
    session_id: str
    result_viewed: bool = True


@router.post("/acknowledge")
async def acknowledge_result_viewed(
    ack: AcknowledgmentRequest,
    request: Request,
    session_id: Optional[str] = Header(None, alias="X-Session-ID")
):
    """
    Acknowledge that user actually viewed the result.
    This distinguishes between:
    - Backend completed but user didn't see it (closed browser before response arrived)
    - User actually saw the explanation
    """
    try:
        # Use session_id from header if available, otherwise from body
        sid = session_id or ack.session_id

        if not sid:
            return {"status": "error", "message": "No session_id provided"}

        # Update tier1 status from 'completed_not_viewed' to 'completed'
        await update_tier1_status(
            session_id=sid,
            request_status="completed"
        )

        # Update tier2 to mark result as viewed
        await update_tier2_event(
            session_id=sid,
            event_type="result_viewed",
            value=True
        )

        return {
            "status": "success",
            "message": "Result view acknowledged"
        }

    except Exception as e:
        print(f"❌ Acknowledgment error: {str(e)}")
        # Don't fail the request - this is just analytics
        return {"status": "error", "message": str(e)}
