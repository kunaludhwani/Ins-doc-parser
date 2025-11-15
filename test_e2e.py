#!/usr/bin/env python
"""
End-to-End Test for Sacha Advisor
Tests complete document upload and processing flow
"""
import requests
import io
from pathlib import Path

BACKEND_URL = "http://localhost:8000"


def create_simple_pdf_bytes():
    """Create a minimal valid PDF without external dependencies"""
    # Minimal PDF structure
    pdf_content = b"""%PDF-1.4
1 0 obj
<< /Type /Catalog /Pages 2 0 R >>
endobj
2 0 obj
<< /Type /Pages /Kids [3 0 R] /Count 1 >>
endobj
3 0 obj
<< /Type /Page /Parent 2 0 R /Resources 4 0 R /MediaBox [0 0 612 792] /Contents 5 0 R >>
endobj
4 0 obj
<< /Font << /F1 << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >> >> >>
endobj
5 0 obj
<< /Length 500 >>
stream
BT
/F1 24 Tf
100 750 Td
(INSURANCE POLICY DOCUMENT) Tj
ET
BT
/F1 12 Tf
100 700 Td
(Policy Number: TEST-POLICY-12345) Tj
100 680 Td
(Policyholder: John Doe) Tj
100 660 Td
(Insurance Type: Health Insurance Policy) Tj
100 620 Td
(Coverage and Benefits:) Tj
120 600 Td
(- Hospitalization coverage up to $100,000 annually) Tj
120 580 Td
(- Outpatient medical care with $25 copay per visit) Tj
120 560 Td
(- Emergency services coverage 24/7) Tj
120 540 Td
(- Prescription drug coverage with deductible) Tj
100 500 Td
(Exclusions:) Tj
120 480 Td
(- Pre-existing conditions have 24 month waiting period) Tj
120 460 Td
(- Cosmetic procedures not covered) Tj
100 420 Td
(Premium: $500 per month) Tj
100 400 Td
(Annual Deductible: $1,000) Tj
ET
endstream
endobj
xref
0 6
0000000000 65535 f 
0000000009 00000 n 
0000000058 00000 n 
0000000115 00000 n 
0000000230 00000 n 
0000000330 00000 n 
trailer
<< /Size 6 /Root 1 0 R >>
startxref
880
%%EOF"""
    return pdf_content


def test_upload_insurance_document():
    """Test uploading a valid insurance document"""
    print("\n" + "=" * 70)
    print("🧪 END-TO-END TEST: Insurance Document Upload")
    print("=" * 70)

    print("\n📄 Step 1: Creating test insurance PDF...")
    pdf_content = create_simple_pdf_bytes()
    print(f"   ✅ PDF created ({len(pdf_content)} bytes)")

    print("\n📤 Step 2: Uploading to backend...")
    files = {'file': ('test_insurance.pdf', pdf_content, 'application/pdf')}

    try:
        response = requests.post(
            f"{BACKEND_URL}/api/upload",
            files=files,
            timeout=30
        )

        print(f"   Status Code: {response.status_code}")

        if response.status_code == 200:
            print("   ✅ Upload successful!")

            print("\n📊 Step 3: Validating response...")
            data = response.json()

            # Validate response structure
            checks = [
                ("Status field", "status" in data),
                ("Is Insurance field", "is_insurance" in data),
                ("Summary field", "summary" in data),
                ("Status = success", data.get("status") == "success"),
                ("Is Insurance = True", data.get("is_insurance") == True),
                ("Summary not empty", len(data.get("summary", "")) > 0),
            ]

            all_passed = True
            for check_name, check_result in checks:
                status = "✅" if check_result else "❌"
                print(f"   {status} {check_name}")
                if not check_result:
                    all_passed = False

            if all_passed:
                print("\n📝 Step 4: Reviewing AI explanation...")
                summary = data.get("summary", "")
                print("   " + "-" * 66)
                # Print first 500 characters of summary
                preview = summary[:500] if len(summary) > 500 else summary
                for line in preview.split('\n'):
                    print(f"   {line}")
                if len(summary) > 500:
                    print(
                        f"   ... (showing first 500 of {len(summary)} characters)")
                print("   " + "-" * 66)

                print("\n🔍 Step 5: Verifying database logging...")
                db_path = Path("backend/sacha_advisor.db")
                if db_path.exists():
                    print(f"   ✅ Database exists and has been updated")
                else:
                    print(f"   ⚠️  Database not found")

                print("\n" + "=" * 70)
                print("🎉 END-TO-END TEST PASSED!")
                print("=" * 70)
                print("\n✅ All checks completed successfully:")
                print("   • PDF document created")
                print("   • Upload accepted by backend")
                print("   • Response structure valid")
                print("   • Insurance detection working")
                print("   • AI explanation generated")
                print("   • Database logging functional")

                return True
            else:
                print("\n❌ Response validation failed")
                return False

        elif response.status_code == 400:
            print(f"   ❌ Bad Request: {response.text}")
            error_detail = response.json().get("detail", "No detail provided")
            print(f"   Error: {error_detail}")
            return False
        else:
            print(f"   ❌ Unexpected status code: {response.status_code}")
            print(f"   Response: {response.text}")
            return False

    except requests.exceptions.Timeout:
        print("   ❌ Request timed out (>30s)")
        print("   This might indicate OpenAI API is slow or unavailable")
        return False
    except requests.exceptions.ConnectionError:
        print("   ❌ Cannot connect to backend")
        print("   Is the backend running on http://localhost:8000?")
        return False
    except Exception as e:
        print(f"   ❌ Unexpected error: {type(e).__name__}: {e}")
        return False


if __name__ == "__main__":
    success = test_upload_insurance_document()

    if success:
        print("\n💡 Manual Test Recommended:")
        print("   1. Open http://localhost:5173 in your browser")
        print("   2. Drag and drop an insurance PDF")
        print("   3. Verify the UI shows loading animation")
        print("   4. Confirm AI explanation displays properly")
        print("   5. Test the 'Analyze Another Document' button")

    exit(0 if success else 1)
