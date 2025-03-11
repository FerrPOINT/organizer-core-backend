from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Загружаем .env
load_dotenv()


class DBSettings(BaseSettings):
    DATABASE_URL: str

    class Config:
        extra = "ignore"


class UserSettings(BaseSettings):
    USER_NAME: str
    USER_EMAIL: str

    class Config:
        extra = "ignore"


db_settings = DBSettings()
user_settings = UserSettings()
