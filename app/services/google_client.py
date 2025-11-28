from dataclasses import dataclass
import logging
from typing import Any
import json

from google import genai
from google.genai.types import GenerateContentConfig

from app.services.abstract_client import GenerativeAIClient
from app.core import settings
from app.models.schemas import GeneralQuery, GenerateResponse


global_settings = settings.Settings()
google_logger = logging.getLogger("GOOGLE")

@dataclass
class GoogleAIClient(GenerativeAIClient):
    model: str='gemini-2.5-flash'
    temperature: float=0.5
    max_output_tokens: int=2000
    SYSTEM_GUARDRAIL: str = """ 
    Your sole purpose is to act as a **secure, read-only MongoDB Query Generator**.
    You MUST translate the user's natural language request into a valid MongoDB query structure using the provided **GeneralQuery** schema.

    ### STRICT SECURITY AND OUTPUT CONSTRAINTS
    1.  **ABSOLUTELY NO DATA MODIFICATION IS PERMITTED.** You are **STRICTLY FORBIDDEN** from generating any query that could lead to data changes, deletions, or structural modifications (e.g., update, delete, drop, createIndex).
    2.  **OUTPUT REQUIREMENT**: You MUST return a **raw JSON object** that strictly adheres to the schema of the GeneralQuery object. **Crucially, the values for the 'filter' and 'projection' keys must be valid, escaped JSON strings.** You are FORBIDDEN from generating any conversational or explanatory text.
    3.  **Forbidden Request Handling:** If the user requests a forbidden operation (e.g., "delete this record") or asks a general question (e.g., "What is the capital of France?"), you must populate the `filter` with an obvious marker indicating the failure, such as:
        `{"_REFUSED_OPERATION": "Data modification forbidden by system guardrail."}`

    Few-Shot Demonstration Examples (Raw JSON Output)
    Assume the collection structure includes fields like id, title, keywords, authors, and teams.

    | User Request | Expected Raw JSON Output | Rationale |
    | :--- | :--- | :--- |
    | **"Find the title and date for the paper with the ID 5096000."** | {"filter": "{\"id\": \"5096000\"}", "projection": "{\"title\": 1, \"date\": 1, \"_id\": 0}"} | Valid Read Operation. |
    | **"List papers by 'Mathieu Lagrange' about 'acoustic sensor networks'."** | {"filter": "{\"authors\": \"Mathieu Lagrange\", \"keywords\": \"acoustic sensor networks\"}", "projection": "{}"} | Valid Read Operation. |
    | **"Please **delete** the record where the team is 'AAU'."** | {"filter": "{\"_REFUSED_OPERATION\": \"Data modification forbidden by system guardrail.\"}", "projection": "{}"} | FORBIDDEN OPERATION. Refusal marker must be used. |
    | **"What is the average number of authors per paper?"** | {"filter": "{\"_NON_QUERY_OR_COMPLEX_REQUEST\": \"Request requires complex aggregation or is not a simple retrieval query.\"}", "projection": "{}"} | Non-Retrieval Request. Returns a refusal marker. |
"""



    def __post_init__(self):
        try:
            GOOGLE_API_KEY = global_settings.GOOGLE_API_KEY
        except Exception as e:
            google_logger.error("GOOGLE_API_KEY is not set in the environment")
            raise ValueError("GOOGLE_API_KEY is not set in the environment")
        
        if not GOOGLE_API_KEY:
            google_logger.error("GOOGLE_API_KEY is missing or empty.")
            raise ValueError("GOOGLE_API_KEY is missing or empty.")
        
        self.client = genai.Client(api_key=GOOGLE_API_KEY)
        self.config = GenerateContentConfig()
        google_logger.info(f"GoogleAIClient initialized with model: {self.model}")

    # TODO: Now that all works you need to make it more general, also in the endpoint
    def generate_query(self, prompt: str, **kwargs: Any) -> GeneralQuery:
        google_logger.info(f"Generating content using Google client for prompt: '{prompt}...'")
        
        config_params = {
            "temperature": self.temperature,
            "max_output_tokens": self.max_output_tokens,
            "system_instruction": self.SYSTEM_GUARDRAIL, 
            "response_mime_type": "application/json", 
            "response_schema": GeneralQuery,
             
        }
        
        config_params.update(kwargs)
        config = GenerateContentConfig(**config_params)
        
        try:
            response = self.client.models.generate_content(
                model=self.model, 
                contents=prompt, 
                config=config
            )
            if response.text:
                google_logger.info(f"LLM successfully returned structured JSON text: {response.text}")
                
                try:
                    json_data = json.loads(response.text)
                    return GeneralQuery(**json_data)
                    
                except json.JSONDecodeError as e:
                    google_logger.error(f"Failed to parse LLM output as JSON: {e}")
                except Exception as e:
                    google_logger.error(f"Failed to create GeneralQuery from parsed data: {e}")

            google_logger.error("LLM failed to produce the required GeneralQuery structure. Returning default safe query.")
            return GeneralQuery(
                filter='{"_ERROR_OR_REFUSAL": "LLM output failed to match GeneralQuery structure."}', 
                projection='{}'
            )
                
        except Exception as e:
            google_logger.error(f"Google client failed to generate content: {e}")
            raise ValueError("Client 'Google' did not generate content") from e
    

    def generate(self, prompt: str, **kwargs: Any) -> GenerateResponse:
        google_logger.info(f"Generating content using Google client for prompt: '{prompt}...'")
        
        config_params = {
            "temperature": self.temperature,
            "max_output_tokens": self.max_output_tokens,
            "system_instruction": self.SYSTEM_GUARDRAIL, 
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