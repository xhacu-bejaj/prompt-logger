
from dataclasses import dataclass

from google import genai
from google.genai.types import GenerateContentConfig

from config import settings



global_settings = settings.Settings()


@dataclass
class LLM:
    model: str='gemini-2.5-flash'
    temperature: float=0.5
    #max_tokens: int=2000

    def __post_init__(self):
        LLM_API_KEY = global_settings.LLM_API_KEY
        if not LLM_API_KEY:
            raise ValueError("LLM_API_KEY is not set")
        self.client = genai.Client(api_key=LLM_API_KEY)
        self.config = GenerateContentConfig(temperature=self.temperature)

    def generate_llm_response(self, prompt):
        response = self.client.models.generate_content(model=self.model, contents=prompt, config=self.config)
        if response is None or response.text is None:
            raise ValueError("LLM did not respond, ask more kindly")
        return f'Gemini response: {response.text}'
