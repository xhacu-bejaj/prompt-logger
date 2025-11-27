from dataclasses import dataclass

import logging
from typing import Any, Dict

from app.services.abstract_client import GenerativeAIClient
from app.models.schemas import GenerateResponse, QueryResponse


mock_logger = logging.getLogger("MOCK")

@dataclass
class MockClient(GenerativeAIClient):
    def generate(self, prompt: Dict[str, Any], **kwargs) -> Dict[str, Any]: 
        # mock_logger.info("MOCK client received request.")
        query = prompt
        # mock_logger.info("MOCK client finished generation.")
        return query
    