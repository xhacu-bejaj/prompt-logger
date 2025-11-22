import os
from dataclasses import dataclass
import logging

from openai import OpenAI

from app.services.abstract_client import GenerativeAIClient
from app.models.schemas import GenerateResponse
from core import settings

global_settings = settings.Settings()
openai_logger = logging.getLogger("CLIENT.OPENAI")

@dataclass
class OpenAIClient(GenerativeAIClient):
  model: str='gpt-4o-mini'
  temperature: float=0.5
  max_tokens: int=2000

  def __post_init__(self):
      try:
        OPENAI_API_KEY = global_settings.OPENAI_API_KEY
      except Exception as e:
            openai_logger.error("OPENAI_API_KEY is not set in the environment")
            raise ValueError("OPENAI_API_KEY is not set in the environment")
      self.client = OpenAI(api_key=OPENAI_API_KEY)
      openai_logger.info(f"OpenAIClient initialized with model: {self.model}")



  def generate(self, prompt: str, **kwargs) -> GenerateResponse: # <--- Added **kwargs
      """Call the chat completion API with basic retries and timing."""
      openai_logger.info(f"Generating content using OpenAI client for prompt: '{prompt[:50]}...'")
      
      # Use kwargs to override default settings (e.g., model, temp)
      call_params = {
          "model": self.model,
          "temperature": self.temperature,
          "max_tokens": self.max_tokens,
          **kwargs # Merge any additional parameters passed in **kwargs
      }

      try:
          response = self.client.chat.completions.create(
              messages=[
                  {"role": "user", "content": prompt}
              ],
              **call_params
          )
      except Exception as e:
          openai_logger.error(f"OpenAI client failed to generate content: {e}")
          raise ValueError("Client 'Openai' failed to generate content") from e
          
      try:
          # Check for a valid response and extract content
          message= response.choices[0].message
          content = message.content
          
          if not content:
              # Content is None, often due to safety filter or max tokens
              openai_logger.warning("OpenAI returned a message with no content (may be filtered).")
              return GenerateResponse(response=None) 
          
          openai_logger.info("OpenAI client successfully generated content.")
          return GenerateResponse(response=content)
          
      except IndexError:
            openai_logger.error("OpenAI response contained no choices/messages.")
            raise ValueError("Failed to get a valid response from the API: no choices.")
      except Exception as e:
          openai_logger.error(f"Error processing OpenAI response: {e}")
          raise ValueError("Failed to process API response structure.") from e
