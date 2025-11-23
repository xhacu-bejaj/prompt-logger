import sqlite3
from typing import List, Dict, Any, Optional
from app.core.settings import settings 

DB_PATH = settings.DB_PATH

def create_prompt_record_table(conn: sqlite3.Connection):
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

def create_log_table():
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
    
    create_prompt_record_table(conn)
    
    conn.commit()
    conn.close()

def get_db_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def insert_prompt_record(
    provider: str, 
    user_prompt: str, 
    llm_response: str, 
    duration_ms: Optional[int] = None
):
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
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT timestamp, level, message, logger_name, pathname, funcName, lineno FROM logs ORDER BY timestamp DESC LIMIT ?", 
        (limit,)
    )
    
    entries = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return entries

def retrieve_prompt_records(limit: int) -> List[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, timestamp, provider, user_prompt, llm_response, duration_ms FROM prompts_and_responses ORDER BY timestamp DESC LIMIT ?",
        (limit,)
    )
    entries = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return entries