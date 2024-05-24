from app import app
import sqlite3 as sl


def get_db_connection():
    conn = sl.connect(app.config.get("SQLITE_DATABASE_PATH"))
    conn.row_factory = sl.Row
    return conn
