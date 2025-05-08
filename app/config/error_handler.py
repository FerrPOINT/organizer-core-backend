from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from loguru import logger
from starlette.exceptions import HTTPException as StarletteHTTPException


class ErrorHandler:
    @staticmethod
    async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
        """
        Обработка ожидаемых HTTP-исключений (404, 422 и др.).
        """
        logger.warning(f"🚨 HTTP {exc.status_code} | {request.method} {request.url} — {exc.detail}")
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

    @staticmethod
    async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        """
        Обработка неожиданных (непредусмотренных) исключений.
        """
        logger.exception(f"🔥 Необработанная ошибка при {request.method} {request.url}", exc)
        return JSONResponse(status_code=500, content={"detail": "Внутренняя ошибка сервера"})

    @staticmethod
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        logger.warning(
            f"❌ Ошибка валидации при {request.method} {request.url}\n"
            f"📦 Тело запроса: {exc.body}\n"
            f"🔍 Ошибки: {exc.errors()}"
        )
        return JSONResponse(status_code=422, content={"detail": exc.errors()})
