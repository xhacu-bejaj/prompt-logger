from abc import ABC, abstractmethod
from typing import Dict
from app.models.schemas import GenerateResponse, QueryResponse


class GenerativeAIClient(ABC):
  @abstractmethod
  def generate(self, prompt: str, **kwargs) -> Dict[str, QueryResponse]:
      ...