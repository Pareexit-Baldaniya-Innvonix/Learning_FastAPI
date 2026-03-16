import sqlite3
from src.config.constants import DB_NAME


# create database
def get_db_connection():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn
