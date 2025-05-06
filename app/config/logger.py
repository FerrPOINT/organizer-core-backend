import sys

from fastapi import Request, Response
from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware

# Убираем стандартные обработчики, чтобы избежать дублирования логов
logger.remove()

# Логирование в консоль
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
           "<level>{level: <8}</level> | "
           "<cyan>{module}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level="INFO",
)

# Логирование в файл
logger.add(
    "logs/app.log",
    rotation="10 MB",
    retention="10 days",
    level="INFO",
    compression="zip",
)


class LogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        logger.info(f"📥 Входящий запрос: {request.method} {request.url}")
        response = await call_next(request)
        logger.info(f"📤 Ответ {response.status_code} на {request.method} {request.url}")
        return response


logger.info("✅ Loguru инициализирован")
