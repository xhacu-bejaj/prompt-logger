import logging
import sqlite3
from datetime import datetime
import threading


class SQLiteHandler(logging.Handler):

    def __init__(self):
        super().__init__()
        # Import the database connection function here to avoid circular dependencies 
        # during startup, as it might use settings that rely on logger being set up.
        from app.services.database import get_db_connection
        self._get_db_connection = get_db_connection

    def emit(self, record):
        """Called by the logging system to process a record."""
        conn = None
        try:
            conn = self._get_db_connection() 
            cursor = conn.cursor()

            # Format timestamp to ISO 8601 string
            timestamp = datetime.fromtimestamp(record.created).isoformat()
            
            insert_sql = """
                INSERT INTO logs (timestamp, level, logger_name, message, pathname, funcName, lineno)
                VALUES (?, ?, ?, ?, ?, ?, ?);
            """
            
            # Use self.format(record) to capture the final message after formatter processing
            cursor.execute(insert_sql, (
                timestamp,
                record.levelname,
                record.name,
                self.format(record),
                record.pathname,
                record.funcName,
                record.lineno
            ))
            conn.commit()
            
        except Exception as e:
            print(f"LOGGING FAILURE: Error saving log to database: {e}") 
        finally:
            if conn:
                conn.close()