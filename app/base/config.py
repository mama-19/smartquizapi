
from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    DATABASE_URL: str
    TEST_BASE_URL: str
    FERNET_KEY: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRES_MINUTES: int = 3 * 24 * 60  # 30 days in minutes
    REFRESH_TOKEN_EXPIRES_MINUTES: int = 5 * 24 * 60 
    REFRESH_TOKEN_ROTATION: bool
    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

settings = Settings()

