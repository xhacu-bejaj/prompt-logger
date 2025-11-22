import logging
import time
from typing import List

from fastapi import APIRouter, HTTPException, Query


from app.models.schemas import GenerateResponse, Log, PromptRecord, Request
from app.services.client_factory import GenerativeAIClientFactory,Provider
from app.services.logger import get_history, get_logger
from app.services.database import insert_prompt_record, retrieve_prompt_records # Import new DB functions

router = APIRouter(prefix="/api")
route_logger = get_logger("API_ROUTE_GENERATE") 

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
    
    route_logger.info(f"Request received | Provider: {provider_str} | Prompt: '{prompt[:50]}...'")
    
    # --- Step 1: Client Creation ---
    try:
        provider_enum = Provider(provider_str)
        client = GenerativeAIClientFactory().create_client(provider_enum)
        
    except ValueError as e:
        route_logger.warning(f"Client creation failed for provider {provider_str}. Error: {e}", exc_info=True)
        raise HTTPException(status_code=400, detail=f"Invalid provider: {provider_str}. Must be one of 'mock', 'openai', or 'google'.")
    
    # --- Step 2: Content Generation ---
    start_time = time.time() # Start timing
    try:
        response: GenerateResponse = client.generate(request.user_prompt)
        end_time = time.time()
        duration_ms = int((end_time - start_time) * 1000) # Calculate duration in ms
        
        # --- CRITICAL NEW STEP: Insert into prompts_and_responses table ---
        if response.response:
            insert_prompt_record(
                provider=provider_str,
                user_prompt=prompt,
                llm_response=response.response,
                duration_ms=duration_ms
            )
            
        # Log successful completion 
        response_len = len(response.response) if response.response else 0
        route_logger.warning(
            f"Successful generation | Provider: {provider_str} | Response length: {response_len} | Duration: {duration_ms}ms"
        )
        
        return response
    except Exception as e:
        # Log severe error
        route_logger.error(f"LLM generation failed for prompt: '{prompt[:50]}...'. Error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"LLM Generation Error: {e}")

@router.get(
    '/admin/history', 
    response_model=List[Log], 
    tags=["Admin"]
)
def get_log_history(
    lines: int = Query(5, ge=1, le=10, description="Number of log entries to retrieve, max=10")
    ) -> List[Log]: 
    """Retrieves the most recent system log entries from the 'logs' table."""
    
    log_entries_dict = get_history(limit=lines)
    log_entries_pydantic = [Log(**entry) for entry in log_entries_dict]
    
    route_logger.info(f"Retrieved {len(log_entries_pydantic)} log entries for admin history.")
    
    return log_entries_pydantic

# --- NEW ADMIN ENDPOINT ---
@router.get(
    '/admin/prompts',
    response_model=List[PromptRecord],
    tags=["Admin"]
)
def get_prompt_records(
    lines: int = Query(5, ge=1, le=10, description="Number of prompt/response records to retrieve, max=10")
    ) -> List[PromptRecord]:
    """Retrieves the most recent prompt and response records from the dedicated table."""
    
    # 1. Fetch records as a list of dictionaries
    records_dict = retrieve_prompt_records(limit=lines)
    
    # 2. Convert each dictionary into the Pydantic PromptRecord model
    records_pydantic = [PromptRecord(**record) for record in records_dict]
    
    route_logger.info(f"Retrieved {len(records_pydantic)} prompt records.")
    
    return records_pydantic