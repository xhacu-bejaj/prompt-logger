import logging
import sqlite3
from logging.handlers import RotatingFileHandler
from typing import Dict, Any, List

from app.core.settings import settings 
from app.services.SQLiteHandler import SQLiteHandler
from app.services.database import get_db_connection


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
        backupCount=2,        
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)
    
    db_handler = SQLiteHandler(settings.DB_PATH)
    db_handler.setFormatter(formatter)
    root_logger.addHandler(db_handler)

def get_logger(name: str):
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