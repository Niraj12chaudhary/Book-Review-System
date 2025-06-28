# app/core/config.py
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:root@localhost:5432/bookreviews")
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    app_name: str = "Book Review Service"
    debug: bool = True

    class Config:
        env_file = ".env"

settings = Settings()
