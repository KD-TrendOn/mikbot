from pydantic_settings import BaseSettings
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
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
    LANGCHAIN_TRACING_V2: bool
    LANGCHAIN_ENDPOINT: str
    LANGCHAIN_API_KEY: str
    LANGCHAIN_PROJECT: str
    LANGFUSE_PUBLIC_KEY: str
    LANGFUSE_SECRET_KEY: str
    LANGFUSE_HOST: str

    class Config:
        env_file = ".env"


settings = Settings()
