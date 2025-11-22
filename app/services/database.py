import sqlite3
from datetime import datetime

DB_FILE = 'prompt-logger.db'


def init_db():
    conn = sqlite3.connect(DB_FILE)
    

def log_event(provider:str, 
              prompt:str, 
              response:str,
              timestamp:datetime,
              level:str,
              message:str
              ):
    ...
    