from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://user:password@localhost/organizer_db"
    SECRET_KEY: str = "super-secret-key"

    class Config:
        env_file = ".env"

settings = Settings()
