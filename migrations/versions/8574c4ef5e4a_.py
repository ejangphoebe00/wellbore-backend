"""empty message

Revision ID: 8574c4ef5e4a
Revises: 24ec591aefca
Create Date: 2022-03-04 14:22:12.055938

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8574c4ef5e4a'
down_revision = '24ec591aefca'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('geosims_t_Wellbore', 'Basin',
               existing_type=sa.VARCHAR(length=13, collation='SQL_Latin1_General_CP1_CI_AS'),
               type_=sa.Enum('Edward-George', 'Semiliki', 'Pakwach', 'The Albertine Graben', 'Hoima Basin', 'Lake Kyoga Basin', 'Lake Wamala Basin', 'Kadam-Moroto Basin', name='fluidsamplebasin'),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('geosims_t_Wellbore', 'Basin',
               existing_type=sa.Enum('Edward-George', 'Semiliki', 'Pakwach', 'The Albertine Graben', 'Hoima Basin', 'Lake Kyoga Basin', 'Lake Wamala Basin', 'Kadam-Moroto Basin', name='fluidsamplebasin'),
               type_=sa.VARCHAR(length=13, collation='SQL_Latin1_General_CP1_CI_AS'),
               existing_nullable=True)
    # ### end Alembic commands ###