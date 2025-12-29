"""
Configuration Management
Uses Pydantic Settings for environment variable management
"""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Application
    app_name: str = "Intern_AI"
    app_version: str = "1.0.0"
    debug: bool = True
    secret_key: str
    
    # Database
    database_url: str
    
    # Vector Database
    qdrant_url: str = "http://localhost:6333"
    qdrant_api_key: str = ""
    
    # AI API Keys
    gemini_api_key: str
    openai_api_key: str = ""
    claude_api_key: str = ""
    
    # CORS
    allowed_origins: str = "http://localhost:3000"
    
    @property
    def cors_origins(self) -> List[str]:
        """Parse CORS origins from comma-separated string"""
        return [origin.strip() for origin in self.allowed_origins.split(",")]
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
