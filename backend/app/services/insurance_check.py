"""
Financial document detection service
Uses OpenAI for semantic document classification
Accepts insurance and all financial services documents
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
                    "content": """You are a document classification expert specializing in ALL financial documents including insurance, banking, investments, loans, and wealth management.

Your task: Determine if this document is ANY type of financial document.

✅ ACCEPT ALL OF THESE FINANCIAL DOCUMENTS:

Insurance Documents:
- All insurance policies (life, health, motor, property, travel, cyber, liability, etc.)
- Insurance claims, settlements, coverage documents
- Premium notices, policy schedules, endorsements, proposals

Banking Documents:
- Loan agreements (personal, home, auto, business, education)
- Credit card statements, agreements, terms
- Fixed deposit receipts, certificates
- Bank statements, passbooks, account opening forms
- Overdraft facilities, credit lines

Investment Documents:
- Mutual fund statements, SIPs, NAV reports
- Demat account statements, trading accounts
- Stock certificates, share allotment letters
- Bond documents, debentures, securities
- Investment advisory reports, portfolio statements

Retirement & Pension:
- Provident fund statements (EPF, PPF, VPF)
- National Pension System (NPS) documents
- Pension plans, annuity documents
- Gratuity, superannuation documents

Wealth Management:
- Portfolio management services (PMS) documents
- Financial planning reports, wealth advisory
- Estate planning, trust documents
- Tax planning documents, capital gains reports

Alternative Investments:
- ULIP documents
- REIT, InvIT documents
- Gold bonds, sovereign bonds
- Commodities trading documents

EMI & Payment Documents:
- EMI schedules, payment plans
- Buy now pay later (BNPL) agreements
- Payment gateway documents

❌ REJECT ONLY THESE (Non-Financial):
- Pure personal identity documents (passport, Aadhaar, driver's license) WITHOUT financial context
- Employment documents (CVs, offer letters) WITHOUT salary/benefits info
- Pure medical records WITHOUT insurance/claims
- Educational certificates
- General business contracts WITHOUT financial terms
- Travel tickets, hotel bookings WITHOUT financial protection
- Utility bills (unless related to loan/payment plan)

⚠️ CRITICAL RULES:
- If document has ANY financial terms (amount, interest, premium, NAV, returns, EMI, principal) → ACCEPT
- If from ANY financial institution (bank, NBFC, insurer, broker, advisor, fintech) → ACCEPT
- If mentions money, investments, loans, coverage, benefits → ACCEPT
- When in doubt → ACCEPT (very low rejection threshold)
- Confidence: 0.8+ for clear financial docs, 0.6+ for borderline financial docs

Respond in JSON format:
{
    "is_insurance": true/false,
    "confidence": 0.0-1.0,
    "document_type": "loan agreement" or "mutual fund" or "insurance policy" or "FD certificate" etc,
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
        # Fallback to basic keyword check for financial terms
        financial_keywords = ["insurance", "policy", "loan", "emi", "mutual fund", "investment",
                              "bank", "credit", "debit", "premium", "interest", "principal",
                              "nav", "portfolio", "pension", "provident", "deposit", "fd", "rd"]
        is_financial = any(keyword in text.lower()
                           for keyword in financial_keywords)

        return {
            "is_insurance": is_financial,
            "confidence": 0.5,
            "document_type": "financial_document",
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
                    "content": "You are a helpful assistant explaining why Sacha Advisor can only analyze financial documents. Be friendly and concise."
                },
                {
                    "role": "user",
                    "content": f"The user uploaded a '{document_type}'. Explain in 2-3 friendly sentences why Sacha Advisor can't analyze this document (we only handle ALL financial documents including insurance policies, loan agreements, investment documents, mutual funds, fixed deposits, EMI schedules, pension plans, bank statements, credit cards, and any banking/finance/investment related documents). Suggest what type of financial document they should upload instead."
                }
            ],
            temperature=0.7,
            max_tokens=150
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"Rejection message generation error: {str(e)}")
        return f"This appears to be a {document_type}, not a financial document. Sacha Advisor can analyze ALL financial documents including insurance, loans, investments, mutual funds, fixed deposits, EMI schedules, pension plans, bank statements, and more. Please upload any financial document to get started!"
