"""empty message

Revision ID: 90d590ee5eb5
Revises: 439dfff891ec
Create Date: 2017-10-17 16:48:49.015404

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '90d590ee5eb5'
down_revision = '439dfff891ec'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('ingredients', 'created',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('instructions', 'created',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('instructions', 'created',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('ingredients', 'created',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    # ### end Alembic commands ###