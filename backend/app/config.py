"""
Configuration settings for Sacha Advisor backend
"""
import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # OpenAI Configuration
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = "gpt-4o-mini"

    # File Upload Settings
    MAX_FILE_SIZE_MB: int = 50
    MAX_PAGES: int = 50
    ALLOWED_EXTENSIONS: list = [
        ".pdf", ".doc", ".docx", ".jpg", ".jpeg", ".png"]

    # Database
    DATABASE_PATH: str = "sacha_advisor.db"

    # CORS Settings
    CORS_ORIGINS: list = ["http://localhost:5173", "http://localhost:3000"]

    # App Settings
    APP_NAME: str = "Sacha Advisor"
    APP_VERSION: str = "1.1"
    DEBUG: bool = True

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
