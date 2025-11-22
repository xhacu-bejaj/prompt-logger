from datetime import datetime
from typing import List

from pydantic import BaseModel
#%(provider)s %(prompt)s %(response)s
from app.services.client_factory import Provider

class GenerateResponse(BaseModel):
    response:str|None
    #logs:List[str]#|None=None

class Request(BaseModel):
    user_prompt:str
    provider:Provider = Provider.MOCK

class Log(BaseModel):
    provider:str
    prompt:str
    response:str
    timestamp:datetime
    level:str
    message:str

class LogHistory(BaseModel):
    history:List[Log]
    