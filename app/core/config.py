from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/cargo_sms"
    TEST_DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/cargo_sms_test"
    
    SECRET_KEY: str = "your-super-secret-jwt-key-change-this-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    ALGORITHM: str = "HS256"
    
    INFOBIP_API_KEY: str = ""
    INFOBIP_BASE_URL: str = "https://api.infobip.com"
    INFOBIP_SENDER: str = "CargoSMS"
    
    SMS_SANDBOX_MODE: bool = True
    TEST_SENDER_PHONE: str = "+94771234567"
    TEST_RECEIVER_PHONE: str = "+94779876543"
    
    BCRYPT_ROUNDS: int = 12
    RATE_LIMIT_PER_MINUTE: int = 60
    
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"
    
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8080", "http://localhost:8000"]
    
    MAX_FILE_SIZE_MB: int = 10
    UPLOAD_DIR: str = "uploads/"
    
    REDIS_URL: str = "redis://localhost:6379/0"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
