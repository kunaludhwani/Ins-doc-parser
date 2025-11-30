"""
Automated E2E test for abandoned request tracking
Simulates a real upload that gets abandoned mid-processing
"""
import asyncio
import aiohttp
import time
import uuid
from pathlib import Path


async def test_abandoned_upload():
    """
    Test abandoned upload by:
    1. Starting an upload request
    2. Closing the connection mid-processing
    3. Verifying the backend detects disconnect and logs as abandoned
    """

    print("=" * 80)
    print("🧪 TESTING ABANDONED UPLOAD TRACKING")
    print("=" * 80)

    # Generate unique session ID
    session_id = str(uuid.uuid4())
    print(f"\n📋 Session ID: {session_id}")

    # Create a test PDF file
    test_pdf_path = Path("test_document.pdf")
    if not test_pdf_path.exists():
        print("⚠️  test_document.pdf not found, creating a dummy one...")
        # Create a simple PDF with basic structure
        pdf_content = b"""%PDF-1.4
1 0 obj
<<
/Type /Catalog
/Pages 2 0 R
>>
endobj
2 0 obj
<<
/Type /Pages
/Kids [3 0 R]
/Count 1
>>
endobj
3 0 obj
<<
/Type /Page
/Parent 2 0 R
/MediaBox [0 0 612 792]
/Contents 4 0 R
/Resources <<
/Font <<
/F1 <<
/Type /Font
/Subtype /Type1
/BaseFont /Helvetica
>>
>>
>>
>>
endobj
4 0 obj
<<
/Length 44
>>
stream
BT
/F1 12 Tf
100 700 Td
(Test Insurance Document) Tj
ET
endstream
endobj
xref
0 5
0000000000 65535 f 
0000000009 00000 n 
0000000058 00000 n 
0000000115 00000 n 
0000000317 00000 n 
trailer
<<
/Size 5
/Root 1 0 R
>>
startxref
410
%%EOF
"""
        test_pdf_path.write_bytes(pdf_content)
        print(f"✅ Created test PDF: {test_pdf_path}")

    print("\n🚀 Starting upload request...")
    print("⏱️  Will disconnect after 2 seconds to simulate abandoned upload")

    try:
        # Create aiohttp session with short timeout
        timeout = aiohttp.ClientTimeout(total=2)  # Disconnect after 2 seconds

        async with aiohttp.ClientSession(timeout=timeout) as session:
            # Prepare multipart form data
            with open(test_pdf_path, 'rb') as f:
                data = aiohttp.FormData()
                data.add_field('file',
                               f,
                               filename='test_insurance.pdf',
                               content_type='application/pdf')

                # Send request with custom headers
                headers = {
                    'X-Session-ID': session_id,
                    'X-Language': 'english'
                }

                try:
                    async with session.post(
                        'http://localhost:8000/upload',
                        data=data,
                        headers=headers
                    ) as response:
                        # This should timeout before completing
                        result = await response.json()
                        print(
                            f"❌ Request completed (should have timed out): {result}")
                        return False

                except asyncio.TimeoutError:
                    print("✅ Connection timed out as expected (simulating disconnect)")
                except aiohttp.ClientError as e:
                    print(
                        f"✅ Connection error as expected: {type(e).__name__}")

    except Exception as e:
        print(f"⚠️  Unexpected error: {str(e)}")

    # Wait for backend to detect disconnect and update database
    print("\n⏳ Waiting 5 seconds for backend to detect disconnect and log...")
    await asyncio.sleep(5)

    # Now verify the logs
    print("\n" + "=" * 80)
    print("🔍 VERIFYING ABANDONED LOG IN DATABASE")
    print("=" * 80)

    import asyncpg
    import os
    from dotenv import load_dotenv

    load_dotenv('backend/.env')
    DATABASE_URL = os.getenv("DATABASE_URL")

    try:
        conn = await asyncpg.connect(DATABASE_URL)

        # Check tier1 logs
        tier1_log = await conn.fetchrow("""
            SELECT 
                session_id,
                request_status,
                processing_time_total,
                file_type,
                timestamp
            FROM request_logs_tier1
            WHERE session_id = $1
        """, uuid.UUID(session_id))

        if tier1_log:
            print(f"\n✅ TIER 1 LOG FOUND:")
            print(f"   Session ID: {tier1_log['session_id']}")
            print(f"   Status: {tier1_log['request_status']}")
            print(
                f"   Processing Time: {tier1_log['processing_time_total']}ms")
            print(f"   File Type: {tier1_log['file_type']}")
            print(f"   Timestamp: {tier1_log['timestamp']}")

            if tier1_log['request_status'] == 'abandoned':
                print("\n✅✅✅ SUCCESS! Request marked as ABANDONED in Tier 1")
            else:
                print(
                    f"\n❌ FAIL: Expected status='abandoned', got '{tier1_log['request_status']}'")
        else:
            print(f"\n❌ TIER 1 LOG NOT FOUND for session {session_id}")

        # Check tier2 logs
        tier2_log = await conn.fetchrow("""
            SELECT 
                session_id,
                abandoned_at_step,
                file_size_bytes,
                timestamp
            FROM user_behavior_tier2
            WHERE session_id = $1
        """, uuid.UUID(session_id))

        if tier2_log:
            print(f"\n✅ TIER 2 LOG FOUND:")
            print(f"   Session ID: {tier2_log['session_id']}")
            print(f"   Abandoned At Step: {tier2_log['abandoned_at_step']}")
            print(f"   File Size: {tier2_log['file_size_bytes']} bytes")
            print(f"   Timestamp: {tier2_log['timestamp']}")

            if tier2_log['abandoned_at_step'] == 'client_disconnect':
                print("\n✅✅✅ SUCCESS! Abandoned step tracked in Tier 2")
            else:
                print(
                    f"\n⚠️  Abandoned step: {tier2_log['abandoned_at_step']}")
        else:
            print(f"\n❌ TIER 2 LOG NOT FOUND for session {session_id}")

        await conn.close()

        # Summary
        print("\n" + "=" * 80)
        if tier1_log and tier1_log['request_status'] == 'abandoned':
            print("✅✅✅ TEST PASSED: Abandoned upload correctly tracked!")
            print("=" * 80)
            return True
        else:
            print("❌ TEST FAILED: Abandoned upload not properly tracked")
            print("=" * 80)
            return False

    except Exception as e:
        print(f"\n❌ Database verification error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def test_successful_upload():
    """
    Test a successful upload to verify normal flow still works
    """
    print("\n" + "=" * 80)
    print("🧪 TESTING SUCCESSFUL UPLOAD (CONTROL TEST)")
    print("=" * 80)

    session_id = str(uuid.uuid4())
    print(f"\n📋 Session ID: {session_id}")

    test_pdf_path = Path("test_document.pdf")

    try:
        async with aiohttp.ClientSession() as session:
            with open(test_pdf_path, 'rb') as f:
                data = aiohttp.FormData()
                data.add_field('file',
                               f,
                               filename='test_insurance.pdf',
                               content_type='application/pdf')

                headers = {
                    'X-Session-ID': session_id,
                    'X-Language': 'english'
                }

                print("🚀 Sending upload request...")
                async with session.post(
                    'http://localhost:8000/upload',
                    data=data,
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=60)
                ) as response:
                    result = await response.json()
                    print(f"✅ Response: {result['status']}")

                    # Verify in database
                    print("\n🔍 Verifying in database...")
                    await asyncio.sleep(1)

                    import asyncpg
                    import os
                    from dotenv import load_dotenv

                    load_dotenv('backend/.env')
                    DATABASE_URL = os.getenv("DATABASE_URL")

                    conn = await asyncpg.connect(DATABASE_URL)

                    tier1_log = await conn.fetchrow("""
                        SELECT request_status
                        FROM request_logs_tier1
                        WHERE session_id = $1
                    """, uuid.UUID(session_id))

                    if tier1_log:
                        status = tier1_log['request_status']
                        print(f"✅ Status in DB: {status}")

                        if status == 'completed':
                            print("✅✅✅ SUCCESS: Completed upload tracked correctly")
                        elif status == 'rejected':
                            print("✅ Document was rejected (not insurance-related)")
                        else:
                            print(f"⚠️  Unexpected status: {status}")

                    await conn.close()

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()


async def main():
    """Run all tests"""
    print("=" * 80)
    print("     ABANDONED REQUEST TRACKING - AUTOMATED TEST SUITE")
    print("=" * 80)
    print()
    print("This test will:")
    print("  1. Simulate an abandoned upload (disconnect mid-processing)")
    print("  2. Verify backend detects disconnect")
    print("  3. Check database logs for 'abandoned' status")
    print("  4. Test successful upload as control")
    print()
    input("Press ENTER to start tests (make sure backend and frontend are running)...")

    # Test 1: Abandoned upload
    test1_passed = await test_abandoned_upload()

    # Test 2: Successful upload
    await test_successful_upload()

    # Final summary
    print("\n" + "=" * 80)
    print("📊 FINAL RESULTS")
    print("=" * 80)
    if test1_passed:
        print("✅ Abandoned tracking: WORKING")
        print("✅ Backend correctly detects client disconnect")
        print("✅ Database logs abandoned requests properly")
    else:
        print("❌ Abandoned tracking: NEEDS INVESTIGATION")
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(main())
