# ----- library import -----
import sqlite3

# ----- local import -----
from src.config.constants import DB_NAME


# create database
def get_db_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn
