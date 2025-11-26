"""
Create a test PDF document for testing
"""
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch


def create_test_pdf():
    filename = "test_insurance_policy.pdf"
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(inch, height - inch, "Life Insurance Policy Document")

    # Content
    c.setFont("Helvetica", 12)
    y = height - 1.5 * inch

    content = [
        "Policy Number: LIC/2024/123456",
        "Policyholder: John Doe",
        "Sum Assured: ₹50,00,000",
        "Premium: ₹25,000 per annum",
        "Policy Term: 20 years",
        "",
        "Coverage Details:",
        "- Death Benefit: Sum Assured plus accumulated bonuses",
        "- Maturity Benefit: Sum Assured if policyholder survives",
        "- Riders Available: Accidental Death, Critical Illness",
        "",
        "Premium Payment:",
        "- Payment Mode: Annual, Semi-annual, Quarterly, Monthly",
        "- Grace Period: 30 days for annual payments",
        "",
        "Exclusions:",
        "- Suicide within 12 months of policy start",
        "- Death due to undisclosed pre-existing conditions",
        "- War, terrorism, nuclear risks",
        "",
        "Free Look Period: 30 days from policy receipt"
    ]

    for line in content:
        c.drawString(inch, y, line)
        y -= 0.3 * inch

    c.save()
    print(f"✅ Created {filename}")
    return filename


if __name__ == "__main__":
    create_test_pdf()
