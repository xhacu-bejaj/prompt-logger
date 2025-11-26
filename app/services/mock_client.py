from dataclasses import dataclass
import logging
from typing import Dict

from app.services.abstract_client import GenerativeAIClient
from app.models.schemas import GenerateResponse, QueryResponse


mock_logger = logging.getLogger("MOCK")

@dataclass
class MockClient(GenerativeAIClient):
    
    def generate(self, prompt: QueryResponse, **kwargs) -> QueryResponse: 
        mock_logger.info("MOCK client received request.")
        
        # response = GenerateResponse(
        #     response=prompt
        # )
        response = prompt
        mock_logger.info("MOCK client finished generation.")
        return response