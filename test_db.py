# pyrefly: ignore [missing-import]
import pyodbc

print("Available ODBC Drivers:", pyodbc.drivers())

# Try connecting to SQLEXPRESS
drivers = [d for d in pyodbc.drivers() if "SQL Server" in d]
driver = drivers[0] if drivers else "ODBC Driver 17 for SQL Server"
print("Using driver:", driver)

conn_str = f"DRIVER={{{driver}}};SERVER=.\\SQLEXPRESS;DATABASE=master;Trusted_Connection=yes;TrustServerCertificate=yes;"

try:
    conn = pyodbc.connect(conn_str, autocommit=True)
    print("Successfully connected to SQL Server (SQLEXPRESS)!")
    cursor = conn.cursor()
    
    # Check if lms_db exists
    cursor.execute("SELECT name FROM sys.databases WHERE name = 'lms_db'")
    row = cursor.fetchone()
    if not row:
        cursor.execute("CREATE DATABASE lms_db")
        print("Database 'lms_db' created successfully!")
    else:
        print("Database 'lms_db' already exists.")
    cursor.close()
    conn.close()
except Exception as e:
    print("Error connecting to SQLEXPRESS:", e)
