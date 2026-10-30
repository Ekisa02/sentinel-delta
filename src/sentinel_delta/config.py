import os
from pydantic import BaseSettings


class Settings(BaseSettings):
    APP_ENV: str = os.getenv("APP_ENV", "development")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite+sqlite:///./sentinel_delta.db")
    MODEL_DIR: str = os.getenv("MODEL_DIR", "./models")
    DEFAULT_MODEL_PATH: str = os.getenv("DEFAULT_MODEL_PATH", "./models/seed_model.pt")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")


settings = Settings()
