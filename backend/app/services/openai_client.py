"""
OpenAI client service
Handles communication with OpenAI API for financial document explanation
Supports insurance, loans, investments, and all financial documents
Includes streaming support for faster perceived response time
"""
from openai import AsyncOpenAI
from app.config import settings


async def get_insurance_explanation(text: str) -> str:
    """
    Get simplified explanation of financial document using OpenAI
    Handles insurance, loans, investments, mutual funds, FDs, EMIs, etc.

    Args:
        text: Extracted text from financial document

    Returns:
        Formatted explanation with sections
    """
    # Initialize async OpenAI client
    client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    # Craft the prompt
    prompt = f"""You are Sacha Advisor, an AI assistant that simplifies ALL financial documents for everyday people.

Your task is to analyze the following financial document and provide a clear, friendly explanation.

This could be ANY financial document including:
- Insurance policies, claims, coverage documents
- Loan agreements (home, personal, auto, education, business)
- Investment documents (mutual funds, stocks, bonds, SIPs)
- Fixed deposits, recurring deposits, savings schemes
- EMI schedules, payment plans, credit agreements
- Pension plans, provident funds, retirement documents
- Portfolio management, wealth advisory documents
- Bank statements, credit card terms, demat accounts

IMPORTANT RULES:
- Use simple, conversational language (like explaining to a friend)
- Break down complex financial jargon into easy-to-understand terms
- Use analogies where helpful
- DO NOT provide financial advice or recommend what to buy/invest
- DO NOT calculate returns, interest, or premiums yourself
- DO NOT provide legal advice or tax planning
- Only explain what's written in the document

Please structure your response in the following format:

**📋 Summary**
[2-3 sentence overview of what this document is - identify the type: insurance/loan/investment/etc.]

**✅ Key Benefits/Features**
[List the main benefits, features, or terms in bullet points]

**❌ Exclusions/Restrictions**
[List what's NOT covered, restrictions, or limitations in bullet points - if applicable]

**⚠️ Important Things to Know**
[List key terms, conditions, interest rates, maturity periods, charges, penalties, etc.]

**💡 Simple Analogy**
[Explain the document using a simple real-world analogy]

**🎯 5-Point Breakdown**
1. [Most important point]
2. [Second important point]
3. [Third important point]
4. [Fourth important point]
5. [Fifth important point]

Here's the financial document text:

{text[:4000]}

Provide a friendly, helpful explanation:"""

    try:
        # Call OpenAI API asynchronously
        response = await client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are Sacha Advisor, a friendly AI that simplifies ALL financial documents including insurance, loans, investments, mutual funds, fixed deposits, EMI schedules, pension plans, and more. You explain complex financial terms in simple language without providing financial or legal advice."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=1500
        )

        explanation = response.choices[0].message.content
        return explanation

    except Exception as e:
        raise Exception(f"Error getting AI explanation: {str(e)}")


async def get_insurance_explanation_stream(text: str):
    """
    Stream simplified explanation of financial document using OpenAI
    Used for /upload-stream endpoint to provide progressive response

    Args:
        text: Extracted text from financial document

    Yields:
        str: Chunks of explanation as they're generated
    """
    # Initialize async OpenAI client
    client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    # Use the same prompt as non-streaming version
    prompt = f"""You are Sacha Advisor, an AI assistant that simplifies ALL financial documents for everyday people.

Your task is to analyze the following financial document and provide a clear, friendly explanation.

This could be ANY financial document including:
- Insurance policies, claims, coverage documents
- Loan agreements (home, personal, auto, education, business)
- Investment documents (mutual funds, stocks, bonds, SIPs)
- Fixed deposits, recurring deposits, savings schemes
- EMI schedules, payment plans, credit agreements
- Pension plans, provident funds, retirement documents
- Portfolio management, wealth advisory documents
- Bank statements, credit card terms, demat accounts

IMPORTANT RULES:
- Use simple, conversational language (like explaining to a friend)
- Break down complex financial jargon into easy-to-understand terms
- Use analogies where helpful
- DO NOT provide financial advice or recommend what to buy/invest
- DO NOT calculate returns, interest, or premiums yourself
- DO NOT provide legal advice or tax planning
- Only explain what's written in the document

Please structure your response in the following format:

**📋 Summary**
[2-3 sentence overview of what this document is - identify the type: insurance/loan/investment/etc.]

**✅ Key Benefits/Features**
[List the main benefits, features, or terms in bullet points]

**❌ Exclusions/Restrictions**
[List what's NOT covered, restrictions, or limitations in bullet points - if applicable]

**⚠️ Important Things to Know**
[List key terms, conditions, interest rates, maturity periods, charges, penalties, etc.]

**💡 Simple Analogy**
[Explain the document using a simple real-world analogy]

**🎯 5-Point Breakdown**
1. [Most important point]
2. [Second important point]
3. [Third important point]
4. [Fourth important point]
5. [Fifth important point]

Here's the financial document text:

{text[:4000]}

Provide a friendly, helpful explanation:"""

    try:
        # Call OpenAI API with streaming enabled
        stream = await client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are Sacha Advisor, a friendly AI that simplifies ALL financial documents including insurance, loans, investments, mutual funds, fixed deposits, EMI schedules, pension plans, and more. You explain complex financial terms in simple language without providing financial or legal advice."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=1500,
            stream=True  # Enable streaming
        )

        # Yield chunks as they arrive
        async for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

    except Exception as e:
        raise Exception(f"Error streaming AI explanation: {str(e)}")
