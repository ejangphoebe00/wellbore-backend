"""empty message

Revision ID: 5c28fc29fdfa
Revises: d043f13a1281
Create Date: 2021-07-09 14:10:46.573072

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5c28fc29fdfa'
down_revision = 'd043f13a1281'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('crane.rt_CatalogSecurityFlag',
    sa.Column('CatalogSecurityFlag_id', sa.Integer(), nullable=False),
    sa.Column('CatalogSecurityFlagName', sa.NVARCHAR(length=255), nullable=True),
    sa.Column('SortOrder', sa.Integer(), nullable=True),
    sa.Column('Comments', sa.NVARCHAR(length=500), nullable=True),
    sa.Column('ModifiedOn', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('CatalogSecurityFlag_id')
    )
    op.create_table('crane.rt_CoreType',
    sa.Column('CoreType_id', sa.Integer(), nullable=False),
    sa.Column('CoreTypeName', sa.NVARCHAR(length=255), nullable=True),
    sa.Column('SortOrder', sa.Integer(), nullable=True),
    sa.Column('Comments', sa.NVARCHAR(length=500), nullable=True),
    sa.Column('ModifiedOn', sa.TIMESTAMP(), nullable=True),
    sa.PrimaryKeyConstraint('CoreType_id')
    )
    op.create_table('crane.rt_FileFormat',
    sa.Column('FileFormat_id', sa.Integer(), nullable=False),
    sa.Column('FileFormatName', sa.NVARCHAR(length=255), nullable=True),
    sa.Column('SortOrder', sa.Integer(), nullable=True),
    sa.Column('Comments', sa.NVARCHAR(length=500), nullable=True),
    sa.Column('ModifiedOn', sa.TIMESTAMP(), nullable=True),
    sa.PrimaryKeyConstraint('FileFormat_id')
    )
    op.create_table('crane.rt_FileSecurityGrade',
    sa.Column('FileSecurityGrade_id', sa.Integer(), nullable=False),
    sa.Column('FileSecurityGradeName', sa.NVARCHAR(length=255), nullable=True),
    sa.Column('SortOrder', sa.Integer(), nullable=True),
    sa.Column('Comments', sa.NVARCHAR(length=500), nullable=True),
    sa.Column('ModifiedOn', sa.TIMESTAMP(), nullable=True),
    sa.PrimaryKeyConstraint('FileSecurityGrade_id')
    )
    op.create_table('crane.t_CraneUserLoginHistory',
    sa.Column('UserLoginHistory_id', sa.Integer(), nullable=False),
    sa.Column('LogStaff_id', sa.Integer(), nullable=True),
    sa.Column('CraneCompany_id', sa.Integer(), nullable=True),
    sa.Column('LogCompanyAuthorisedUser_id', sa.Integer(), nullable=True),
    sa.Column('LogAuthorisedUserName', sa.VARCHAR(length=100), nullable=True),
    sa.Column('LoginStatus_id', sa.Integer(), nullable=True),
    sa.Column('UserOnlineStatus', sa.SMALLINT(), nullable=True),
    sa.Column('LogLoginDate', sa.DateTime(), nullable=True),
    sa.Column('LogLogoutDate', sa.DateTime(), nullable=True),
    sa.Column('UserLoginLogName', sa.VARCHAR(length=100), nullable=True),
    sa.Column('UserAcessLogName', sa.VARCHAR(length=100), nullable=True),
    sa.Column('Comments', sa.NVARCHAR(length=500), nullable=True),
    sa.PrimaryKeyConstraint('UserLoginHistory_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('crane.t_CraneUserLoginHistory')
    op.drop_table('crane.rt_FileSecurityGrade')
    op.drop_table('crane.rt_FileFormat')
    op.drop_table('crane.rt_CoreType')
    op.drop_table('crane.rt_CatalogSecurityFlag')
    # ### end Alembic commands ###
