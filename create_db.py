import sqlite3

# Specify the path for the database
db_path = r"C:\Users\DELL\Desktop\tourism.db"  # Or any other location

try:
    # Try to create a connection and create the database file
    conn = sqlite3.connect(db_path)
    print("Database created successfully.")
    conn.close()
except sqlite3.OperationalError as e:
    print(f"Error: {e}")
