# # original
# from pydantic_settings import BaseSettings
# class Settings(BaseSettings):
#     DATABASE_URL: str
#     TEST_BASE_URL: str
#     FERNET_KEY: str

#     class Config:
#         env_file = ".env"
#         env_file_encoding = 'utf-8'

# settings = Settings()

# config with mailtrap
from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    DATABASE_URL: str
    TEST_BASE_URL: str
    FERNET_KEY: str
    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

settings = Settings()

