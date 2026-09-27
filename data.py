import psycopg2
from psycopg2.extras import RealDictCursor

DB_CONFIG = {
    "dbname": "library_db",
    "user": "postgres",
    "password": "1234",
    "host": "localhost",
    "port": "5432"
}

def get_db_connection():
    """Establishes and returns a connection to the PostgreSQL database."""
    try:
        conn = psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor)
        return conn
    except Exception as e:
        print(f"[DB ERROR] Could not connect to PostgreSQL: {e}")
        return None

def check_db_connection():
    """Tests the database connection and returns True if successful, False otherwise."""
    conn = get_db_connection()
    if conn:
        print("[DB SUCCESS] Successfully connected to PostgreSQL database!")
        conn.close()
        return True
    return False