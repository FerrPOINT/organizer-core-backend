import logging
import subprocess
import time

from fastapi import FastAPI
from sqlalchemy import text

from app.db import engine

app = FastAPI(title="Organizer Core API")

# Логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Ожидаем доступность БД
def wait_for_db():
    """Ожидаем доступности базы данных перед запуском миграций."""
    timeout = 30  # Максимальное время ожидания БД (в секундах)

    # Логируем URL подключения
    logger.info(f"Подключаемся к базе данных: {engine.url}")  # Логируем URL подключения

    while timeout > 0:
        try:
            with engine.connect() as connection:
                # Простой запрос для проверки подключения к базе данных
                connection.execute(text("SELECT 1"))
                logger.info("✅ База данных доступна!")
                return  # Если база данных доступна, выходим из функции
        except Exception:
            logger.warning("⏳ Ожидание БД...")
            time.sleep(2)  # Если база данных недоступна, ждем 2 секунды
            timeout -= 2  # Уменьшаем время ожидания на 2 секунды
    # Если база данных не доступна после всех попыток, выводим ошибку и завершаем процесс
    logger.error("❌ База данных недоступна! Выход.")
    exit(1)


# Применяем миграции Alembic
def run_migrations():
    """Применяем миграции Alembic."""
    logger.info("🔄 Применяем миграции Alembic...")
    subprocess.run(["alembic", "upgrade", "head"], check=True)  # Убираем --config
    logger.info("✅ Все миграции применены!")


def start_server():
    """Запускаем FastAPI."""
    logger.info("🚀 Запуск FastAPI...")
    subprocess.run(["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"], check=True)


# Ожидаем доступность БД и применяем миграции
wait_for_db()
run_migrations()
start_server()


@app.get("/")
def read_root():
    return {"message": "Welcome to Organizer Core API"}
