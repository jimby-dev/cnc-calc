"""
Application configuration settings
"""
import os
from pydantic_settings import BaseSettings
from typing import List, Optional

class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    # Application
    APP_NAME: str = "CNC Calculator API"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # Database
    # No default URL - must be set via environment variable
    DATABASE_URL: str = ""
    DATABASE_POOL_SIZE: int = 10
    DATABASE_MAX_OVERFLOW: int = 20
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379"
    REDIS_PASSWORD: Optional[str] = None
    
    # Security
    # No default secret - must be set via environment variable
    SECRET_KEY: str = ""
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256"
    
    # API Key Authentication (required for all endpoints)
    API_KEY: Optional[str] = None
    
    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
    ]
    ALLOWED_HOSTS: List[str] = ["localhost", "127.0.0.1"]
    
    # AWS (for production)
    AWS_REGION: str = "us-east-1"
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    
    # Export settings
    EXPORT_MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    EXPORT_ALLOWED_FORMATS: List[str] = ["fusion_json", "csv"]
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"
    
    # Rate limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    
    class Config:
        env_file = ".env"
        case_sensitive = True
    
    def model_post_init(self, __context) -> None:
        """Validate settings after initialization"""
        self._validate_production_settings()
    
    def _validate_production_settings(self) -> None:
        """Validate that required settings are set in production"""
        if self.ENVIRONMENT == "production":
            # Validate DATABASE_URL
            if not self.DATABASE_URL:
                raise ValueError("DATABASE_URL must be set in production environment")
            if "cnc_password" in self.DATABASE_URL or "localhost" in self.DATABASE_URL:
                raise ValueError("DATABASE_URL must point to production database, not development")
            
            # Validate SECRET_KEY
            if not self.SECRET_KEY:
                raise ValueError("SECRET_KEY must be set in production environment")
            if self.SECRET_KEY == "your-secret-key-change-in-production":
                raise ValueError("SECRET_KEY must be changed from default value in production")
            
            # Validate API_KEY
            if not self.API_KEY:
                raise ValueError("API_KEY must be set in production environment")

# Create settings instance
# Pydantic-settings automatically loads from environment variables
# For development, provide defaults if not set
# Development defaults (only used if env vars not set)
_dev_defaults = {}
if os.getenv("ENVIRONMENT", "development") == "development":
    _dev_defaults = {
        "DATABASE_URL": os.getenv("DATABASE_URL", "postgresql://cnc_user:cnc_password@localhost:5432/cnc_calc"),
        "SECRET_KEY": os.getenv("SECRET_KEY", "dev-secret-key-change-in-production"),
    }

settings = Settings(**_dev_defaults)
