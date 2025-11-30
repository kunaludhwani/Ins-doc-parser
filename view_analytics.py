"""
View daily analytics dashboard
Shows simple metrics for last 30 days
"""
import asyncio
import asyncpg
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv('backend/.env')


async def view_dashboard():
    """Display daily analytics dashboard"""

    conn = await asyncpg.connect(os.getenv("DATABASE_URL"))

    print("\n" + "=" * 100)
    print("SACHA ADVISOR - DAILY ANALYTICS DASHBOARD (LAST 30 DAYS)")
    print("=" * 100)

    # Get last 30 days analytics
    rows = await conn.fetch("""
        SELECT 
            TO_CHAR(date, 'YYYY-MM-DD (Dy)') as date_str,
            total_uploads,
            unique_users,
            completed_count,
            abandoned_count,
            wrong_doc_count,
            success_rate
        FROM daily_analytics
        WHERE date >= CURRENT_DATE - INTERVAL '30 days'
        ORDER BY date DESC
        LIMIT 30
    """)

    if not rows:
        print("\nNo data available yet. Run the migration SQL first.")
        await conn.close()
        return

    # Print header
    print(f"\n{'Date':<20} {'Total':<8} {'Users':<8} {'Success':<8} {'Abandoned':<10} {'Wrong Doc':<10} {'Success %':<10}")
    print("-" * 100)

    # Print each day
    total_uploads = 0
    total_users = set()
    total_success = 0
    total_abandoned = 0
    total_wrong = 0

    for row in rows:
        print(f"{row['date_str']:<20} {row['total_uploads']:<8} {row['unique_users']:<8} "
              f"{row['completed_count']:<8} {row['abandoned_count']:<10} "
              f"{row['wrong_doc_count']:<10} {row['success_rate'] or 0:.1f}%")

        total_uploads += row['total_uploads']
        total_success += row['completed_count']
        total_abandoned += row['abandoned_count']
        total_wrong += row['wrong_doc_count']

    # Print summary
    print("-" * 100)
    overall_success_rate = (
        total_success / total_uploads * 100) if total_uploads > 0 else 0
    print(f"{'TOTAL (30 days)':<20} {total_uploads:<8} {'-':<8} {total_success:<8} "
          f"{total_abandoned:<10} {total_wrong:<10} {overall_success_rate:.1f}%")

    print("\n" + "=" * 100)
    print("SUMMARY")
    print("=" * 100)
    print(f"Total Uploads:      {total_uploads}")
    print(f"Successful:         {total_success} ({overall_success_rate:.1f}%)")
    print(
        f"Abandoned by User:  {total_abandoned} ({total_abandoned/total_uploads*100 if total_uploads > 0 else 0:.1f}%)")
    print(
        f"Wrong Documents:    {total_wrong} ({total_wrong/total_uploads*100 if total_uploads > 0 else 0:.1f}%)")

    # Get breakdown of wrong docs
    print("\n" + "-" * 100)
    print("WRONG DOCUMENT BREAKDOWN")
    print("-" * 100)

    wrong_breakdown = await conn.fetch("""
        SELECT 
            request_status,
            COUNT(*) as count
        FROM request_logs_tier1
        WHERE timestamp >= CURRENT_DATE - INTERVAL '30 days'
          AND request_status IN ('invalid_file', 'unreadable_document', 'rejected_by_sachadvisor')
        GROUP BY request_status
        ORDER BY count DESC
    """)

    for row in wrong_breakdown:
        status_label = {
            'invalid_file': 'Invalid File Type/Size',
            'unreadable_document': 'Unreadable Document',
            'rejected_by_sachadvisor': 'Not Insurance Doc'
        }.get(row['request_status'], row['request_status'])

        percentage = (row['count'] / total_wrong *
                      100) if total_wrong > 0 else 0
        print(f"{status_label:<30} {row['count']:<8} ({percentage:.1f}%)")

    await conn.close()
    print("\n")


async def refresh_today():
    """Refresh today's analytics"""
    conn = await asyncpg.connect(os.getenv("DATABASE_URL"))

    print("Refreshing today's analytics...")
    await conn.execute("SELECT refresh_daily_analytics(CURRENT_DATE)")
    print("✅ Today's analytics updated")

    await conn.close()


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "refresh":
        asyncio.run(refresh_today())
    else:
        asyncio.run(view_dashboard())
