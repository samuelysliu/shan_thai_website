"""add order_detail table

Revision ID: 2d4af5a039f5
Revises: d1b9c07ba2fc
Create Date: 2024-12-13 19:26:45.308451

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2d4af5a039f5'
down_revision: Union[str, None] = 'd1b9c07ba2fc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 新增欄位，允許為 NULL
    op.add_column('orders', sa.Column('discountPrice', sa.Integer(), nullable=True))
    op.add_column('orders', sa.Column('useDiscount', sa.Boolean(), nullable=True))
    op.add_column('orders', sa.Column('recipientName', sa.String(), nullable=True))  # 初始允許 NULL
    op.add_column('orders', sa.Column('recipientPhone', sa.String(length=15), nullable=True))  # 初始允許 NULL
    op.add_column('orders', sa.Column('recipientEmail', sa.String(), nullable=True))  # 初始允許 NULL
    op.add_column('orders', sa.Column('orderNote', sa.String(), nullable=True))

    # 更新現有的資料，為新欄位填充默認值
    op.execute('UPDATE orders SET "recipientName" = \'\' WHERE "recipientName" IS NULL')
    op.execute('UPDATE orders SET "recipientPhone" = \'\' WHERE "recipientPhone" IS NULL')
    op.execute('UPDATE orders SET "recipientEmail" = \'\' WHERE "recipientEmail" IS NULL')

    # 將欄位修改為 NOT NULL
    op.alter_column('orders', 'recipientName', nullable=False)
    op.alter_column('orders', 'recipientPhone', nullable=False)
    op.alter_column('orders', 'recipientEmail', nullable=False)
    op.alter_column('orders', 'address', existing_type=sa.VARCHAR(), nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    op.alter_column('orders', 'address', existing_type=sa.VARCHAR(), nullable=True)
    op.drop_column('orders', 'orderNote')
    op.drop_column('orders', 'recipientEmail')
    op.drop_column('orders', 'recipientPhone')
    op.drop_column('orders', 'recipientName')
    op.drop_column('orders', 'useDiscount')
    op.drop_column('orders', 'discountPrice')
    # ### end Alembic commands ###
