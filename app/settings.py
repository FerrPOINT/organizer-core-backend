from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Загружаем .env
load_dotenv()


class DBSettings(BaseSettings):
    DATABASE_URL: str

    class Config:
        extra = "ignore"


class AdminSettings(BaseSettings):
    ADMIN_NAME: str
    ADMIN_EMAIL: str
    ADMIN_PASSWORD: str

    class Config:
        extra = "ignore"


class OauthSettings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_HOURS: float
    ORIGIN: str

    class Config:
        extra = "ignore"


db_settings = DBSettings()
admin_settings = AdminSettings()
oauth_settings = OauthSettings()
