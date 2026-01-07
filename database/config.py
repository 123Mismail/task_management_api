from pydantic_settings import SettingsConfigDict, BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

    DATABASE_URL: Optional[str] = os.getenv("DATABASE_URL", "sqlite:///./task_management.db")


settings = Settings()