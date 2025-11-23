import logging
from fastapi import FastAPI
import uvicorn

from app.services.logger import setup_logging
from app.services.database import database 
from app.api.routes import router
from app.services.database.database import create_log_table 


setup_logging() 
create_log_table() 

logger = logging.getLogger("MAIN")
logger.info("Application starting up...")

app = FastAPI(
    title="Prompt Logger & Generative AI API",
    description="A microservice for managing LLM interactions and logging history to SQLite.",
    version="1.0.0"
)

app.include_router(router)

if __name__ == "__main__":
    logger.info("Starting Uvicorn server...")
    uvicorn.run("main:app", host="127.0.0.1", port=8080, log_level="info", reload=True) 