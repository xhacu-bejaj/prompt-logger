from dataclasses import dataclass
import logging

from app.services.abstract_client import GenerativeAIClient
from app.models.schemas import GenerateResponse

# Use a specific logger name for this module
mock_logger = logging.getLogger("CLIENT.MOCK")

@dataclass
class MockClient(GenerativeAIClient):
    
    def generate(self, prompt: str, **kwargs) -> GenerateResponse: # <--- Matches abstract
        mock_logger.info("MOCK client received request. Simulating latency.")
        
        # Return the response object that matches the expected schema
        response = GenerateResponse(
            response=f"Mock response for prompt: '{prompt}...'. Provider: MOCK"
        )
        mock_logger.info("MOCK client finished generation.")
        return response