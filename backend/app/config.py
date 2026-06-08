"""Runtime configuration for the backend.

This module centralizes environment-based backend settings. The backend reads
from the root project .env file so it uses the same DATABASE_URL as the
collector.
"""

from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# Resolve the repository root from this file's location.
# backend/app/config.py -> github-issue-hunter/
PROJECT_ROOT = Path(__file__).resolve().parents[2]

class Settings(BaseSettings):
  database_url: str = Field(alias='DATABASE_URL')
  
  model_config = SettingsConfigDict(
    env_file=PROJECT_ROOT / '.env',
    env_file_encoding='utf-8',
    extra='ignore',
  )
  
settings = Settings()