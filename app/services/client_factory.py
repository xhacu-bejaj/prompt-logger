from enum import Enum
import logging

from app.services.abstract_client import GenerativeAIClient

class Provider(Enum):
    OPENAI = 'openai'
    GOOGLE = 'google'
    MOCK = 'mock'

class GenerativeAIClientFactory:
    
    @staticmethod
    def create_client(provider: Provider) -> GenerativeAIClient:
        if provider == Provider.OPENAI:
            logging.info("Creating OpenAI client")
            from app.services.openai_client import OpenAIClient
            return OpenAIClient()
        elif provider == Provider.GOOGLE:
            logging.info("Creating Google GenAI client")
            from app.services.google_client import GoogleAIClient
            return GoogleAIClient()
        elif provider == Provider.MOCK:
            from app.services.mock_client import MockClient
            logging.info("Creating mock client")
            return MockClient()
        else:
            raise ValueError("Client not supported")