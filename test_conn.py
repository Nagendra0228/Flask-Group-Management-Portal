import pyodbc

try:
    conn = pyodbc.connect(
        r'DRIVER={ODBC Driver 17 for SQL Server};'
        r'SERVER=DESKTOP-NR0NEH1\SQLEXPRESS;'
        r'DATABASE=master;'
        r'Trusted_Connection=yes;'
    )
    print("✅ Connection successful")
    conn.close()
except Exception as e:
    print("❌ Connection failed:", e)
