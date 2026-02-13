#!/usr/bin/env python3
"""
Cleanup script for 90-day retention policy (T077).

Deletes records older than 90 days from:
- chat_messages
- feedback_events
- issue_reports

This script should be run daily via a scheduled job (e.g., Vercel cron, GitHub Actions).
"""
import os
import psycopg
from datetime import datetime, timedelta
import sys


def cleanup_old_logs():
    """
    Delete records older than 90 days from logging tables.

    Returns:
        dict: Summary of deleted records per table
    """
    # Get database URL from environment
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("ERROR: DATABASE_URL environment variable not set")
        sys.exit(1)

    # Calculate cutoff date (90 days ago)
    cutoff_date = datetime.utcnow() - timedelta(days=90)

    print(f"Cleanup started at {datetime.utcnow().isoformat()}")
    print(f"Deleting records older than {cutoff_date.isoformat()}")

    deleted_counts = {}

    try:
        with psycopg.connect(database_url) as conn:
            with conn.cursor() as cur:
                # Delete from chat_messages
                cur.execute("""
                    DELETE FROM chat_messages
                    WHERE created_at < %s
                """, (cutoff_date,))
                deleted_counts['chat_messages'] = cur.rowcount

                # Delete from feedback_events
                cur.execute("""
                    DELETE FROM feedback_events
                    WHERE created_at < %s
                """, (cutoff_date,))
                deleted_counts['feedback_events'] = cur.rowcount

                # Delete from issue_reports
                cur.execute("""
                    DELETE FROM issue_reports
                    WHERE created_at < %s
                """, (cutoff_date,))
                deleted_counts['issue_reports'] = cur.rowcount

                # Commit all deletions
                conn.commit()

        # Print summary
        print("\nCleanup completed successfully:")
        print(f"  - chat_messages: {deleted_counts['chat_messages']} records deleted")
        print(f"  - feedback_events: {deleted_counts['feedback_events']} records deleted")
        print(f"  - issue_reports: {deleted_counts['issue_reports']} records deleted")
        print(f"  - Total: {sum(deleted_counts.values())} records deleted")

        return deleted_counts

    except psycopg.Error as e:
        print(f"ERROR: Database error during cleanup: {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: Unexpected error during cleanup: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    cleanup_old_logs()
