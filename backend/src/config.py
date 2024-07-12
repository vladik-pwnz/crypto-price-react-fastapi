from pydantic_settings import BaseSettings, SettingsConfigDict
import logging

logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    CMC_API_KEY: str
    model_config = SettingsConfigDict(env_file="../.env")

settings = Settings()
logger.info(f"Loaded CMC_API_KEY from environment: {settings.CMC_API_KEY}")