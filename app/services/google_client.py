from dataclasses import dataclass
import logging


from google import genai
from google.genai.types import GenerateContentConfig

from app.services.abstract_client import GenerativeAIClient
from core import settings
from app.models.schemas import GenerateResponse


global_settings = settings.Settings()
logger = logging.getLogger("uvicorn.error")

@dataclass
class GoogleAIClient(GenerativeAIClient):
    model: str='gemini-2.5-flash'
    temperature: float=0.5
    #max_tokens: int=2000

    def __post_init__(self):
        try:
            GOOGLE_API_KEY = global_settings.GOOGLE_API_KEY
        except Exception as e:
            logger.exception(f"Client creation failed for provider 'Gemini':{e}",extra={"provider":"Gemini"})
            raise ValueError("GOOGLE_API_KEY is not set in the environment")
        self.client = genai.Client(api_key=GOOGLE_API_KEY)
        self.config = GenerateContentConfig(temperature=self.temperature)

    def generate(self, prompt:str)->GenerateResponse:
        try:
            response = self.client.models.generate_content(model=self.model, contents=prompt, config=self.config)
            logger.info(msg=response, extra={
                "prompt": prompt,
                "provider": self.model    
            })
        except Exception as e:
            logger.exception(f"Client 'Google' did not generate content:{e}")
            raise ValueError("Client 'Google' did not generate content")
        return GenerateResponse(response=response.text)
