import sys

from sqlalchemy.orm import Session

from app.config.logger import logger
from app.db.models.user import User
from app.db.session_factory import SessionLocal
from app.services.auth import get_password_hash
from app.settings import admin_settings


def init_default_admin():
    db: Session = SessionLocal()

    try:
        # Проверяем, есть ли хоть один пользователь в базе
        user_exists = db.query(User).first()
        if user_exists:
            logger.info("✅ В базе уже есть пользователи, создание админа не требуется.")
            return

        logger.info("⚙️ В базе нет пользователей. Создаю администратора...")

        # Создаём админа
        admin = User(
            name=admin_settings.ADMIN_NAME,
            email=admin_settings.ADMIN_EMAIL,
            hashed_password=get_password_hash(admin_settings.ADMIN_PASSWORD),
            role="admin",
        )
        db.add(admin)
        db.commit()
        logger.info(f"✅ Администратор '{admin.username}' успешно создан.")

    except Exception as e:
        logger.info(f"❌ Ошибка при создании админа: {e}")
        sys.exit(1)
    finally:
        db.close()
