from abc import ABC, abstractmethod
from app.models.schemas import GenerateResponse, QueryResponse


class GenerativeAIClient(ABC):
  @abstractmethod
  def generate(self, prompt: str, **kwargs) -> QueryResponse:
      ...