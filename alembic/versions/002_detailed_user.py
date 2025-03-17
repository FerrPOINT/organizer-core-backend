"""Расширение таблицы users новыми полями"""

from alembic import op

revision = '002'
down_revision = '001'


def upgrade():
    op.execute("""
        ALTER TABLE users
        ADD COLUMN hashed_password VARCHAR(255) NOT NULL DEFAULT '',
        ADD COLUMN role VARCHAR(50) DEFAULT 'USER',
        ADD COLUMN is_active BOOLEAN DEFAULT TRUE,
        ADD COLUMN created_at TIMESTAMP DEFAULT NOW(),
        ADD COLUMN updated_at TIMESTAMP DEFAULT NOW();
    """)


def downgrade():
    op.execute("""
        ALTER TABLE users 
        DROP COLUMN hashed_password,
        DROP COLUMN role,
        DROP COLUMN is_active,
        DROP COLUMN created_at,
        DROP COLUMN updated_at;
    """)
