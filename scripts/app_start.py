import subprocess
import subprocess
import sys
import time

from loguru import logger
from sqlalchemy import text

from app.db.session_factory import engine
from config.logger import configure_logging


# Логирование

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
    subprocess.run([sys.executable, "-m", "alembic", "upgrade", "head"], check=True)
    logger.info("✅ Все миграции применены!")


# Запускаем main
def start_server():
    try:
        """Запускаем FastAPI."""
        logger.info("🚀 Запуск FastAPI...")
        subprocess.run([sys.executable, "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"],
                       check=True)
    except KeyboardInterrupt:
        logger.info("🛑 Сервер остановлен пользователем (Ctrl+C)")
        sys.exit(0)
    except Exception as e:
        logger.info(f"❌ Ошибка при запуске сервера: {e}")
        sys.exit(1)


configure_logging()
wait_for_db()
run_migrations()
start_server()