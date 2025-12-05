from pydantic import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    LLM_MODEL: str
    LANGFUSE_PUBLIC_KEY: str
    LANGFUSE_SECRET_KEY: str
    LANGFUSE_HOST: str
    INVENTORY_AGENT_CARD_URL: str
    PROCUREMENT_AGENT_CARD_URL: str
    PO_AGENT_CARD_URL: str
    PUBLIC_BASE_URL: str = ""
    ASSORTMENT_PORT: int = 8000
    APP_NAME: str = "assortment-planner"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()
