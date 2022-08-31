"""empty message

Revision ID: a8eebbf3896c
Revises: 79dacfb45a6b
Create Date: 2022-08-29 18:43:53.534334

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a8eebbf3896c'
down_revision = '79dacfb45a6b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('orders_email_key', 'orders', type_='unique')
    op.drop_constraint('orders_username_key', 'orders', type_='unique')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('orders_username_key', 'orders', ['username'])
    op.create_unique_constraint('orders_email_key', 'orders', ['email'])
    # ### end Alembic commands ###
