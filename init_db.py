import sqlite3

# Direct database initialization
conn = sqlite3.connect('backend/sacha_advisor.db')
cursor = conn.cursor()

# Create the table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS request_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        file_type TEXT NOT NULL,
        page_count INTEGER,
        text_length INTEGER,
        explanation TEXT NOT NULL
    )
""")

conn.commit()
print("Database table created/verified successfully")

# Check what's in there
cursor.execute("SELECT COUNT(*) FROM request_logs")
count = cursor.fetchone()[0]
print(f"Total records in request_logs: {count}")

if count > 0:
    cursor.execute(
        "SELECT id, file_type, page_count, text_length FROM request_logs ORDER BY id DESC LIMIT 3")
    print("\nLatest records:")
    for row in cursor.fetchall():
        print(
            f"  ID={row[0]}, Type={row[1]}, Pages={row[2]}, TextLen={row[3]}")

conn.close()
