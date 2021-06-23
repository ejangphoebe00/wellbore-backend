"""empty message

Revision ID: beb42a6a2a77
Revises: d3ff8635423e
Create Date: 2021-06-23 13:34:13.358302

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'beb42a6a2a77'
down_revision = 'd3ff8635423e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
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
    sa.Column('UserSecurityLevel_id', sa.Integer(), nullable=False),
    sa.Column('UserWebSecurityLevel_id', sa.Integer(), nullable=False),
    sa.Column('UserNogtrWebSecurityLevel_id', sa.Integer(), nullable=False),
    sa.Column('UserPremsWebSecurityLevel_id', sa.Integer(), nullable=False),
    sa.Column('UserIntranetSecurityLevel_id', sa.Integer(), nullable=False),
    sa.Column('UserNsdWebSecurityLevel_id', sa.Integer(), nullable=False),
    sa.Column('LoginErrorCount', sa.Integer(), nullable=True),
    sa.Column('LoginStatus_id', sa.Integer(), nullable=True),
    sa.Column('LastSeen', sa.DateTime(), nullable=True),
    sa.Column('DeactivateAccount', sa.SMALLINT(), nullable=True),
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
    sa.Column('RecordChangeStamp', sa.VARBINARY(length='MAX'), nullable=True),
    sa.Column('DefaultPassword', sa.NVARCHAR(length=255), nullable=True),
    sa.Column('DefaultChangeDate', sa.DateTime(), nullable=True),
    sa.Column('PasswordChangeDate', sa.TIMESTAMP(), nullable=True),
    sa.PrimaryKeyConstraint('CraneUser_id'),
    sa.UniqueConstraint('CraneUserName'),
    sa.UniqueConstraint('UserEmailAddress'),
    sa.UniqueConstraint('UserPremsUser_id'),
    sa.UniqueConstraint('UserStaff_id')
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
    op.drop_table('crane.t_CraneUser')
    # ### end Alembic commands ###
