# app/main.py
from fastapi import FastAPI
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware import Middleware

from app.core.error_handler import ErrorHandler
from app.core.logger import LogMiddleware, logger
from app.init_db import init_default_admin  #
from app.routes import auth, users
from app.services.openapi_saver import save_openapi_schema, save_openapi_schema_yaml
from app.settings import admin_settings  # Импортируем настройки

logger.info("[🚀] Проверка базы и инициализация...")
init_default_admin()  # ✅ Запускаем создание дефолтного админа

app = FastAPI(
    title="Organizer Core API",
    middleware=[Middleware(LogMiddleware)]
)
# ✅ Регистрируем роуты
app.include_router(auth.router)
app.include_router(users.router)

# ✅ Регистрируем обработчики ошибок
app.add_exception_handler(StarletteHTTPException, ErrorHandler.http_exception_handler)
app.add_exception_handler(Exception, ErrorHandler.general_exception_handler)

logger.info("🚀 Приложение FastAPI запущено!")

# ✅ Сохранение опенапи схемы
save_openapi_schema(app)
save_openapi_schema_yaml(app)


# TODO: тестовый эндпоинт, удалить после тестирования АПИ
@app.get("/")
def read_root():
    return {"message": f"Добро пожаловать в Organizer Core API! DB: {admin_settings.ADMIN_NAME}"}
