"""Runtime configuration for the GitHub Issue Collector Agent.

This module loads environment variables from the root .env file.
Keeping settings centralized prevents database URLs, API tokens, and other
runtime values from being scattered across the collector codebase.
"""

from pathlib import Path

from pydantic import Field # type: ignore
from pydantic_settings import BaseSettings, SettingsConfigDict # type: ignore

# This file lives at:
# github-issue-hunter/collector/collector/config.py
#
# parents[0] = github-issue-hunter/collector/collector
# parents[1] = github-issue-hunter/collector
# parents[2] = github-issue-hunter
#
# We use this to reliably find the root .env file.
PROJECT_ROOT = Path(__file__).resolve().parents[2]

class Settings(BaseSettings):
  """Collector settings loaded from environment variables.

    DATABASE_URL tells the collector how to connect to PostgreSQL.

    GITHUB_TOKEN is used later when the collector starts calling the GitHub API.
    It is optional for now because this step only verifies configuration loading.
    """
    
  database_url: str = Field(alias="DATABASE_URL")
  github_token: str | None = Field(default=None, alias="GITHUB_TOKEN")
  
  model_config = SettingsConfigDict(
    env_file=PROJECT_ROOT / ".env",
    env_file_encoding="utf-8",
    extra="ignore",
  )
  
settings = Settings()