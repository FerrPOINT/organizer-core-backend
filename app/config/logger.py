import logging
import sys

from fastapi import Request, Response
from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware


class InterceptHandler(logging.Handler):
    def emit(self, record):
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Поднимаемся по стеку, пока не выйдем из logging
        frame, depth = logging.currentframe(), 2
        while frame and frame.f_globals.get("__name__", "").startswith("logging"):
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def _log_formatter(record):
    function = "global" if record["function"] == "<module>" else record["function"]
    module_name = record["name"].split(".")[-1]
    return (
        f"{record['time']:YYYY-MM-DD HH:mm:ss.SSS} | "
        f"{record['level']:<8} | "
        f"{module_name}:{function}:{record['line']:<3} - "
        f"{record['message']}\n"
    )


def configure_logging():
    logger.remove()

    logger.add(
        sys.stdout,
        format=_log_formatter,
        level="INFO",
        enqueue=True,
    )

    logger.add(
        "logs/app.log",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {module}:{function}:{line} | {message}",
        level="INFO",
        rotation="10 MB",
        retention="10 days",
        compression="zip",
        enqueue=True,
    )

    # Перехватываем все существующие логгеры
    logging.root.handlers = [InterceptHandler()]
    logging.root.setLevel(logging.INFO)

    for name in logging.root.manager.loggerDict:
        ext_logger = logging.getLogger(name)
        ext_logger.handlers = [InterceptHandler()]
        ext_logger.propagate = False

    logger.info("✅ Loguru инициализирован")



class LogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        logger.info(f"📥 Входящий запрос: {request.method} {request.url}")
        response = await call_next(request)
        logger.info(f"📤 Ответ {response.status_code} на {request.method} {request.url}")
        return response
