"""
Translation router
Handles translation requests for multilingual support
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.translation_service import translate_to_hindi
from app.schemas.responses import TranslationResponse

router = APIRouter()


class TranslateRequest(BaseModel):
    text: str
    target_language: str = "hi"  # Hindi by default


@router.post("/translate", response_model=TranslationResponse)
async def translate_text(request: TranslateRequest):
    """
    Translate text to target language
    Currently supports Hindi (hi)
    """
    try:
        if request.target_language != "hi":
            raise HTTPException(
                status_code=400,
                detail="Currently only Hindi (hi) translation is supported"
            )

        translated_text = await translate_to_hindi(request.text)

        return TranslationResponse(
            status="success",
            translated_text=translated_text,
            language=request.target_language
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Translation failed: {str(e)}"
        )
