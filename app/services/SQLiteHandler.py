import logging
from datetime import datetime



class SQLiteHandler(logging.Handler):

    def __init__(self):
        super().__init__()
        from app.services.database import get_db_connection
        self._get_db_connection = get_db_connection

    def emit(self, record):
        conn = None
        try:
            conn = self._get_db_connection() 
            cursor = conn.cursor()
            timestamp = datetime.fromtimestamp(record.created).isoformat()
            
            insert_sql = """
                INSERT INTO logs (timestamp, level, logger_name, message, pathname, funcName, lineno)
                VALUES (?, ?, ?, ?, ?, ?, ?);
            """
            
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