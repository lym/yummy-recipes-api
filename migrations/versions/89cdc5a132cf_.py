"""empty message

Revision ID: 89cdc5a132cf
Revises: 
Create Date: 2017-11-18 14:34:06.619047

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '89cdc5a132cf'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'recipes', ['title'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'recipes', type_='unique')
    # ### end Alembic commands ###
