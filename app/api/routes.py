import json
from pprint import pprint
from typing import Any, Dict, List

from fastapi import APIRouter, HTTPException, Query
from pymongo import MongoClient

from app.core.settings import settings
from app.models.schemas import GeneralQuery, GenerateResponse, Log, MongoRequest, PromptRecord, Request
from app.models.schemas import QueryResponse
from app.services.client_factory import GenerativeAIClientFactory,Provider
from app.services.google_client import GoogleAIClient
from app.services.logger import get_history, get_logger
from app.services.database.database import insert_prompt_record, retrieve_prompt_records 
from app.services.database.mongoDB_handler import serialize_mongo_doc, MongoDBHandler

router = APIRouter(prefix="/api")
route_logger = get_logger("ROUTE") 

mongo_handler = MongoDBHandler()
uri = mongo_handler.uri
mongo_client = MongoClient(uri)
mongo_db = mongo_handler.db
mongo_collection = mongo_handler.collection

@router.get('/health')
def health():
    route_logger.info("Health check endpoint accessed.")
    return {'status':'ok'}

# @router.post('/generate', response_model=GenerateResponse)
# def generate(
#     request:Request
#     ):
#     provider = request.provider 
#     prompt = request.user_prompt
    
#     route_logger.info(f"Request received | Provider: {provider} | Prompt: '{prompt}'")
    
#     try:
#         provider_enum = Provider(provider)
#         client = GenerativeAIClientFactory().create_client(provider_enum)
#     except ValueError as e:
#         route_logger.warning(f"Client creation failed for provider {provider}. Error: {e}", exc_info=True)
#         raise HTTPException(status_code=400, detail=f"Invalid provider: {provider}. Must be one of 'mock', 'openai', or 'google'.")
    
#     start_time = time.time()
#     try:
#         response: GenerateResponse = client.generate(request.user_prompt)
#         end_time = time.time()
#         duration_ms = int((end_time - start_time) * 1000)
    
#         if response.response:
#             insert_prompt_record(
#                 provider=provider,
#                 user_prompt=prompt,
#                 llm_response=response.response,
#                 duration_ms=duration_ms
#             )
            
#         response_len = len(response.response) if response.response else 0
#         route_logger.warning(
#             f"Successful generation | Provider: {provider} | Response length: {response_len} | Duration: {duration_ms}ms"
#         )
#         return response
#     except Exception as e:
#         route_logger.error(f"LLM generation failed for prompt: '{prompt}...'. Error: {e}", exc_info=True)
#         raise HTTPException(status_code=500, detail=f"LLM Generation Error: {e}")

@router.get('/admin/history', response_model=List[Log], tags=["Admin"])
def get_log_history(
    lines: int = Query(5, ge=1, le=10, description="Number of log entries to retrieve, max=10")
    ) -> List[Log]: 
    
    log_entries_dict = get_history(limit=lines)
    log_entries_pydantic = [Log(**entry) for entry in log_entries_dict]
    
    route_logger.info(f"Retrieved {len(log_entries_pydantic)} log entries for admin history.")
    
    return log_entries_pydantic

@router.get('/admin/prompts', response_model=List[PromptRecord], tags=["Admin"])
def get_prompt_records(
    lines: int = Query(5, ge=1, le=10, description="Number of prompt/response records to retrieve, max=10")
    ) -> List[PromptRecord]:
    
    records_dict = retrieve_prompt_records(limit=lines)
    records_pydantic = [PromptRecord(**record) for record in records_dict]
    
    route_logger.info(f"Retrieved {len(records_pydantic)} prompt records.")
    return records_pydantic


@router.post('/query') 
def raw_query(raw_query:GeneralQuery):
    query_filter = raw_query.filter
    query_projection = raw_query.projection
    
    query_projection["_id"] = 0 # mongodb never returns document _id, which I do not know how to serialize
    
    route_logger.info(f"Query Filter: {query_filter}, Projection: {query_projection}")
    
    mongo_response = mongo_collection.find(query_filter, query_projection)
    results = mongo_response.to_list(length=None)
    serialized_results = serialize_mongo_doc(results)
    
    route_logger.info(f"cleaned_mongo_response: {serialized_results}")
    
    return serialized_results

@router.post('/nl2query')
def nl2query(prompt:str):
    provider='google'
    try:
        provider_enum = Provider(provider)
        client = GoogleAIClient()#GenerativeAIClientFactory().create_client(provider_enum)
    except ValueError as e:
        route_logger.warning(f"Client creation failed for provider {provider}. Error: {e}", exc_info=True)
        raise HTTPException(status_code=400, detail=f"Invalid provider: {provider}. Must be one of 'mock', 'openai', or 'google'.")
    try:
        response: GeneralQuery = client.generate_query(prompt) # type: ignore[reportCallIssue]
    except ValueError as e:
        raise e
    return response

    




    

# @router.post('/nl2query')
# def natural2query(user_request:MongoRequest):
#     provider = user_request.provider 
#     prompt = user_request.user_prompt
    
#     try:
#         provider_enum = Provider(provider)
#         client = GenerativeAIClientFactory().create_client(provider_enum)
#     except ValueError as e:
#         raise HTTPException(status_code=400, detail=f"Invalid provider: {provider}. Must be one of 'mock', 'openai', or 'google'.")
    
#     try:
#         response_query: Dict[str, QueryResponse] = client.generate(prompt)
#         #return response
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"LLM Generation Error: {e}")
    
#     # Now send LLM response to mongodb
#     articles_db = mongo_client.get_database('articles_db')
#     articles_collection = articles_db.get_collection('articles')

#     db_answer = articles_collection.find_one(response_query)
#     #pprint(db_answer)
    
#     mongo_client.close() # for now
#     return db_answer
