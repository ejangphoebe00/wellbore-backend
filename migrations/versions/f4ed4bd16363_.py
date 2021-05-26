"""empty message

Revision ID: f4ed4bd16363
Revises: 0a73f9cc67fb
Create Date: 2021-05-26 23:31:00.486369

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f4ed4bd16363'
down_revision = '0a73f9cc67fb'
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
    sa.Column('LoginID', sa.NVARCHAR(length=255), nullable=False),
    sa.Column('LoginIDAlias', sa.NVARCHAR(length=255), nullable=True),
    sa.Column('UserCompany_id', sa.Integer(), nullable=True),
    sa.Column('UserCategory_id', sa.Integer(), nullable=True),
    sa.Column('UserPremsUser_id', sa.Integer(), nullable=True),
    sa.Column('UserStaff_id', sa.Integer(), nullable=True),
    sa.Column('OrganisationName', sa.NVARCHAR(length=255), nullable=False),
    sa.Column('CraneUserID', sa.NVARCHAR(length=255), nullable=True),
    sa.Column('UserPassword', sa.TEXT(), nullable=False),
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
    sa.Column('StoredUserPassword', sa.NVARCHAR(length=255), nullable=True),
    sa.Column('PasswordChangeDate', sa.TIMESTAMP(), nullable=True),
    sa.PrimaryKeyConstraint('CraneUser_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('crane.t_CraneUser')
    # ### end Alembic commands ###
