import json
from pathlib import Path

from fastapi import FastAPI
import uvicorn

from app.api.routes import router
## Set up sqlite db and save the logs there
# add async
# the log endpoint should have INFO and ERRORS, the others meh
# history.log


LOG_CONFIG_PATH = Path(__file__).parent / "log_config.json"
try:
    with open(LOG_CONFIG_PATH, "r") as f:
        LOG_CONFIG = json.load(f)
except FileNotFoundError:
    print(f"Error: Logging config file not found at {LOG_CONFIG_PATH}. Using default Uvicorn logging.")
    # Fallback to Uvicorn's internal configuration if file is missing
    from uvicorn.config import LOGGING_CONFIG as LOG_CONFIG

app = FastAPI(
    title="Student Prompt Logger",
    version="0.1.0",
)

app.include_router(router)

def main():
   
   print("Application is starting...")
   uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8083,
        reload=True,
        log_config=LOG_CONFIG  
    )


if __name__ == "__main__":
    main()

