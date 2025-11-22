from abc import ABC, abstractmethod
from app.models.schemas import GenerateResponse
class GenerativeAIClient(ABC):

  @abstractmethod
  def generate(self, prompt: str, **kwargs) -> GenerateResponse:
      ...