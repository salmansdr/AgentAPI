# db.py
import pyodbc
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    conn_str = (
        f"Driver={{{os.getenv('DB_DRIVER')}}};"
        f"Server={os.getenv('DB_SERVER')};"
        f"Database={os.getenv('DB_NAME')};"
    )
    if os.getenv("DB_TRUSTED_CONNECTION", "no").lower() == "yes":
        conn_str += "Trusted_Connection=yes;"
    else:
        conn_str += (
            f"UID={os.getenv('DB_USER')};"
            f"PWD={os.getenv('DB_PASSWORD')};"
        )
    return pyodbc.connect(conn_str)
