import os
import logging

from pydantic_settings import BaseSettings, SettingsConfigDict

logger = logging.getLogger("uvicorn.error")

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception as e:
    logger.exception(f"load_dotenv failed to retrieve environment variables: {e}")
    raise ValueError(f"Failed to retrieve environment variables:") from e

class Settings:
    DB_PATH = os.getenv('DB_PATH','promptlog.db')
    LOG_LEVEL = os.getenv('LOG_LEVEL','INFO')
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY','')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    #model_config = SettingsConfigDict()
settings = Settings()
