from enum import Enum


from app.services.abstract_client import GenerativeAIClient


class Provider(str,Enum):
    OPENAI = 'openai'
    GOOGLE = 'google'
    MOCK = 'mock'

class GenerativeAIClientFactory:
    @staticmethod
    def create_client(provider: Provider) -> GenerativeAIClient:
        if provider == Provider.OPENAI:
            from app.services.openai_client import OpenAIClient
            return OpenAIClient()
        elif provider == Provider.GOOGLE:
            from app.services.google_client import GoogleAIClient
            return GoogleAIClient()
        elif provider == Provider.MOCK:
            from app.services.mock_client import MockClient
            return MockClient()
        else:
            raise ValueError("Client not supported")