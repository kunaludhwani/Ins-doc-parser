"""
Supabase PostgreSQL connection management
Provides async connection pooling for all database operations
"""
import asyncpg
from app.config import settings
from typing import Optional

# Global connection pool
_pool: Optional[asyncpg.Pool] = None


async def get_pool() -> asyncpg.Pool:
    """
    Get or create the global connection pool
    Optimized for high concurrency with larger pool and faster timeout

    Returns:
        asyncpg.Pool: Connection pool instance
    """
    global _pool

    if _pool is None:
        _pool = await asyncpg.create_pool(
            dsn=settings.DATABASE_URL,
            min_size=5,   # Increased from 2 for better concurrency
            max_size=30,  # Increased from 10 for high traffic
            command_timeout=20,  # Reduced from 60 for fail-fast behavior
            max_inactive_connection_lifetime=300,
            server_settings={
                'application_name': 'sacha_advisor_backend',
                'jit': 'off'  # Disable JIT compilation for faster simple queries
            }
        )
        print(f"✅ Supabase pool created: 5-30 connections (optimized)")

    return _pool


async def close_pool():
    """
    Close the connection pool gracefully
    """
    global _pool

    if _pool is not None:
        await _pool.close()
        _pool = None


async def init_db():
    """
    Initialize database connection and verify tables exist
    This should be called on application startup
    """
    try:
        pool = await get_pool()

        async with pool.acquire() as conn:
            # Verify all 3 tables exist
            tables = await conn.fetch("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name IN ('request_logs_tier1', 'user_behavior_tier2', 'advanced_analytics_tier3')
            """)

            table_names = [row['table_name'] for row in tables]

            if len(table_names) == 3:
                print(f"✅ Supabase connected: All 3 analytics tables verified")
            else:
                missing = set(['request_logs_tier1', 'user_behavior_tier2',
                              'advanced_analytics_tier3']) - set(table_names)
                print(f"⚠️  Warning: Missing tables: {missing}")

    except Exception as e:
        print(f"❌ Supabase connection failed: {str(e)}")
        raise


async def execute_query(query: str, *args):
    """
    Execute a query without returning results (INSERT, UPDATE, DELETE)

    Args:
        query: SQL query string
        *args: Query parameters
    """
    pool = await get_pool()
    async with pool.acquire() as conn:
        await conn.execute(query, *args)


async def fetch_one(query: str, *args):
    """
    Fetch a single row

    Args:
        query: SQL query string
        *args: Query parameters

    Returns:
        Record or None
    """
    pool = await get_pool()
    async with pool.acquire() as conn:
        return await conn.fetchrow(query, *args)


async def fetch_all(query: str, *args):
    """
    Fetch multiple rows

    Args:
        query: SQL query string
        *args: Query parameters

    Returns:
        List of Records
    """
    pool = await get_pool()
    async with pool.acquire() as conn:
        return await conn.fetch(query, *args)
