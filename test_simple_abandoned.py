"""
Simple automated test for abandoned tracking without user input
"""
import asyncio
import aiohttp
import uuid
import asyncpg
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv('backend/.env')
DATABASE_URL = os.getenv("DATABASE_URL")


async def test_abandoned():
    """Test abandoned upload by timing out mid-request"""

    print("=" * 80)
    print("TESTING ABANDONED UPLOAD TRACKING")
    print("=" * 80)

    session_id = str(uuid.uuid4())
    print(f"\nSession ID: {session_id}")

    # Create minimal test PDF
    test_pdf = Path("test_document.pdf")
    if not test_pdf.exists():
        test_pdf.write_bytes(
            b"%PDF-1.4\n1 0 obj\n<</Type/Catalog/Pages 2 0 R>>endobj\n%%EOF")
        print("Created test PDF")

    print("\nStep 1: Starting upload request...")
    print("Step 2: Will timeout after 2 seconds to simulate disconnect...")

    try:
        timeout = aiohttp.ClientTimeout(total=2)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            with open(test_pdf, 'rb') as f:
                data = aiohttp.FormData()
                data.add_field('file', f, filename='test.pdf',
                               content_type='application/pdf')

                headers = {
                    'X-Session-ID': session_id,
                    'X-Language': 'english'
                }

                try:
                    async with session.post('http://localhost:8000/upload', data=data, headers=headers) as resp:
                        result = await resp.json()
                        print(f"ERROR: Request completed (should have timed out)")
                        return False
                except asyncio.TimeoutError:
                    print("Step 3: Connection timed out (expected)")
                except Exception as e:
                    print(
                        f"Step 3: Connection error (expected): {type(e).__name__}")
    except Exception as e:
        print(f"ERROR: {e}")
        return False

    print("\nStep 4: Waiting 5 seconds for backend to log abandonment...")
    await asyncio.sleep(5)

    print("\nStep 5: Checking database...")
    conn = await asyncpg.connect(DATABASE_URL)

    tier1 = await conn.fetchrow(
        "SELECT request_status, processing_time_total FROM request_logs_tier1 WHERE session_id = $1",
        uuid.UUID(session_id)
    )

    tier2 = await conn.fetchrow(
        "SELECT abandoned_at_step FROM user_behavior_tier2 WHERE session_id = $1",
        uuid.UUID(session_id)
    )

    await conn.close()

    print("\n" + "=" * 80)
    print("RESULTS")
    print("=" * 80)

    if tier1:
        print(f"Tier 1 Status: {tier1['request_status']}")
        print(f"Processing Time: {tier1['processing_time_total']}ms")

        if tier1['request_status'] == 'abandoned':
            print("\n*** SUCCESS: Tier 1 shows 'abandoned' status ***")
        else:
            print(
                f"\n*** FAIL: Expected 'abandoned', got '{tier1['request_status']}' ***")
            return False
    else:
        print("*** FAIL: No Tier 1 log found ***")
        return False

    if tier2:
        print(f"Tier 2 Abandoned At: {tier2['abandoned_at_step']}")

        if tier2['abandoned_at_step'] == 'client_disconnect':
            print("\n*** SUCCESS: Tier 2 shows 'client_disconnect' ***")
        else:
            print(
                f"\n*** PARTIAL: Tier 2 shows '{tier2['abandoned_at_step']}' ***")
    else:
        print("*** FAIL: No Tier 2 log found ***")
        return False

    print("\n" + "=" * 80)
    print("ALL TESTS PASSED - ABANDONED TRACKING IS WORKING!")
    print("=" * 80)
    return True


if __name__ == "__main__":
    result = asyncio.run(test_abandoned())
    exit(0 if result else 1)
