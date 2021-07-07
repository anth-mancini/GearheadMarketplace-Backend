from pydantic import BaseSettings

class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URL: str
    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

settings = Settings(_env_file='.env', _env_file_encoding='utf-8')