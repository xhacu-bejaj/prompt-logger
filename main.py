import logging
from fastapi import FastAPI
import uvicorn

# Import the necessary setup functions
from app.services.logger import setup_logging
from app.services import database # Importing this module ensures the log table is created
from app.api.routes import router
from app.services.database import create_log_table # Ensure this is imported


# 1. Database and Logging Setup (MUST be executed before the app starts)
# Note: By simply importing the database module, the create_log_table() 
# function runs.
#database 
setup_logging() # Configures the custom SQLite handler and console handler








# 1. Database Setup - CRITICAL: This MUST run before anything else starts using the DB.
create_log_table() 

# 2. Logging Setup
setup_logging() 
logger = logging.getLogger("MAIN")
logger.info("Application starting up...")

# 3. FastAPI App Setup
app = FastAPI(
    title="Prompt Logger & Generative AI API",
    description="A microservice for managing LLM interactions and logging history to SQLite.",
    version="1.0.0"
)

app.include_router(router)



if __name__ == "__main__":
    logger.info("Starting Uvicorn server...")
    uvicorn.run("main:app", host="127.0.0.1", port=8080, log_level="info", reload=True)