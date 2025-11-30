import asyncio
import asyncpg
import os
from dotenv import load_dotenv

load_dotenv('backend/.env')


async def check():
    conn = await asyncpg.connect(os.getenv("DATABASE_URL"))

    # Check last 5 tier1 logs
    rows = await conn.fetch("""
        SELECT session_id::text, request_status, file_type, 
               TO_CHAR(timestamp, 'HH24:MI:SS') as time
        FROM request_logs_tier1 
        ORDER BY timestamp DESC 
        LIMIT 5
    """)

    print("\nLast 5 uploads:")
    print("-" * 70)
    for r in rows:
        print(
            f"{r['time']} | {r['session_id'][:8]}... | {r['request_status']:10s} | {r['file_type']}")

    # Check for abandoned
    abandoned = await conn.fetchval(
        "SELECT COUNT(*) FROM request_logs_tier1 WHERE request_status = 'abandoned'"
    )

    print(f"\nTotal abandoned uploads: {abandoned}")

    await conn.close()

asyncio.run(check())
