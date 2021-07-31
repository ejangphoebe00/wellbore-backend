"""empty message

Revision ID: 655b063128a9
Revises: 
Create Date: 2021-07-09 13:09:33.704954

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '655b063128a9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('crane.rt_CraneWebSecurityLevel',
    sa.Column('WebSecurityLevel_id', sa.Integer(), nullable=False),
    sa.Column('WebSecurityLevelName', sa.NVARCHAR(length=255), nullable=True),
    sa.Column('WebSecurityLevelDescription', sa.NVARCHAR(length=255), nullable=True),
    sa.Column('WebSecurityLevelAbbreviation', sa.NVARCHAR(length=255), nullable=True),
    sa.Column('Comments', sa.NVARCHAR(length=500), nullable=True),
    sa.Column('ModifiedOn', sa.DateTime(), nullable=True),
    sa.Column('ModifiedBy', sa.NVARCHAR(length=255), nullable=True),
    sa.PrimaryKeyConstraint('WebSecurityLevel_id')
    )
    op.create_table('revoked_tokens',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('jti', sa.String(length=120), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('revoked_tokens')
    op.drop_table('crane.rt_CraneWebSecurityLevel')
    # ### end Alembic commands ###