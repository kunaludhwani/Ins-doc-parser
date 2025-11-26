"""
Translation service for multilingual support - Optimized with caching
Uses OpenAI to translate insurance explanations
"""
from openai import AsyncOpenAI
from app.config import settings
from app.services.cache_service import cache_service, cache_key_from_text


async def translate_to_hindi(english_text: str) -> str:
    """
    Translate insurance explanation from English to Hindi

    Args:
        english_text: English explanation text

    Returns:
        Translated Hindi text
    """
    # Check cache first - translations are expensive
    cache_key = cache_key_from_text(english_text, "translation_hi")
    cached_translation = cache_service.get(cache_key)

    if cached_translation is not None:
        return cached_translation

    client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    try:
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": """You are a professional translator specializing in insurance and financial documents. 
Translate the following insurance document explanation from English to Hindi.

IMPORTANT RULES:
- Maintain the exact same markdown formatting (**, ✅, ❌, 💡, 🎯, etc.)
- Keep section headers in the same structure
- Translate naturally and accurately
- Use appropriate Hindi financial/insurance terminology
- Keep emojis and bullet points as-is
- Maintain professional tone"""
                },
                {
                    "role": "user",
                    "content": f"Translate this insurance explanation to Hindi:\n\n{english_text}"
                }
            ],
            temperature=0.3,
            max_tokens=2000
        )

        translated_text = response.choices[0].message.content

        # Cache the translation
        cache_service.set(cache_key, translated_text)

        return translated_text

    except Exception as e:
        raise Exception(f"Translation error: {str(e)}")
