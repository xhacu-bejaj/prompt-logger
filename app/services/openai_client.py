import os
from dataclasses import dataclass
import logging

from openai import OpenAI

from app.services.abstract_client import GenerativeAIClient
from app.models.schemas import GenerateResponse
from core import settings

global_settings = settings.Settings()
logger = logging.getLogger(__name__)

@dataclass
class OpenAIClient(GenerativeAIClient):
  model: str='gpt-4o-mini'
  temperature: float=0.5
  max_tokens: int=2000

  def __post_init__(self):
      try:
        OPENAI_API_KEY = global_settings.OPENAI_API_KEY
      except Exception as e:
            logger.exception(f"Client creation failed for provider 'Openai':{e}")
            raise ValueError("OPENAI_API_KEY is not set in the environment")
      self.client = OpenAI(api_key=OPENAI_API_KEY)
      logger.info(f"API KEY FOUND: Openai client successfully created")



  def generate(self, prompt: str) -> GenerateResponse:
      """Call the chat completion API with basic retries and timing.
      Returns the model's answer as plain text.
      """
      try:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=self.temperature,
            max_tokens=self.max_tokens
        )
      except Exception as e:
          logger.exception(f"Client 'Openai' failed to generate content':{e}")
          raise ValueError("Client 'Openai' failed to generate content") from e
        
      try:
        choices = response.choices
      except Exception as e:
            logger.exception(f"Response from Openai failed':{e}")
            raise ValueError("Failed to get a valid response from the API") from e

      first_choice = choices[0]
      message = first_choice.message

      try:
          reason = message.refusal
      except Exception as e:
          logger.exception(f"Response from Openai failed because':{e}")
          raise ValueError("No content in the assistant's message: " + str(reason)) from e # type: ignore
      
      return GenerateResponse(response=f"Openai: {message.content}")
