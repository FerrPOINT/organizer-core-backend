from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware import Middleware

from app.api.routes import users, auth
from app.config.error_handler import ErrorHandler
from app.config.init_db import init_default_admin  #
from app.config.logger import LogMiddleware
from app.config.openapi_saver import save_openapi_schema, save_openapi_schema_yaml
from app.settings import oauth_settings  # Импортируем настройки

logger.info("🚀 Проверка базы и инициализация...")
init_default_admin()  # ✅ Запускаем создание дефолтного админа

logger.info("✅ Создание апи")
app = FastAPI(
    title="Organizer Core API",
    middleware=[Middleware(LogMiddleware)]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[oauth_settings.ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger.info("✅ Регистрируем роуты")
app.include_router(auth.router)
app.include_router(users.router)

logger.info("✅ Регистрируем обработчики ошибок")
app.add_exception_handler(StarletteHTTPException, ErrorHandler.http_exception_handler)
app.add_exception_handler(RequestValidationError, ErrorHandler.validation_exception_handler)
app.add_exception_handler(Exception, ErrorHandler.general_exception_handler)

logger.info("🚀 Приложение FastAPI запущено!")

logger.info("✅ Сохранение опенапи схемы")
save_openapi_schema(app)
save_openapi_schema_yaml(app)
if oauth_settings.OPENAPI_COPY_FOLDER:
    save_openapi_schema(app, oauth_settings.OPENAPI_COPY_FOLDER + "openapi.json")
