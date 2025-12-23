"""
Configuration settings for Sacha Advisor backend
Supports all financial documents: insurance, loans, investments, mutual funds, 
fixed deposits, EMI schedules, pension plans, and more
"""
import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # OpenAI Configuration
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = "gpt-4o-mini"

    # File Upload Settings
    MAX_FILE_SIZE_MB: int = 50
    MAX_PAGES: int = 100
    ALLOWED_EXTENSIONS: list = [
        ".pdf", ".doc", ".docx", ".jpg", ".jpeg", ".png"]

    # Database
    DATABASE_PATH: str = "sacha_advisor.db"
    # Supabase PostgreSQL connection
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    SUPABASE_SERVICE_KEY: str = os.getenv(
        "SUPABASE_SERVICE_KEY", "")  # service_role key
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")  # Project URL

    # CORS Settings
    CORS_ORIGINS: list = ["http://localhost:5173", "http://localhost:3000"]

    # App Settings
    APP_NAME: str = "Sacha Advisor"
    APP_VERSION: str = "1.1"
    DEBUG: bool = True

    # Cache Settings
    CACHE_ENABLED: bool = True
    CACHE_TTL_SECONDS: int = 3600  # 1 hour cache for document analysis
    CACHE_MAX_SIZE: int = 100  # Maximum cache entries

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
