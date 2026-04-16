import sqlite3
import os

def get_db_connection():
    # Ensure the instance directory exists
    os.makedirs('instance', exist_ok=True)
    db_path = os.path.join('instance', 'database.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    # Enable foreign key constraint support in sqlite
    conn.execute('PRAGMA foreign_keys = ON')
    return conn
