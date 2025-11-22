import logging

from fastapi import APIRouter, HTTPException, Query


from app.models.schemas import GenerateResponse, Log, LogHistory, Request
from app.services.client_factory import GenerativeAIClientFactory
from app.services.logger import get_history

err_logger = logging.getLogger("uvicorn.error")
acc_logger = logging.getLogger("uvicorn.access")
router = APIRouter(prefix="/api")

@router.get('/health')
def health():
    acc_logger.info("Health check endpoint accessed.")
    return {'status':'ok'}

@router.post('/generate', response_model=GenerateResponse)
def generate(
    request:Request
    ):
    provider = request.provider
    prompt = request.user_prompt

    acc_logger.info(f"Received generate request: {provider} {prompt}")
    
    try:
        client = GenerativeAIClientFactory().create_client(request.provider)
    except ValueError as e:
        err_logger.exception(f"Client creation failed. {provider} DETAIL:{e}")
        raise HTTPException(status_code=400, detail=str(e))
    
    try:
        response = client.generate(request.user_prompt)
        acc_logger.info(
            f"Successfully generated response. {provider} {prompt} {response}"
        )
        return GenerateResponse(response=response)
    except Exception as e:
        err_logger.exception(
            f"FATAL error during generation. {provider} {prompt} DETAIL:{e}"
        )
        raise HTTPException(status_code=500, detail=str(e))

@router.get('/admin/history', response_model=LogHistory, tags=["Admin"])
def get_log_history(
    lines: int = Query(5, ge=1, le=10, description="Number of log entries to retrieve, max=10")
    ):
    try: 
        history = get_history(lines)
        return LogHistory(history=history)
    except Exception:
        err_logger.exception("Failed to retrieve log history.") 
        raise HTTPException(status_code=500, detail="Internal server error while accessing history.")