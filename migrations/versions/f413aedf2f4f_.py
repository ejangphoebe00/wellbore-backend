"""empty message

Revision ID: f413aedf2f4f
Revises: b857fea6bc1c
Create Date: 2021-08-06 14:07:14.379743

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f413aedf2f4f'
down_revision = 'b857fea6bc1c'
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
    op.create_table('crane.t_CraneUser',
    sa.Column('CraneUser_id', sa.Integer(), nullable=False),
    sa.Column('FirstName', sa.NVARCHAR(length=255), nullable=False),
    sa.Column('MiddleName', sa.NVARCHAR(length=255), nullable=True),
    sa.Column('Surname', sa.NVARCHAR(length=255), nullable=False),
    sa.Column('LUID', sa.Integer(), nullable=True),
    sa.Column('CraneUserName', sa.NVARCHAR(length=255), nullable=False),
    sa.Column('LoginID', sa.NVARCHAR(length=255), nullable=True),
    sa.Column('LoginIDAlias', sa.NVARCHAR(length=255), nullable=True),
    sa.Column('UserCategory', sa.Enum('Admin', 'Staff', name='usercatgoryenum'), nullable=True),
    sa.Column('UserCompany_id', sa.Integer(), nullable=True),
    sa.Column('UserPremsUser_id', sa.Integer(), nullable=True),
    sa.Column('UserStaff_id', sa.Integer(), nullable=True),
    sa.Column('OrganisationName', sa.NVARCHAR(length=255), nullable=False),
    sa.Column('UserPassword', sa.NVARCHAR(length=255), nullable=True),
    sa.Column('UserEmailAddress', sa.NVARCHAR(length=255), nullable=False),
    sa.Column('UserSecurityLevel_id', sa.Integer(), nullable=True),
    sa.Column('UserWebSecurityLevel_id', sa.Integer(), nullable=False),
    sa.Column('UserNogtrWebSecurityLevel_id', sa.Integer(), nullable=True),
    sa.Column('UserPremsWebSecurityLevel_id', sa.Integer(), nullable=True),
    sa.Column('UserIntranetSecurityLevel_id', sa.Integer(), nullable=True),
    sa.Column('UserNsdWebSecurityLevel_id', sa.Integer(), nullable=True),
    sa.Column('LoginErrorCount', sa.Integer(), nullable=True),
    sa.Column('LoginStatus_id', sa.Integer(), nullable=True),
    sa.Column('LastSeen', sa.DateTime(), nullable=True),
    sa.Column('DeactivateAccount', sa.SMALLINT(), nullable=False),
    sa.Column('ActivationChangeComment', sa.NVARCHAR(length=255), nullable=True),
    sa.Column('ActivationChangeDate', sa.DateTime(), nullable=True),
    sa.Column('CredentialsSent', sa.SMALLINT(), nullable=True),
    sa.Column('UserOnlineStatus', sa.SMALLINT(), nullable=True),
    sa.Column('Comments', sa.NVARCHAR(length=500), nullable=True),
    sa.Column('OrganisationUserName', sa.NVARCHAR(length=255), nullable=True),
    sa.Column('CreatedBy_id', sa.Integer(), nullable=True),
    sa.Column('DateCreated', sa.DateTime(), nullable=True),
    sa.Column('ModifiedOn', sa.DateTime(), nullable=True),
    sa.Column('ModifiedBy', sa.NVARCHAR(length=255), nullable=True),
    sa.Column('RecordChangeStamp', sa.NVARCHAR(length=100), nullable=True),
    sa.Column('DefaultPassword', sa.NVARCHAR(length=255), nullable=True),
    sa.Column('DefaultChangeDate', sa.DateTime(), nullable=True),
    sa.Column('PasswordChangeDate', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['UserWebSecurityLevel_id'], ['crane.rt_CraneWebSecurityLevel.WebSecurityLevel_id'], ),
    sa.PrimaryKeyConstraint('CraneUser_id'),
    sa.UniqueConstraint('CraneUserName'),
    sa.UniqueConstraint('UserEmailAddress'),
    sa.UniqueConstraint('UserStaff_id')
    )
    op.create_table('crane.t_CraneUserLoginHistory',
    sa.Column('UserLoginHistory_id', sa.Integer(), nullable=False),
    sa.Column('HistLogUser_id', sa.Integer(), nullable=False),
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
    sa.ForeignKeyConstraint(['HistLogUser_id'], ['crane.t_CraneUser.CraneUser_id'], ),
    sa.PrimaryKeyConstraint('UserLoginHistory_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('crane.t_CraneUserLoginHistory')
    op.drop_table('crane.t_CraneUser')
    op.drop_table('revoked_tokens')
    op.drop_table('crane.rt_CraneWebSecurityLevel')
    # ### end Alembic commands ###