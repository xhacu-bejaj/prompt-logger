import requests

from fastapi import FastAPI

from app.llm import LLM
from config.schemas import ResponseSchema
## Set up sqlite db and save the logs there
# add async
# the log endpoin should have INFO and ERRORS, the others meh


app = FastAPI(title="Student Prompt Logger", version="0.1.0")
l_model = LLM()

@app.get('/health')
def health():
    return {'status':'ok'}

# TODO: POST /generate
# TODO: GET /history

@app.post('/generate') #, response_model=ResponseSchema)
def generate(
    user_prompt:str
    ):
    response = l_model.generate_llm_response(user_prompt)
    #model = l_model.model
    return response
    
# commeeee
@app.get('/history{limit}')
def get_log_history():
    ...



