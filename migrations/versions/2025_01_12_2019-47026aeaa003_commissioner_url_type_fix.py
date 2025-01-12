"""Commissioner Url Type Fix

Revision ID: 47026aeaa003
Revises: d4130308811a
Create Date: 2025-01-12 20:19:35.343906

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '47026aeaa003'
down_revision: Union[str, None] = 'd4130308811a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Добавляем значение "main" в тип commissariaturltype
    op.execute("ALTER TYPE commissariaturltype ADD VALUE 'MAIN'")


def downgrade():
    # Шаг 1: Создаем новый тип ENUM с нужными значениями
    op.execute("""
        CREATE TYPE commissariaturltype_new AS ENUM ('VK', 'INSTAGRAM', 'FACEBOOK', 'TELEGRAM', 'WHATSAPP', 'VIBER', 'TIKTOK');
    """)

    # Шаг 2: Меняем тип колонки с использованием нового ENUM
    op.execute("""
        ALTER TABLE commissariat_urls 
        ALTER COLUMN type TYPE commissariaturltype_new USING type::text::commissariaturltype_new;
    """)

    # Шаг 3: Удаляем старый тип ENUM
    op.execute("""
        DROP TYPE commissariaturltype;
    """)

    # Шаг 4: Переименовываем новый тип ENUM в исходное имя
    op.execute("""
        ALTER TYPE commissariaturltype_new RENAME TO commissariaturltype;
    """)


