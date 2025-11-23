import logging
from datetime import datetime
import sqlite3

from app.services.database import get_db_connection


class SQLiteHandler(logging.Handler):
    def __init__(self, db_path: str):
        super().__init__()
        self.db_path = db_path

    def emit(self, record: logging.LogRecord):
        if record.levelno < logging.WARNING:
            return

        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
    
            cursor.execute(
                """
                INSERT INTO logs (
                    timestamp, level, message, logger_name, 
                    pathname, funcName, lineno
                ) 
                VALUES (
                    ?, ?, ?, ?, ?, ?, ?
                )
                """,
                (
                    record.asctime, 
                    record.levelname, 
                    record.getMessage(),
                    record.name,
                    record.pathname,
                    record.funcName,
                    record.lineno
                )
            )
            conn.commit()
        except sqlite3.OperationalError as e:
            print(f"LOGGING FAILURE: Error saving log to database: {e}") 
        finally:
            if conn:
                conn.close()