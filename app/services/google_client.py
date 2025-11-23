from dataclasses import dataclass
import logging
from typing import Any


from google import genai
from google.genai.types import GenerateContentConfig

from app.services.abstract_client import GenerativeAIClient
from app.core import settings
from app.models.schemas import GenerateResponse


global_settings = settings.Settings()
google_logger = logging.getLogger("GOOGLE")

@dataclass
class GoogleAIClient(GenerativeAIClient):
    model: str='gemini-2.5-flash'
    temperature: float=0.5
    max_output_tokens: int=2000

    def __post_init__(self):
        try:
            GOOGLE_API_KEY = global_settings.GOOGLE_API_KEY
        except Exception as e:
            google_logger.error("GOOGLE_API_KEY is not set in the environment")
            raise ValueError("GOOGLE_API_KEY is not set in the environment")
        self.client = genai.Client(api_key=GOOGLE_API_KEY)
        self.config = GenerateContentConfig()
        google_logger.info(f"GoogleAIClient initialized with model: {self.model}")

    def generate(self, prompt: str, **kwargs: Any) -> GenerateResponse:
        google_logger.info(f"Generating content using Google client for prompt: '{prompt}...'")
        
        config_params = {
            "temperature": self.temperature,
            "max_output_tokens": self.max_output_tokens,
        }
        
        config_params.update(kwargs)
        config = GenerateContentConfig(**config_params)
        
        try:
            response = self.client.models.generate_content(
                model=self.model, 
                contents=prompt, 
                config=config
            )
            
            if not response.text:
                 raise ValueError("Google API returned an empty response.")
            google_logger.info("Google client successfully generated content.")
            return GenerateResponse(response=response.text)
            
        except Exception as e:
            google_logger.error(f"Google client failed to generate content: {e}")
            raise ValueError("Client 'Google' did not generate content") from e