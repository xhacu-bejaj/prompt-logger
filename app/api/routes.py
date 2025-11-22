import logging

from fastapi import APIRouter, HTTPException
from app.services.abstract_client import GenerativeAIClient
from app.models.schemas import GenerateResponse, Request

from app.services.client_factory import GenerativeAIClientFactory

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api")

@router.get('/health')
def health():
    logger.info("Health check endpoint accessed.")
    return {'status':'ok'}

@router.post('/generate', response_model=GenerateResponse)
def generate(
    request:Request
    ):
    logger.info(f"Received generate request for provider: {request.provider} and prompt: '{request.user_prompt}...'")
    try:
        client = GenerativeAIClientFactory().create_client(request.provider)
    except ValueError as e:
        logger.warning(f"Client creation failed for provider '{request.provider}': {e}")
        raise HTTPException(status_code=400, detail=str(e))
    try:
        response = client.generate(request.user_prompt)
        logger.info(f"Successfully generated response using {request.provider}.")
        return response
    except Exception as e:
        logger.exception(f"FATAL error during generation for provider {request.provider}: {e}")
        raise HTTPException(status_code=500, detail=e)

@router.get('/history{limit}')
def get_log_history():
    ...