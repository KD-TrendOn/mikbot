from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    OPENAI_API_KEY: str
    LIGHT_MODEL_NAME: str
    MAIN_MODEL_NAME: str
    LLM_TEMPERATURE: float
    EMBEDDINGS_MODEL: str
    DEVICE: str
    PG_COLLECTION_NAME: str
    PG_CONNECTION: str

    class Config:
        env_file = ".env"

settings = Settings()