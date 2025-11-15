#!/usr/bin/env python
"""
Smoke test for Sacha Advisor
Tests the complete end-to-end flow
"""
import requests
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io

# Configuration
BACKEND_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:5173"


def create_test_insurance_pdf():
    """Create a simple test insurance PDF"""
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)

    # Add insurance-related content
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, 750, "INSURANCE POLICY DOCUMENT")

    c.setFont("Helvetica", 12)
    c.drawString(100, 720, "Policy Number: TEST-12345")
    c.drawString(100, 700, "Policyholder: Test User")
    c.drawString(100, 680, "Coverage Type: Health Insurance")

    c.drawString(100, 640, "Benefits:")
    c.drawString(120, 620, "- Hospitalization coverage up to $100,000")
    c.drawString(120, 600, "- Outpatient care coverage")
    c.drawString(120, 580, "- Emergency services coverage")
    c.drawString(120, 560, "- Prescription drug coverage")

    c.drawString(100, 520, "Exclusions:")
    c.drawString(
        120, 500, "- Pre-existing conditions (24 month waiting period)")
    c.drawString(120, 480, "- Cosmetic procedures")
    c.drawString(120, 460, "- Experimental treatments")

    c.drawString(100, 420, "Premium: $500 per month")
    c.drawString(100, 400, "Deductible: $1,000 annually")
    c.drawString(100, 380, "Copay: $25 per visit")

    c.save()
    buffer.seek(0)
    return buffer.getvalue()


def test_health_check():
    """Test 1: Health check endpoint"""
    print("🔍 Test 1: Health Check")
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        print("✅ Health check passed")
        return True
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False


def test_upload_valid_insurance():
    """Test 2: Upload valid insurance document"""
    print("\n🔍 Test 2: Upload Valid Insurance Document")
    try:
        # Create test PDF
        pdf_content = create_test_insurance_pdf()

        # Upload
        files = {'file': ('test_insurance.pdf',
                          pdf_content, 'application/pdf')}
        response = requests.post(
            f"{BACKEND_URL}/api/upload", files=files, timeout=30)

        print(f"Status Code: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            assert data["status"] == "success"
            assert data["is_insurance"] == True
            assert "summary" in data
            # Should have substantial explanation
            assert len(data["summary"]) > 100
            print("✅ Valid insurance upload passed")
            print(f"📝 Summary preview: {data['summary'][:200]}...")
            return True
        else:
            print(f"❌ Upload failed: {response.text}")
            return False

    except Exception as e:
        print(f"❌ Upload test failed: {e}")
        return False


def test_file_validation():
    """Test 3: File validation (oversized file)"""
    print("\n🔍 Test 3: File Validation - Oversized File")
    try:
        # Create oversized PDF (simulate)
        large_content = b"PDF" + (b"x" * (60 * 1024 * 1024))  # 60MB

        files = {'file': ('large.pdf', large_content, 'application/pdf')}
        response = requests.post(
            f"{BACKEND_URL}/api/upload", files=files, timeout=30)

        # Should return 400 Bad Request
        if response.status_code == 400:
            print("✅ File size validation working")
            return True
        else:
            print(f"⚠️ Expected 400, got {response.status_code}")
            return False

    except Exception as e:
        print(f"❌ Validation test failed: {e}")
        return False


def test_non_insurance_document():
    """Test 4: Reject non-insurance document"""
    print("\n🔍 Test 4: Non-Insurance Document Detection")
    try:
        # Create non-insurance PDF
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        c.setFont("Helvetica", 12)
        c.drawString(100, 750, "This is a random document")
        c.drawString(100, 730, "It has nothing to do with insurance")
        c.drawString(100, 710, "Just some random text here")
        c.save()
        buffer.seek(0)

        files = {'file': ('random.pdf', buffer.getvalue(), 'application/pdf')}
        response = requests.post(
            f"{BACKEND_URL}/api/upload", files=files, timeout=30)

        # Should return 400 - not insurance
        if response.status_code == 400 and "insurance" in response.text.lower():
            print("✅ Non-insurance detection working")
            return True
        else:
            print(f"⚠️ Expected rejection, got {response.status_code}")
            print(f"Response: {response.text}")
            return False

    except Exception as e:
        print(f"❌ Non-insurance test failed: {e}")
        return False


def run_smoke_tests():
    """Run all smoke tests"""
    print("=" * 60)
    print("🚀 SACHA ADVISOR - SMOKE TEST SUITE")
    print("=" * 60)

    results = []

    # Run tests
    results.append(("Health Check", test_health_check()))
    results.append(("Valid Insurance Upload", test_upload_valid_insurance()))
    results.append(("File Size Validation", test_file_validation()))
    results.append(("Non-Insurance Detection", test_non_insurance_document()))

    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")

    print("\n" + "=" * 60)
    print(f"Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 ALL TESTS PASSED!")
        return True
    else:
        print(f"⚠️ {total - passed} test(s) failed")
        return False


if __name__ == "__main__":
    success = run_smoke_tests()
    exit(0 if success else 1)
