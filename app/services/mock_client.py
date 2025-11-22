from dataclasses import dataclass

from app.services.abstract_client import GenerativeAIClient
from app.models.schemas import GenerateResponse

# Use Prompt type alias of str instead
@dataclass
class MockClient(GenerativeAIClient):
    def generate(self, prompt: str, **kwargs) -> GenerateResponse:
        self.prompt = prompt 
        return GenerateResponse(response=prompt)