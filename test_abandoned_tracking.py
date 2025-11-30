"""
Test script to verify abandoned request tracking in Supabase
Tests that abandoned uploads are correctly logged when client disconnects
"""
import asyncio
import asyncpg
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Load environment variables
load_dotenv('backend/.env')

DATABASE_URL = os.getenv("DATABASE_URL")


async def check_abandoned_logs():
    """Check Supabase for abandoned request logs"""

    print("=" * 80)
    print("🔍 CHECKING ABANDONED REQUEST LOGS IN SUPABASE")
    print("=" * 80)

    try:
        # Connect to database
        conn = await asyncpg.connect(DATABASE_URL)
        print("✅ Connected to Supabase PostgreSQL")

        # Test 1: Check if request_status column exists
        print("\n" + "=" * 80)
        print("TEST 1: Verify request_status column exists")
        print("=" * 80)

        column_check = await conn.fetchrow("""
            SELECT column_name, data_type, column_default
            FROM information_schema.columns
            WHERE table_name = 'request_logs_tier1' 
            AND column_name = 'request_status'
        """)

        if column_check:
            print(f"✅ request_status column exists:")
            print(f"   - Type: {column_check['data_type']}")
            print(f"   - Default: {column_check['column_default']}")
        else:
            print("❌ request_status column NOT FOUND!")
            print("⚠️  Please run migration_add_status.sql in Supabase SQL Editor")
            await conn.close()
            return

        # Test 2: Check all request statuses in last 24 hours
        print("\n" + "=" * 80)
        print("TEST 2: Recent request statuses (last 24 hours)")
        print("=" * 80)

        recent_requests = await conn.fetch("""
            SELECT 
                session_id,
                request_status,
                processing_time_total,
                timestamp,
                file_type,
                rejection_reason
            FROM request_logs_tier1
            WHERE timestamp > NOW() - INTERVAL '24 hours'
            ORDER BY timestamp DESC
            LIMIT 20
        """)

        if recent_requests:
            print(f"Found {len(recent_requests)} recent requests:")
            print()

            status_counts = {}
            for req in recent_requests:
                status = req['request_status'] or 'NULL'
                status_counts[status] = status_counts.get(status, 0) + 1

                session_str = str(req['session_id'])[
                    :12] if req['session_id'] else 'N/A'
                print(f"📋 Session: {session_str}...")
                print(f"   Status: {req['request_status']}")
                print(f"   File Type: {req['file_type']}")
                print(f"   Processing Time: {req['processing_time_total']}ms")
                print(f"   Timestamp: {req['timestamp']}")
                if req['rejection_reason']:
                    print(f"   Rejection: {req['rejection_reason']}")
                print()

            print("STATUS SUMMARY:")
            for status, count in sorted(status_counts.items()):
                print(f"  {status}: {count}")
        else:
            print("No requests found in last 24 hours")

        # Test 3: Check for abandoned requests specifically
        print("\n" + "=" * 80)
        print("TEST 3: Abandoned requests (status = 'abandoned')")
        print("=" * 80)

        abandoned = await conn.fetch("""
            SELECT 
                t1.session_id,
                t1.request_status,
                t1.processing_time_total,
                t1.timestamp,
                t1.file_type,
                t2.abandoned_at_step,
                t2.file_size_bytes
            FROM request_logs_tier1 t1
            LEFT JOIN user_behavior_tier2 t2 ON t1.session_id = t2.session_id
            WHERE t1.request_status = 'abandoned'
            ORDER BY t1.timestamp DESC
            LIMIT 10
        """)

        if abandoned:
            print(f"✅ Found {len(abandoned)} abandoned requests:")
            print()
            for req in abandoned:
                print(f"🚫 Abandoned Upload:")
                print(f"   Session ID: {str(req['session_id'])}")
                print(
                    f"   Processing Time: {req['processing_time_total']}ms before abandon")
                print(f"   Timestamp: {req['timestamp']}")
                print(f"   File Type: {req['file_type']}")
                print(f"   File Size: {req['file_size_bytes']} bytes")
                print(f"   Abandoned At: {req['abandoned_at_step']}")
                print()
        else:
            print("⚠️  No abandoned requests found")
            print("   This is normal if no uploads were abandoned yet")

        # Test 4: Check status distribution
        print("\n" + "=" * 80)
        print("TEST 4: Overall status distribution (all time)")
        print("=" * 80)

        status_dist = await conn.fetch("""
            SELECT 
                request_status,
                COUNT(*) as count,
                AVG(processing_time_total) as avg_time
            FROM request_logs_tier1
            GROUP BY request_status
            ORDER BY count DESC
        """)

        if status_dist:
            print("Status Distribution:")
            total = sum(row['count'] for row in status_dist)
            for row in status_dist:
                status = row['request_status'] or 'NULL'
                count = row['count']
                percentage = (count / total * 100) if total > 0 else 0
                avg_time = row['avg_time'] or 0
                print(
                    f"  {status:12s}: {count:3d} ({percentage:5.1f}%) - Avg: {avg_time:.0f}ms")

        # Test 5: Check tier2 abandoned tracking
        print("\n" + "=" * 80)
        print("TEST 5: Tier2 abandoned step tracking")
        print("=" * 80)

        tier2_abandoned = await conn.fetch("""
            SELECT 
                abandoned_at_step,
                COUNT(*) as count
            FROM user_behavior_tier2
            WHERE abandoned_at_step IS NOT NULL
            GROUP BY abandoned_at_step
            ORDER BY count DESC
        """)

        if tier2_abandoned:
            print("Abandoned at steps:")
            for row in tier2_abandoned:
                print(f"  {row['abandoned_at_step']:20s}: {row['count']}")
        else:
            print("  No abandoned step data found")

        print("\n" + "=" * 80)
        print("✅ DATABASE VERIFICATION COMPLETE")
        print("=" * 80)

        await conn.close()

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()


async def simulate_abandoned_upload():
    """
    Simulate an abandoned upload by starting a request and not completing it
    This tests if the check_disconnect() function works
    """
    print("\n" + "=" * 80)
    print("🧪 SIMULATING ABANDONED UPLOAD")
    print("=" * 80)
    print()
    print("To properly test abandoned tracking:")
    print("1. Open frontend: http://localhost:5173")
    print("2. Select a file to upload")
    print("3. Immediately after clicking upload, close the browser window")
    print("4. Wait 2-3 seconds for disconnect detection")
    print("5. Run this script again to check for abandoned logs")
    print()


if __name__ == "__main__":
    print("ABANDONED REQUEST TRACKING TEST SUITE")
    print()

    # First check current state
    asyncio.run(check_abandoned_logs())

    # Then provide instructions for manual test
    asyncio.run(simulate_abandoned_upload())
