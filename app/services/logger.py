import logging
import sys
from app.services.database import retrieve_log_entries # Import the new retrieval function
from app.services.SQLiteHandler import SQLiteHandler 
from app.core.settings import settings

# --- Logger Setup ---

def setup_logging():
    """Configures the root logger with the SQLite Handler and console output."""
    
    logger = logging.getLogger()
    logger.setLevel(settings.LOG_LEVEL) 
    
    
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

   
    db_handler = SQLiteHandler()
   
    db_handler.setLevel(logging.WARNING) 
    db_handler.setFormatter(formatter)
    
   
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(settings.LOG_LEVEL)
    
   
    if not logger.handlers: 
        logger.addHandler(db_handler)
        logger.addHandler(console_handler)

def get_logger(name: str):
    """Returns a specific logger instance."""
    return logging.getLogger(name)

# --- History Retrieval Utility ---

def get_history(limit: int):
    """
    Fetches log entries from the database. This function acts as a wrapper 
    around the database retrieval logic.
    """
    try:
        return retrieve_log_entries(limit=limit)
    except Exception as e:
        # Use the root logger to log database retrieval failures
        logging.getLogger().error(f"Failed to retrieve log history from DB: {e}")
        return []