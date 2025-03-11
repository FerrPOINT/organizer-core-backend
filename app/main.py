from fastapi import FastAPI
from starlette.middleware import Middleware

from app.core.logger import LogMiddleware, logger
from app.settings import user_settings  # Импортируем настройки

app = FastAPI(
    title="Organizer Core API",
    middleware=[Middleware(LogMiddleware)]
)

logger.info("🚀 Приложение FastAPI запущено!")

@app.get("/")
def read_root():
    return {"message": f"Добро пожаловать в Organizer Core API! DB: {user_settings}"}
