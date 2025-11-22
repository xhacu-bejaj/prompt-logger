from fastapi import APIRouter, HTTPException
from app.services.abstract_client import GenerativeAIClient
from app.models.schemas import GenerateResponse, Request

from app.services.client_factory import GenerativeAIClientFactory
router = APIRouter(prefix="/api")

@router.get('/health')
def health():
    return {'status':'ok'}

@router.post('/generate', response_model=GenerateResponse)
def generate(
    request:Request
    ):
    try:
        client = GenerativeAIClientFactory().create_client(request.provider)
    except ValueError as e:
        # invalid provider, save later in logging
        raise HTTPException(status_code=400, detail=str(e))
    try:
        response = client.generate(request.user_prompt)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)

@router.get('/history{limit}')
def get_log_history():
    ...