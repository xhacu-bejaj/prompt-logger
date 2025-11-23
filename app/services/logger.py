import logging
import sqlite3
from logging.handlers import RotatingFileHandler
from typing import Dict, Any, List

from app.core.settings import settings 
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

def setup_logging():
    
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    formatter = logging.Formatter(LOG_FORMAT)
    
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    file_handler = RotatingFileHandler(
        settings.LOG_FILE_PATH,
        maxBytes=1024 * 1024 * 5, # 5 MB per file
        backupCount=2,           # Keep two backup files
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)
    
    # 4. Database Handler (for important events and history)
    db_handler = SQLiteHandler(settings.DB_PATH)
    db_handler.setFormatter(formatter) # The format is needed to populate record.asctime
    root_logger.addHandler(db_handler)

def get_logger(name: str):
    """Retrieves a logger instance for a specific module."""
    return logging.getLogger(name)

def get_history(limit: int) -> List[Dict[str, Any]]:
    """Fetches log history from the database (via logger service for decoupling)."""
    # NOTE: Imports are inside function to avoid circular dependency
    from app.services.database import retrieve_log_entries
    
    try:
        # Retrieve dictionary list from database
        return retrieve_log_entries(limit=limit)
    except Exception as e:
        logging.getLogger("root").error(f"Failed to retrieve log history from DB: {e}", exc_info=True)
        return []