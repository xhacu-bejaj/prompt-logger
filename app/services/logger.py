from datetime import datetime
import logging

from typing import List


from app.models.schemas import Log, LogHistory


logger = logging.getLogger("uvicorn.error")

def get_history(n: int) -> List[Log]:
    ...
    
 