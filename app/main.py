from fastapi import FastAPI
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware import Middleware

from app.core.error_handler import ErrorHandler
from app.core.logger import LogMiddleware, logger
from app.routes import auth, users
from app.util.init_db import init_default_admin  #
from app.util.openapi_saver import save_openapi_schema, save_openapi_schema_yaml

logger.info("🚀 Проверка базы и инициализация...")
init_default_admin()  # ✅ Запускаем создание дефолтного админа

logger.info("✅ Создание апи")
app = FastAPI(
    title="Organizer Core API",
    middleware=[Middleware(LogMiddleware)]
)

logger.info("✅ Регистрируем роуты")
app.include_router(auth.router)
app.include_router(users.router)

logger.info("✅ Регистрируем обработчики ошибок")
app.add_exception_handler(StarletteHTTPException, ErrorHandler.http_exception_handler)
app.add_exception_handler(Exception, ErrorHandler.general_exception_handler)

logger.info("🚀 Приложение FastAPI запущено!")

logger.info("✅ Сохранение опенапи схемы")
save_openapi_schema(app)
save_openapi_schema_yaml(app)
