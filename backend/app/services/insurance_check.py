"""
Insurance document detection service
Uses OpenAI for semantic document classification
"""
from openai import AsyncOpenAI
from app.config import settings
import json


async def classify_document_with_ai(text: str) -> dict:
    """
    Use OpenAI to semantically classify if document is insurance-related

    Args:
        text: Extracted text from document

    Returns:
        dict: {
            "is_insurance": bool,
            "confidence": float,
            "document_type": str,
            "reason": str
        }
    """
    # Truncate text to first 3000 characters for classification
    text_sample = text[:3000]

    try:
        client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": """You are a document classification expert. Analyze the provided document text and determine:
1. Is this an insurance-related document? (policy, claim form, coverage document, brochure, product description, etc.)
2. What type of document is it?
3. Confidence level (0.0 to 1.0)
4. Brief explanation

ACCEPTABLE INSURANCE DOCUMENTS:
- Insurance policies (life, health, motor, property, travel, etc.)
- Insurance claim forms
- Coverage documents and summaries
- Insurance product brochures and marketing materials
- Insurance benefit descriptions
- Policy renewal notices
- Insurance certificates
- Any document explaining insurance products or coverage

REJECT ONLY IF:
- Personal documents (passport, ID, bank statements)
- Employment documents (reference letters, salary slips)
- Medical documents (prescriptions, test reports)
- Legal contracts unrelated to insurance
- General business documents

Respond in JSON format:
{
    "is_insurance": true/false,
    "confidence": 0.0-1.0,
    "document_type": "insurance policy" or "reference letter" or "claim form" or "insurance brochure" etc,
    "reason": "brief explanation why this is/isn't an insurance document"
}"""
                },
                {
                    "role": "user",
                    "content": f"Classify this document:\n\n{text_sample}"
                }
            ],
            temperature=0.3,
            max_tokens=200
        )

        result = json.loads(response.choices[0].message.content)
        return result

    except Exception as e:
        print(f"AI classification error: {str(e)}")
        # Fallback to basic keyword check
        return {
            "is_insurance": "insurance" in text.lower() or "policy" in text.lower(),
            "confidence": 0.5,
            "document_type": "unknown",
            "reason": "AI classification unavailable, using basic keyword matching"
        }


async def generate_rejection_message(document_type: str, reason: str) -> str:
    """
    Generate a friendly explanation for why the document can't be analyzed

    Args:
        document_type: Type of document detected
        document_reason: Reason for rejection

    Returns:
        str: Human-friendly explanation
    """
    try:
        client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant explaining why Sacha Advisor can only analyze insurance documents. Be friendly and concise."
                },
                {
                    "role": "user",
                    "content": f"The user uploaded a '{document_type}'. Explain in 2-3 friendly sentences why Sacha Advisor can't analyze this document (we only handle insurance policies, claims, coverage documents, brochures, and insurance product materials). Suggest what they should upload instead."
                }
            ],
            temperature=0.7,
            max_tokens=150
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"Rejection message generation error: {str(e)}")
        return f"This appears to be a {document_type}, not an insurance document. Sacha Advisor can only analyze insurance policies, claims, and coverage documents. Please upload a valid insurance document to get started!"
