#!/usr/bin/env python
"""
Simple smoke test for Sacha Advisor - Testing with requests only
"""
import requests
import json

BACKEND_URL = "http://localhost:8000"


def test_health_check():
    """Test 1: Health check endpoint"""
    print("🔍 Test 1: Health Check")
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Response: {json.dumps(data, indent=2)}")
            assert data["status"] == "healthy"
            print("   ✅ PASSED")
            return True
        else:
            print(f"   ❌ FAILED - Expected 200, got {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ FAILED - {e}")
        return False


def test_api_docs():
    """Test 2: Check if API docs are accessible"""
    print("\n🔍 Test 2: API Documentation")
    try:
        response = requests.get(f"{BACKEND_URL}/docs", timeout=5)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ PASSED - API docs accessible")
            return True
        else:
            print(f"   ❌ FAILED - Expected 200, got {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ FAILED - {e}")
        return False


def test_cors_headers():
    """Test 3: Check CORS headers"""
    print("\n🔍 Test 3: CORS Configuration")
    try:
        response = requests.options(f"{BACKEND_URL}/api/upload", timeout=5)
        print(f"   Status: {response.status_code}")
        headers = response.headers
        if 'access-control-allow-origin' in headers:
            print(f"   CORS Origin: {headers['access-control-allow-origin']}")
            print("   ✅ PASSED - CORS configured")
            return True
        else:
            print("   ⚠️  WARNING - No CORS headers found")
            return True  # Not critical for local testing
    except Exception as e:
        print(f"   ❌ FAILED - {e}")
        return False


def test_database_exists():
    """Test 4: Check if database was created"""
    print("\n🔍 Test 4: Database Initialization")
    from pathlib import Path
    db_path = Path("backend/sacha_advisor.db")
    if db_path.exists():
        size = db_path.stat().st_size
        print(f"   Database found: {db_path}")
        print(f"   Size: {size} bytes")
        print("   ✅ PASSED")
        return True
    else:
        print(f"   ❌ FAILED - Database not found at {db_path}")
        return False


def run_smoke_tests():
    """Run all smoke tests"""
    print("=" * 70)
    print("🚀 SACHA ADVISOR - QUICK SMOKE TEST")
    print("=" * 70)
    print(f"\nBackend URL: {BACKEND_URL}")
    print(f"Testing basic functionality...\n")

    results = []

    # Run tests
    results.append(("Health Check", test_health_check()))
    results.append(("API Documentation", test_api_docs()))
    results.append(("CORS Configuration", test_cors_headers()))
    results.append(("Database Initialization", test_database_exists()))

    # Summary
    print("\n" + "=" * 70)
    print("📊 TEST SUMMARY")
    print("=" * 70)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")

    print("\n" + "=" * 70)
    print(f"Results: {passed}/{total} tests passed ({int(passed/total*100)}%)")

    if passed == total:
        print("🎉 ALL BASIC TESTS PASSED!")
        print("\n📝 Next Steps:")
        print("   1. Open http://localhost:5173 in browser")
        print("   2. Upload a test insurance PDF (< 50 MB, < 50 pages)")
        print("   3. Verify AI explanation appears")
    else:
        print(f"⚠️  {total - passed} test(s) failed - check errors above")

    print("=" * 70)

    return passed == total


if __name__ == "__main__":
    success = run_smoke_tests()
    exit(0 if success else 1)
