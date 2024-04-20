import psycopg2
from psycopg2 import OperationalError
import os

connection_string = os.getenv("CONNECTION_STRING")

def create_conn():
    conn = None
    try:
        conn = psycopg2.connect(connection_string)
        print("Connection to database successful")
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    return conn

def check_database_connection(conn):
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT 1')
        print("Database is running")
    except Exception as e:
        print(f"Database query failed: {e}")
    finally:
        cursor.close()
        conn.close()

conn = create_conn()
if conn is not None:
    check_database_connection(conn)