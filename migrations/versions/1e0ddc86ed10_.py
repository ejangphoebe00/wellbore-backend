"""empty message

Revision ID: 1e0ddc86ed10
Revises: f2af16d7de43
Create Date: 2021-09-15 01:56:54.777941

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1e0ddc86ed10'
down_revision = 'f2af16d7de43'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('crane_t_CraneUser', 'UserCategory')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('crane_t_CraneUser', sa.Column('UserCategory', sa.VARCHAR(length=5, collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=True))
    # ### end Alembic commands ###