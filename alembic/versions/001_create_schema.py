"""Добавление таблицы users"""

from alembic import op

revision = '001'
down_revision = None


def upgrade():
    """Применение миграции (создание таблицы)"""
    op.execute("""
        CREATE TABLE users (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(150) UNIQUE NOT NULL
        );
    """)


def downgrade():
    """Откат миграции (удаление таблицы)"""
    op.execute("""
        DROP TABLE users;
    """)
