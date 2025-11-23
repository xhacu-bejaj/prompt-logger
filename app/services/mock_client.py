from dataclasses import dataclass
import logging

from app.services.abstract_client import GenerativeAIClient
from app.models.schemas import GenerateResponse


mock_logger = logging.getLogger("MOCK")

@dataclass
class MockClient(GenerativeAIClient):
    
    def generate(self, prompt: str, **kwargs) -> GenerateResponse: 
        mock_logger.info("MOCK client received request.")
        
        response = GenerateResponse(
            response=f"Mock response for prompt: '{prompt}...'. Provider: MOCK"
        )
        mock_logger.info("MOCK client finished generation.")
        return response