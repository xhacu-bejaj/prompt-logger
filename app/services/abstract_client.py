from abc import ABC, abstractmethod
from typing import Any, Dict
from app.models.schemas import GenerateResponse, QueryResponse


class GenerativeAIClient(ABC):
  @abstractmethod
  def generate(self, prompt: Dict[str, Any], **kwargs) -> Dict[str, Any]:
      ...