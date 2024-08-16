from pydantic_settings import BaseSettings
from dotenv import load_dotenv
load_dotenv()
from os import getenv
class Settings(BaseSettings):
    DATABASE_URL: str
    OPENAI_API_KEY: str
    OPENAI_BASE_PROVIDER: str
    LLM_TEMPERATURE: float
    EMBEDDINGS_MODEL: str
    DEVICE: str
    PG_COLLECTION_NAME: str
    PG_CONNECTION: str
    LANGCHAIN_TRACING_V2: str
    LANGCHAIN_ENDPOINT: str
    LANGCHAIN_API_KEY: str
    LANGCHAIN_PROJECT: str
    class Config:
        env_file = ".env"

settings = Settings()