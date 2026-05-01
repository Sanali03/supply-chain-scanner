import sqlite3
import os
import sys

BASE_DIR = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.getcwd()

DATABASE_NAME = os.path.join(BASE_DIR, "scanner.db")

def get_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn