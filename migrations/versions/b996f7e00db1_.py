"""empty message

Revision ID: b996f7e00db1
Revises: 
Create Date: 2022-12-16 21:01:16.299309

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b996f7e00db1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('saved_recipes', 'instructions',
               existing_type=sa.TEXT(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('saved_recipes', 'instructions',
               existing_type=sa.TEXT(),
               nullable=False)
    # ### end Alembic commands ###
