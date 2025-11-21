from typing import List

from pydantic import BaseModel

class ResponseSchema(BaseModel):
    response:str
    logs:List[str]|None=None