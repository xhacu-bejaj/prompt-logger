import sqlite3
from typing import List, Dict, Any, Optional
from app.core.settings import settings 

DB_PATH = settings.DB_PATH

# 1. New table creation function
def create_prompt_record_table(conn: sqlite3.Connection):
    """Creates the table to store the actual prompt and response data."""
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS prompts_and_responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            provider TEXT NOT NULL,
            user_prompt TEXT NOT NULL,
            llm_response TEXT NOT NULL,
            duration_ms INTEGER 
        )
    """)
    conn.commit()

# Existing function modified to call the new table creation
def create_log_table():
    """Ensures the log and prompt record tables are created."""
    conn = get_db_connection()
    
    # 1. Create the system log table (existing logic)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            level TEXT NOT NULL,
            message TEXT NOT NULL,
            logger_name TEXT,
            pathname TEXT,
            funcName TEXT,
            lineno INTEGER
        )
    """)
    
    # 2. Create the new prompt record table
    create_prompt_record_table(conn)
    
    conn.commit()
    conn.close()

def get_db_connection() -> sqlite3.Connection:
    """Creates and returns a database connection object."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # This allows accessing columns by name
    return conn

# 2. New insertion function
def insert_prompt_record(
    provider: str, 
    user_prompt: str, 
    llm_response: str, 
    duration_ms: Optional[int] = None
):
    """Inserts a new prompt and response record into the database."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO prompts_and_responses (
                timestamp, provider, user_prompt, llm_response, duration_ms
            ) 
            VALUES (
                datetime('now'), ?, ?, ?, ?
            )
            """,
            (provider, user_prompt, llm_response, duration_ms)
        )
        conn.commit()
    except Exception as e:
        print(f"Error inserting prompt record: {e}")
        conn.rollback()
    finally:
        conn.close()

def retrieve_log_entries(limit: int) -> List[Dict[str, Any]]:
    """Retrieves the most recent log entries from the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # We still retrieve from the 'logs' table
    cursor.execute(
        "SELECT timestamp, level, message, logger_name, pathname, funcName, lineno FROM logs ORDER BY timestamp DESC LIMIT ?", 
        (limit,)
    )
    
    # Convert Row objects to dictionaries
    entries = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return entries

# 3. New retrieval function for prompt history (for future admin endpoint)
def retrieve_prompt_records(limit: int) -> List[Dict[str, Any]]:
    """Retrieves the most recent prompt and response records."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, timestamp, provider, user_prompt, llm_response, duration_ms FROM prompts_and_responses ORDER BY timestamp DESC LIMIT ?",
        (limit,)
    )
    entries = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return entries