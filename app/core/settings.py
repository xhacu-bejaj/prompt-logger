import os

from pydantic_settings import BaseSettings

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception as e:
    raise ValueError(f"Failed to retrieve environment variables:") from e

class Settings:
    DB_PATH = os.getenv('DB_PATH','promptlog.db')
    LOG_LEVEL = os.getenv('LOG_LEVEL','INFO')
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY','')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY','')
    LOG_FILE_PATH = os.getenv('LOG_FILE_PATH', 'service.log')

settings = Settings()
