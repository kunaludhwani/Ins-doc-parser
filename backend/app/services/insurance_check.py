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
                    "content": """You are a document classification expert specializing in BFSI (Banking, Financial Services, and Insurance) documents.

Your task: Determine if this document is related to insurance, finance, or financial services.

✅ ACCEPT ALL OF THESE:

Insurance Documents:
- Insurance policies (all types: life, health, motor, property, travel, cyber, professional liability, etc.)
- Insurance claim forms and claim settlements
- Coverage documents, policy summaries, certificates
- Insurance product brochures, marketing materials, proposals
- Benefit illustrations, policy schedules, endorsements
- Premium notices, renewal documents, quotations
- Insurance applications, underwriting documents
- Reinsurance agreements, treaty documents
- Loss reports, risk assessments, actuarial reports

Financial Services Documents:
- Investment products (mutual funds, bonds, annuities)
- Pension plans, retirement plans, provident funds
- Financial advisory documents, wealth management proposals
- Banking products with insurance components (loan protection, credit life)
- Mortgage insurance, title insurance documents
- Surety bonds, guarantee documents
- Employee benefits documents (group insurance, health benefits)

Insurtech & Industry Documents:
- Insurance technology product descriptions
- Digital insurance platforms, apps, services
- Insurance aggregator comparisons
- Regulatory filings, compliance documents
- Insurance industry reports, market analysis
- Parametric insurance, microinsurance documents

❌ REJECT ONLY:
- Pure personal identity documents (passport, driver's license, national ID)
- Employment-only documents (reference letters, CVs, job offers) WITHOUT insurance/benefits info
- Pure medical records (prescriptions, lab reports, discharge summaries) WITHOUT insurance claims
- General business contracts with NO insurance/financial component
- Educational certificates, transcripts
- Property deeds, lease agreements WITHOUT insurance component

⚠️ IMPORTANT:
- If document mentions insurance, premiums, coverage, claims, benefits, financial protection → ACCEPT
- If document is from insurance company, broker, agent, insurtech → ACCEPT
- If document relates to BFSI industry → ACCEPT
- When in doubt → ACCEPT (low rejection threshold)
- Confidence should be 0.7+ for clear insurance docs, 0.5-0.7 for finance-related

Respond in JSON format:
{
    "is_insurance": true/false,
    "confidence": 0.0-1.0,
    "document_type": "insurance policy" or "financial services" or "claim form" etc,
    "reason": "brief explanation"
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
                    "content": f"The user uploaded a '{document_type}'. Explain in 2-3 friendly sentences why Sacha Advisor can't analyze this document (we only handle insurance, financial services, BFSI, and insurtech-related documents including policies, claims, investment products, pension plans, and financial protection documents). Suggest what they should upload instead."
                }
            ],
            temperature=0.7,
            max_tokens=150
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"Rejection message generation error: {str(e)}")
        return f"This appears to be a {document_type}, not an insurance document. Sacha Advisor can only analyze insurance policies, claims, and coverage documents. Please upload a valid insurance document to get started!"
