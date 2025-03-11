from fastapi import Request
from fastapi.responses import JSONResponse
from loguru import logger
from starlette.exceptions import HTTPException as StarletteHTTPException


class ErrorHandler:
    @staticmethod
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        """Обрабатывает HTTP-исключения (404, 422 и т. д.)"""
        logger.error(f"🚨 HTTP {exc.status_code}: {exc.detail} при запросе {request.method} {request.url}")
        return JSONResponse({"error": exc.detail}, status_code=exc.status_code)

    @staticmethod
    async def general_exception_handler(request: Request, exc: Exception):
        """Обрабатывает все неожиданные ошибки"""
        logger.exception(f"🔥 Необработанная ошибка: {request.method} {request.url}")
        return JSONResponse({"error": "Внутренняя ошибка сервера"}, status_code=500)
