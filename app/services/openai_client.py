import os
from dataclasses import dataclass

from openai import OpenAI

from app.services.abstract_client import GenerativeAIClient
from app.models.schemas import GenerateResponse

@dataclass
class OpenAIClient(GenerativeAIClient):
  model: str='gpt-4o-mini'
  temperature: float=0.5
  max_tokens: int=2000

  def __post_init__(self):

      OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
      if not OPENAI_API_KEY:
          raise ValueError("OPENAI_API_KEY is not set in the environment")

      self.client = OpenAI(api_key=OPENAI_API_KEY)

  def generate(self, prompt: str) -> GenerateResponse:
      """Call the chat completion API with basic retries and timing.
      Returns the model's answer as plain text.
      """
      response = self.client.chat.completions.create(
          model=self.model,
          messages=[
              {"role": "user", "content": prompt}
          ],
          temperature=self.temperature,
          max_tokens=self.max_tokens
      )
      if response is None:
          raise ValueError("No response from the API")

      choices = response.choices
      if not choices or len(choices) == 0:
          raise ValueError("Failed to get a valid response from the API")

      first_choice = choices[0]
      message = first_choice.message
      if message.role != "assistant":
          raise ValueError("Invalid message format in the response")

      if not message.content:
          reason = message.refusal
          raise ValueError("No content in the assistant's message: " + str(reason))
      
      return GenerateResponse(response=f"Openai: {message.content}")
