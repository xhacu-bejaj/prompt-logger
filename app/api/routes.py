import time
from typing import List

from fastapi import APIRouter, HTTPException, Query

from app.models.schemas import GenerateResponse, Log, PromptRecord, Request
from app.services.client_factory import GenerativeAIClientFactory,Provider
from app.services.logger import get_history, get_logger
from app.services.database import insert_prompt_record, retrieve_prompt_records 

router = APIRouter(prefix="/api")
route_logger = get_logger("ROUTE") 

@router.get('/health')
def health():
    route_logger.info("Health check endpoint accessed.")
    return {'status':'ok'}

@router.post('/generate', response_model=GenerateResponse)
def generate(
    request:Request
    ):
    provider_str = request.provider 
    prompt = request.user_prompt
    
    route_logger.info(f"Request received | Provider: {provider_str} | Prompt: '{prompt}'")
    
    try:
        provider_enum = Provider(provider_str)
        client = GenerativeAIClientFactory().create_client(provider_enum)
    except ValueError as e:
        route_logger.warning(f"Client creation failed for provider {provider_str}. Error: {e}", exc_info=True)
        raise HTTPException(status_code=400, detail=f"Invalid provider: {provider_str}. Must be one of 'mock', 'openai', or 'google'.")
    
    start_time = time.time()
    try:
        response: GenerateResponse = client.generate(request.user_prompt)
        end_time = time.time()
        duration_ms = int((end_time - start_time) * 1000)
    
        if response.response:
            insert_prompt_record(
                provider=provider_str,
                user_prompt=prompt,
                llm_response=response.response,
                duration_ms=duration_ms
            )
            
        response_len = len(response.response) if response.response else 0
        route_logger.warning(
            f"Successful generation | Provider: {provider_str} | Response length: {response_len} | Duration: {duration_ms}ms"
        )
        
        return response
    except Exception as e:
        # Log severe error
        route_logger.error(f"LLM generation failed for prompt: '{prompt}...'. Error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"LLM Generation Error: {e}")

@router.get(
    '/admin/history', 
    response_model=List[Log], 
    tags=["Admin"]
    )

def get_log_history(
    lines: int = Query(5, ge=1, le=10, description="Number of log entries to retrieve, max=10")
    ) -> List[Log]: 
    
    log_entries_dict = get_history(limit=lines)
    log_entries_pydantic = [Log(**entry) for entry in log_entries_dict]
    
    route_logger.info(f"Retrieved {len(log_entries_pydantic)} log entries for admin history.")
    
    return log_entries_pydantic

@router.get(
    '/admin/prompts',
    response_model=List[PromptRecord],
    tags=["Admin"]
)
def get_prompt_records(
    lines: int = Query(5, ge=1, le=10, description="Number of prompt/response records to retrieve, max=10")
    ) -> List[PromptRecord]:
    
    records_dict = retrieve_prompt_records(limit=lines)
    records_pydantic = [PromptRecord(**record) for record in records_dict]
    
    route_logger.info(f"Retrieved {len(records_pydantic)} prompt records.")
    
    return records_pydantic