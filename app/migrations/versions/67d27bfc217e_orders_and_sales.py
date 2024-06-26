"""orders_and_sales

Revision ID: 67d27bfc217e
Revises: 558238208986
Create Date: 2024-04-17 23:11:10.097666

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '67d27bfc217e'
down_revision: Union[str, None] = '558238208986'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('order',
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('last_change_date', sa.DateTime(), nullable=False),
    sa.Column('warehouse_name', sa.String(length=255), nullable=False),
    sa.Column('country_name', sa.String(length=255), nullable=False),
    sa.Column('oblast_okrug_name', sa.String(length=255), nullable=False),
    sa.Column('region_name', sa.String(length=255), nullable=False),
    sa.Column('supplier_article', sa.String(length=255), nullable=False),
    sa.Column('nm_id', sa.BigInteger(), nullable=False),
    sa.Column('barcode', sa.String(length=255), nullable=False),
    sa.Column('category', sa.String(length=255), nullable=False),
    sa.Column('subject', sa.String(length=255), nullable=False),
    sa.Column('brand', sa.String(length=255), nullable=False),
    sa.Column('tech_size', sa.String(length=255), nullable=False),
    sa.Column('income_id', sa.BigInteger(), nullable=False),
    sa.Column('is_supply', sa.Boolean(), nullable=False),
    sa.Column('is_realization', sa.Boolean(), nullable=False),
    sa.Column('total_price', sa.Float(), nullable=False),
    sa.Column('discount_percent', sa.Integer(), nullable=False),
    sa.Column('spp', sa.Float(), nullable=False),
    sa.Column('finished_price', sa.Float(), nullable=False),
    sa.Column('price_with_disc', sa.Float(), nullable=False),
    sa.Column('order_type', sa.Enum('client', 'return_of_marriage', 'forced_return', 'return_of_anonymity', 'return_invalid_attachment', 'seller_return', name='ordertype'), nullable=False),
    sa.Column('sticker', sa.String(length=255), nullable=True),
    sa.Column('g_number', sa.String(length=255), nullable=True),
    sa.Column('srid', sa.String(length=255), nullable=True),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_order_id'), 'order', ['id'], unique=False)
    op.create_table('sale',
    sa.Column('payment_sale_amount', sa.Float(), nullable=False),
    sa.Column('for_pay', sa.Float(), nullable=False),
    sa.Column('sale_id', sa.String(length=255), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('last_change_date', sa.DateTime(), nullable=False),
    sa.Column('warehouse_name', sa.String(length=255), nullable=False),
    sa.Column('country_name', sa.String(length=255), nullable=False),
    sa.Column('oblast_okrug_name', sa.String(length=255), nullable=False),
    sa.Column('region_name', sa.String(length=255), nullable=False),
    sa.Column('supplier_article', sa.String(length=255), nullable=False),
    sa.Column('nm_id', sa.BigInteger(), nullable=False),
    sa.Column('barcode', sa.String(length=255), nullable=False),
    sa.Column('category', sa.String(length=255), nullable=False),
    sa.Column('subject', sa.String(length=255), nullable=False),
    sa.Column('brand', sa.String(length=255), nullable=False),
    sa.Column('tech_size', sa.String(length=255), nullable=False),
    sa.Column('income_id', sa.BigInteger(), nullable=False),
    sa.Column('is_supply', sa.Boolean(), nullable=False),
    sa.Column('is_realization', sa.Boolean(), nullable=False),
    sa.Column('total_price', sa.Float(), nullable=False),
    sa.Column('discount_percent', sa.Integer(), nullable=False),
    sa.Column('spp', sa.Float(), nullable=False),
    sa.Column('finished_price', sa.Float(), nullable=False),
    sa.Column('price_with_disc', sa.Float(), nullable=False),
    sa.Column('order_type', sa.Enum('client', 'return_of_marriage', 'forced_return', 'return_of_anonymity', 'return_invalid_attachment', 'seller_return', name='ordertype'), nullable=False),
    sa.Column('sticker', sa.String(length=255), nullable=True),
    sa.Column('g_number', sa.String(length=255), nullable=True),
    sa.Column('srid', sa.String(length=255), nullable=True),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_sale_id'), 'sale', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_sale_id'), table_name='sale')
    op.drop_table('sale')
    op.drop_index(op.f('ix_order_id'), table_name='order')
    op.drop_table('order')
    # ### end Alembic commands ###
