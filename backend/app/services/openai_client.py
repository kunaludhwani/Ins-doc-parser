"""
OpenAI client service
Handles communication with OpenAI API for document explanation
"""
from openai import AsyncOpenAI
from app.config import settings


async def get_insurance_explanation(text: str) -> str:
    """
    Get simplified explanation of insurance document using OpenAI

    Args:
        text: Extracted text from insurance document

    Returns:
        Formatted explanation with sections
    """
    # Initialize async OpenAI client
    client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    # Craft the prompt
    prompt = f"""You are Sacha Advisor, an AI assistant that simplifies insurance documents for everyday people.

Your task is to analyze the following insurance policy document and provide a clear, friendly explanation.

IMPORTANT RULES:
- Use simple, conversational language (like explaining to a friend)
- Break down complex insurance jargon into easy-to-understand terms
- Use analogies where helpful
- DO NOT provide financial advice or recommend what policy to buy
- DO NOT calculate premiums or suggest coverage amounts
- DO NOT provide legal advice
- Only explain what's written in the document

Please structure your response in the following format:

**📋 Summary**
[2-3 sentence overview of what this policy is]

**✅ Key Benefits**
[List the main benefits/coverage in bullet points]

**❌ Exclusions**
[List what's NOT covered in bullet points]

**⚠️ Important Things to Know**
[List key terms, conditions, waiting periods, etc.]

**💡 Simple Analogy**
[Explain the policy using a simple real-world analogy]

**🎯 5-Point Breakdown**
1. [Most important point]
2. [Second important point]
3. [Third important point]
4. [Fourth important point]
5. [Fifth important point]

Here's the insurance document text:

{text[:4000]}

Provide a friendly, helpful explanation:"""

    try:
        # Call OpenAI API asynchronously
        response = await client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are Sacha Advisor, a friendly AI that simplifies insurance documents. You explain complex insurance terms in simple language without providing financial or legal advice."
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
