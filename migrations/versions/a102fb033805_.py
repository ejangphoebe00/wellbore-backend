"""empty message

Revision ID: a102fb033805
Revises: 5d727ee176eb
Create Date: 2021-06-23 13:28:04.287882

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a102fb033805'
down_revision = '5d727ee176eb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('revoked_tokens',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('jti', sa.String(length=120), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('crane.t_CraneUser', sa.Column('UserCategory', sa.Enum('Admin', 'Staff', name='usercatgoryenum'), nullable=True))
    op.alter_column('crane.t_CraneUser', 'LoginID',
               existing_type=sa.NVARCHAR(length=255),
               nullable=True)
    op.alter_column('crane.t_CraneUser', 'UserPassword',
               existing_type=sa.TEXT(length=2147483647, collation='SQL_Latin1_General_CP1_CI_AS'),
               nullable=True)
    op.drop_column('crane.t_CraneUser', 'CraneUserID')
    op.drop_column('crane.t_CraneUser', 'StoredUserPassword')
    op.drop_column('crane.t_CraneUser', 'UserCategory_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('crane.t_CraneUser', sa.Column('UserCategory_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('crane.t_CraneUser', sa.Column('StoredUserPassword', sa.NVARCHAR(length=255), autoincrement=False, nullable=True))
    op.add_column('crane.t_CraneUser', sa.Column('CraneUserID', sa.NVARCHAR(length=255), autoincrement=False, nullable=True))
    op.alter_column('crane.t_CraneUser', 'UserPassword',
               existing_type=sa.TEXT(length=2147483647, collation='SQL_Latin1_General_CP1_CI_AS'),
               nullable=False)
    op.alter_column('crane.t_CraneUser', 'LoginID',
               existing_type=sa.NVARCHAR(length=255),
               nullable=False)
    op.drop_column('crane.t_CraneUser', 'UserCategory')
    op.drop_table('revoked_tokens')
    # ### end Alembic commands ###