from fastapi import FastAPI
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware import Middleware

from app.core.error_handler import ErrorHandler
from app.core.logger import LogMiddleware, logger
from app.settings import user_settings  # Импортируем настройки

app = FastAPI(
    title="Organizer Core API",
    middleware=[Middleware(LogMiddleware)]
)

# ✅ Регистрируем обработчики ошибок
app.add_exception_handler(StarletteHTTPException, ErrorHandler.http_exception_handler)
app.add_exception_handler(Exception, ErrorHandler.general_exception_handler)

logger.info("🚀 Приложение FastAPI запущено!")


@app.get("/")
def read_root():
    return {"message": f"Добро пожаловать в Organizer Core API! DB: {user_settings}"}
