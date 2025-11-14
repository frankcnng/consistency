import sqlite3
import re
from openpyxl import load_workbook


def create_db(db_path):
    """Create the AEF consistency database at 'db_path'."""

    conn	= sqlite3.connect(db_path)
    cursor	= conn.cursor()

    # Create tables
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Submissions (
        id INTEGER PRIMARY KEY,
        project_id TEXT,
        project_title TEXT,
        host_country TEXT,
        implementing_entity TEXT
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS AEF_Activities (
        id INTEGER PRIMARY KEY,
        project_id TEXT,
        activity_id TEXT,
        activity_type TEXT,
        start_date TEXT,
        end_date TEXT,
        emission_reduction REAL
    );
    """)

    conn.commit()
    conn.close()