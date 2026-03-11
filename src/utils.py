import sqlite3


# create database
def get_db_connection():
    conn = sqlite3.connect("rate_limiter.db")
    conn.row_factory = sqlite3.Row
    return conn
