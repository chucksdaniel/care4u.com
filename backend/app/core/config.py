from typing import List
from pathlib import Path
from pydantic import ConfigDict
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent

class Settings(BaseSettings):
    """Application settings."""

    PROJECT_NAME: str = "Self-Service Core"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"

    # Database
    DATABASE_URL: str

    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # CORS
    CORS_ORIGINS: List[str] = ["*"]

    # class Config:
    #     """Pydantic configuration."""

    #     env_file = ".env"
    #     env_file_encoding = "utf-8"
  
    model_config = SettingsConfigDict(
        env_file="app/.env",
        env_file_encoding="utf-8",
    )

settings = Settings()