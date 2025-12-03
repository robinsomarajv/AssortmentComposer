from pydantic import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # LLM
    LLM_MODEL: str = "gpt-4o-mini"
    OPENAI_API_KEY: str = ""
    GEMINI_API_KEY: str = ""

    # Langfuse
    LANGFUSE_PUBLIC_KEY: str
    LANGFUSE_SECRET_KEY: str
    LANGFUSE_HOST: str = "https://cloud.langfuse.com"

    # A2A remote agent URLs
    INVENTORY_AGENT_CARD_URL: str
    PROCUREMENT_AGENT_CARD_URL: str
    PO_AGENT_CARD_URL: str

    # App config
    ASSORTMENT_PORT: int = 8000
    APP_NAME: str = "assortment-planner"

    # Optional: other IDs for Langfuse/logging
    LANGFUSE_PROJECT_ID: str = ""
    LANGFUSE_TRACE_ID: str = ""

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

@lru_cache()
def get_settings() -> Settings:
    return Settings()

