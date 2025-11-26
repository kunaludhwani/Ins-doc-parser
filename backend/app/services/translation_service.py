"""
Translation service for multilingual support
Uses OpenAI to translate insurance explanations
"""
from openai import AsyncOpenAI
from app.config import settings


async def translate_to_hindi(english_text: str) -> str:
    """
    Translate insurance explanation from English to Hindi

    Args:
        english_text: English explanation text

    Returns:
        Translated Hindi text
    """
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

        return response.choices[0].message.content

    except Exception as e:
        raise Exception(f"Translation error: {str(e)}")
