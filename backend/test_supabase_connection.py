"""
Supabase Connection Diagnostic Script
Run this to test your Supabase connection independently
"""
import asyncio
import asyncpg
from dotenv import load_dotenv
import os

load_dotenv()


async def test_connection():
    database_url = os.getenv("DATABASE_URL")

    print("="*60)
    print("🔍 SUPABASE CONNECTION DIAGNOSTIC")
    print("="*60)

    if not database_url:
        print("❌ DATABASE_URL not found in .env file")
        return

    # Parse URL to show (without exposing password)
    parts = database_url.split("@")
    if len(parts) > 1:
        host_info = parts[1]
        print(f"📍 Attempting connection to: {host_info}")

    print("\nTesting connection...")

    try:
        # Try to create a single connection (simpler than pool)
        conn = await asyncpg.connect(database_url, timeout=10)
        print("✅ Connection successful!")

        # Test query
        version = await conn.fetchval('SELECT version()')
        print(f"📊 PostgreSQL version: {version[:50]}...")

        # Check tables
        tables = await conn.fetch("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name IN ('request_logs_tier1', 'user_behavior_tier2', 'advanced_analytics_tier3')
        """)

        print(f"\n📋 Tables found: {len(tables)}/3")
        for table in tables:
            print(f"   ✓ {table['table_name']}")

        await conn.close()
        print("\n✅ All checks passed! Supabase is ready to use.")

    except asyncpg.exceptions.InvalidPasswordError:
        print("❌ Invalid password. Check your DATABASE_URL password.")
    except asyncio.TimeoutError:
        print("❌ Connection timeout. Database might still be provisioning.")
        print("   Wait 2-3 minutes and try again.")
    except Exception as e:
        print(f"❌ Connection failed: {str(e)}")
        print("\n🔧 Troubleshooting:")
        print("   1. Check DATABASE_URL in .env file")
        print("   2. Verify Supabase project is active (not paused)")
        print("   3. Ensure tables are created (run SQL in Supabase dashboard)")
        print("   4. Check firewall/VPN isn't blocking connection")
        print("   5. Wait 2-3 minutes if project was just created")

if __name__ == "__main__":
    asyncio.run(test_connection())
