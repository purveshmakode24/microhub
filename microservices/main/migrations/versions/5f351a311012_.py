"""empty message

Revision ID: 5f351a311012
Revises: ad46b2d4bf85
Create Date: 2023-07-21 12:52:27.846994

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5f351a311012'
down_revision = 'ad46b2d4bf85'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('like', schema=None) as batch_op:
        batch_op.create_unique_constraint('unique_user_product', ['user_id', 'product_id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('like', schema=None) as batch_op:
        batch_op.drop_constraint('unique_user_product', type_='unique')

    # ### end Alembic commands ###
