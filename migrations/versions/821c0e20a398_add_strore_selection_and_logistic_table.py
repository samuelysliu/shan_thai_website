"""add strore_selection and logistic table

Revision ID: 821c0e20a398
Revises: 7f52afc49870
Create Date: 2025-01-06 10:08:58.460010

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '821c0e20a398'
down_revision: Union[str, None] = '7f52afc49870'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # Step 1: 暫時刪除外鍵約束
    op.drop_constraint('order_details_oid_fkey', 'order_details', type_='foreignkey')

    # Step 2: 修改 `orders.oid` 類型為 VARCHAR(10)
    op.alter_column(
        'orders',
        'oid',
        existing_type=sa.Integer(),
        type_=sa.String(length=10),
        nullable=False,
    )

    # Step 3: 修改關聯表中的外鍵類型
    op.alter_column(
        'order_details',
        'oid',
        existing_type=sa.Integer(),
        type_=sa.String(length=10),
        nullable=False,
    )

    # Step 4: 重新添加外鍵約束
    op.create_foreign_key(
        'order_details_oid_fkey',
        'order_details',
        'orders',
        ['oid'],
        ['oid'],
        ondelete='CASCADE',
    )

    op.create_table(
        "payment_callbacks",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("merchant_id", sa.String(length=50), nullable=True),
        sa.Column("merchant_trade_no", sa.String(length=10), sa.ForeignKey("orders.oid", ondelete="CASCADE"), nullable=False),
        sa.Column("store_id", sa.String(length=50), nullable=True),
        sa.Column("rtn_code", sa.Integer, nullable=True),
        sa.Column("rtn_msg", sa.String(length=255), nullable=True),
        sa.Column("trade_no", sa.String(length=50), nullable=False),
        sa.Column("trade_amt", sa.Integer, nullable=True),
        sa.Column("payment_date", sa.DateTime, nullable=True),
        sa.Column("payment_type", sa.String(length=50), nullable=True),
        sa.Column("payment_type_charge_fee", sa.Integer, server_default="0", nullable=True),
        sa.Column("platform_id", sa.String(length=50), nullable=True),
        sa.Column("trade_date", sa.DateTime, nullable=True),
        sa.Column("simulate_paid", sa.Integer, server_default="1", nullable=True),
        sa.Column("check_mac_value", sa.String(length=255), nullable=True),
        sa.Column("bank_code", sa.String(length=50), nullable=True),
        sa.Column("v_account", sa.String(length=50), nullable=True),
        sa.Column("expire_date", sa.DateTime, nullable=True),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now(), nullable=True),
    )

    # 創建 store_selection 表
    op.create_table(
        "store_selection",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("merchant_trade_no", sa.String(length=50), nullable=False),
        sa.Column("logistics_sub_type", sa.String(length=50), nullable=False),
        sa.Column("cvs_store_id", sa.String(length=50), nullable=False),
        sa.Column("cvs_store_name", sa.String(length=255), nullable=False),
        sa.Column("cvs_address", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("merchant_trade_no"),
    )

    # 創建 logistics_orders 表
    op.create_table(
        'logistics_orders',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('merchant_trade_no', sa.String(length=20), sa.ForeignKey('orders.oid', ondelete='CASCADE'), nullable=False),
        sa.Column('rtn_code', sa.Integer, nullable=False),
        sa.Column('rtn_msg', sa.Text, nullable=True),
        sa.Column('allpay_logistics_id', sa.String(length=50), nullable=False),
        sa.Column('logistics_type', sa.String(length=20), nullable=True),
        sa.Column('logistics_sub_type', sa.String(length=20), nullable=True),
        sa.Column('goods_amount', sa.Integer, nullable=True),
        sa.Column('update_status_date', sa.DateTime, nullable=True),
        sa.Column('receiver_name', sa.String(length=50), nullable=True),
        sa.Column('receiver_cell_phone', sa.String(length=20), nullable=True),
        sa.Column('receiver_email', sa.String(length=100), nullable=True),
        sa.Column('receiver_address', sa.String(length=255), nullable=True),
        sa.Column('cvs_payment_no', sa.String(length=50), nullable=True),
        sa.Column('cvs_validation_no', sa.String(length=50), nullable=True),
        sa.Column('booking_note', sa.String(length=100), nullable=True),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now(), nullable=False)
    )

    
def downgrade() -> None:
    # 刪除外鍵約束
    op.drop_constraint('order_details_oid_fkey', 'order_details', type_='foreignkey')

    # 還原 orders.oid 類型為 INTEGER
    op.alter_column(
        'orders',
        'oid',
        existing_type=sa.String(length=10),
        type_=sa.Integer(),
        nullable=False,
    )

    # 還原 order_details.oid 類型為 INTEGER
    op.alter_column(
        'order_details',
        'oid',
        existing_type=sa.String(length=10),
        type_=sa.Integer(),
        nullable=False,
    )

    # 重新添加外鍵約束
    op.create_foreign_key(
        'order_details_oid_fkey',
        'order_details',
        'orders',
        ['oid'],
        ['oid'],
        ondelete='CASCADE',
    )

    # 刪除新增的表
    op.drop_table("payment_callbacks")

    op.drop_table("store_selection")
    op.drop_table("logistics_orders")
    op.drop_table("shan_thai_token")

    # 刪除 users.referral_code 列
    op.drop_column('users', 'referral_code')
