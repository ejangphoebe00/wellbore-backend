"""empty message

Revision ID: 858c0886f374
Revises: 45ee234de9e7
Create Date: 2021-08-18 17:32:56.007168

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '858c0886f374'
down_revision = '45ee234de9e7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('crane_t_Wellbore', sa.Column('DevelopmentAreaName', sa.Enum('KFDA', 'TDA', name='developmentareaenum'), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('crane_t_Wellbore', 'DevelopmentAreaName')
    # ### end Alembic commands ###
