import sqlite3

print("Checking SQLite database for existing data...")

sqlite_conn = sqlite3.connect('db.sqlite3')
sqlite_cursor = sqlite_conn.cursor()

# Check tables
sqlite_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = [r[0] for r in sqlite_cursor.fetchall()]

for table in tables:
    if table.startswith('sqlite_') or table.startswith('django_session'):
        continue
    sqlite_cursor.execute(f"SELECT COUNT(*) FROM \"{table}\"")
    count = sqlite_cursor.fetchone()[0]
    if count > 0:
        print(f"Table '{table}' has {count} records in SQLite.")

sqlite_conn.close()
