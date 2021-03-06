"""empty message

Revision ID: 24ec591aefca
Revises: 
Create Date: 2022-02-11 11:25:31.701759

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '24ec591aefca'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('geosims_rt_CraneWebSecurityLevel',
    sa.Column('WebSecurityLevelId', sa.Integer(), nullable=False),
    sa.Column('WebSecurityLevelName', sa.NVARCHAR(length=255), nullable=False),
    sa.Column('WebSecurityLevelDescription', sa.NVARCHAR(length=255), nullable=True),
    sa.Column('WebSecurityLevelAbbreviation', sa.NVARCHAR(length=255), nullable=True),
    sa.Column('Comments', sa.NVARCHAR(length=500), nullable=True),
    sa.Column('ModifiedOn', sa.DateTime(), nullable=True),
    sa.Column('ModifiedBy', sa.NVARCHAR(length=255), nullable=True),
    sa.PrimaryKeyConstraint('WebSecurityLevelId'),
    sa.UniqueConstraint('WebSecurityLevelAbbreviation'),
    sa.UniqueConstraint('WebSecurityLevelName')
    )
    op.create_table('revoked_tokens',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('jti', sa.String(length=120), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('geosims_t_CraneUser',
    sa.Column('CraneUserId', sa.Integer(), nullable=False),
    sa.Column('FirstName', sa.NVARCHAR(length=255), nullable=False),
    sa.Column('MiddleName', sa.NVARCHAR(length=255), nullable=True),
    sa.Column('Surname', sa.NVARCHAR(length=255), nullable=False),
    sa.Column('LUID', sa.Integer(), nullable=True),
    sa.Column('CraneUserName', sa.NVARCHAR(length=255), nullable=False),
    sa.Column('LoginID', sa.NVARCHAR(length=255), nullable=True),
    sa.Column('LoginIDAlias', sa.NVARCHAR(length=255), nullable=True),
    sa.Column('UserCategory', sa.Enum('App Admin', 'Data Admin', 'Staff', name='usercatgoryenum'), nullable=True),
    sa.Column('UserCompanyId', sa.Integer(), nullable=True),
    sa.Column('UserPremsUserId', sa.Integer(), nullable=True),
    sa.Column('UserStaffId', sa.Integer(), nullable=True),
    sa.Column('OrganisationName', sa.NVARCHAR(length=255), nullable=False),
    sa.Column('UserPassword', sa.NVARCHAR(length=255), nullable=True),
    sa.Column('UserEmailAddress', sa.NVARCHAR(length=255), nullable=False),
    sa.Column('UserSecurityLevelId', sa.Integer(), nullable=True),
    sa.Column('UserWebSecurityLevelId', sa.Integer(), nullable=False),
    sa.Column('UserNogtrWebSecurityLevelId', sa.Integer(), nullable=True),
    sa.Column('UserPremsWebSecurityLevelId', sa.Integer(), nullable=True),
    sa.Column('UserIntranetSecurityLevelId', sa.Integer(), nullable=True),
    sa.Column('UserNsdWebSecurityLevelId', sa.Integer(), nullable=True),
    sa.Column('LoginErrorCount', sa.Integer(), nullable=True),
    sa.Column('LoginStatusId', sa.Integer(), nullable=True),
    sa.Column('LastSeen', sa.DateTime(), nullable=True),
    sa.Column('DeactivateAccount', sa.SMALLINT(), nullable=False),
    sa.Column('ActivationChangeComment', sa.NVARCHAR(length=255), nullable=True),
    sa.Column('ActivationChangeDate', sa.DateTime(), nullable=True),
    sa.Column('CredentialsSent', sa.SMALLINT(), nullable=True),
    sa.Column('UserOnlineStatus', sa.SMALLINT(), nullable=True),
    sa.Column('Comments', sa.NVARCHAR(length=500), nullable=True),
    sa.Column('OrganisationUserName', sa.NVARCHAR(length=255), nullable=True),
    sa.Column('ProfilePicture', sa.NVARCHAR(length=225), nullable=True),
    sa.Column('CreatedById', sa.Integer(), nullable=True),
    sa.Column('DateCreated', sa.DateTime(), nullable=True),
    sa.Column('ModifiedOn', sa.DateTime(), nullable=True),
    sa.Column('ModifiedBy', sa.NVARCHAR(length=255), nullable=True),
    sa.Column('RecordChangeStamp', sa.NVARCHAR(length=100), nullable=True),
    sa.Column('DefaultPassword', sa.NVARCHAR(length=255), nullable=True),
    sa.Column('DefaultChangeDate', sa.DateTime(), nullable=True),
    sa.Column('PasswordChangeDate', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['UserWebSecurityLevelId'], ['geosims_rt_CraneWebSecurityLevel.WebSecurityLevelId'], ),
    sa.PrimaryKeyConstraint('CraneUserId'),
    sa.UniqueConstraint('CraneUserName'),
    sa.UniqueConstraint('UserEmailAddress'),
    sa.UniqueConstraint('UserStaffId')
    )
    op.create_table('geosims_rt_PasswordReset',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('ResetKey', sa.String(length=128), nullable=True),
    sa.Column('CraneUserId', sa.Integer(), nullable=True),
    sa.Column('CreationDate', sa.DateTime(), nullable=False),
    sa.Column('HasActivated', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['CraneUserId'], ['geosims_t_CraneUser.CraneUserId'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('ResetKey')
    )
    op.create_table('geosims_t_Company',
    sa.Column('CompanyId', sa.Integer(), nullable=False),
    sa.Column('PAUID', sa.NVARCHAR(length=255), nullable=False),
    sa.Column('CompanyLongName', sa.NVARCHAR(length=255), nullable=False),
    sa.Column('CompanyShortName', sa.NVARCHAR(length=255), nullable=True),
    sa.Column('NSDNumber', sa.NVARCHAR(length=255), nullable=False),
    sa.Column('CompanyCategoryId', sa.Integer(), nullable=True),
    sa.Column('Country', sa.String(), nullable=True),
    sa.Column('RegistrationNumber', sa.NVARCHAR(length=255), nullable=False),
    sa.Column('TINNumber', sa.NVARCHAR(length=255), nullable=False),
    sa.Column('CompanyTelephone', sa.NVARCHAR(length=255), nullable=True),
    sa.Column('CompanyEmail', sa.NVARCHAR(length=255), nullable=True),
    sa.Column('CompanyWebsite', sa.TEXT(), nullable=True),
    sa.Column('CompanyEntityTypeId', sa.Integer(), nullable=True),
    sa.Column('CompanyEntitySubTypeId', sa.Integer(), nullable=True),
    sa.Column('CompanyMajorActivityId', sa.Integer(), nullable=True),
    sa.Column('CompanyActivityDivisionId', sa.Integer(), nullable=True),
    sa.Column('CompanyActivityDivisionClassId', sa.Integer(), nullable=True),
    sa.Column('CompanyActivityDivisionClassCategoryId', sa.Integer(), nullable=True),
    sa.Column('BusinessNatureDescription', sa.TEXT(), nullable=True),
    sa.Column('CompanyPostalAddress', sa.NVARCHAR(length=255), nullable=True),
    sa.Column('CompanyPhysicalAddress', sa.NVARCHAR(length=255), nullable=True),
    sa.Column('CompanyOtherEmails', sa.NVARCHAR(length=255), nullable=True),
    sa.Column('NSDQualificationDate', sa.DateTime(), nullable=True),
    sa.Column('NSDQualificationYear', sa.String(length=10), nullable=True),
    sa.Column('PrimaryContactEntity', sa.NVARCHAR(length=50), nullable=True),
    sa.Column('ContactEntityEmail', sa.NVARCHAR(length=100), nullable=True),
    sa.Column('ContactEntityTelephone', sa.NVARCHAR(length=55), nullable=True),
    sa.Column('ContactEntityMobile', sa.NVARCHAR(length=55), nullable=True),
    sa.Column('ContactDesignation', sa.NVARCHAR(length=100), nullable=True),
    sa.Column('OperatorSortOrder', sa.Integer(), nullable=True),
    sa.Column('ContractorSortOrder', sa.Integer(), nullable=True),
    sa.Column('PAURegistrationDate', sa.DateTime(), nullable=True),
    sa.Column('CraneNOGTRID', sa.NVARCHAR(length=100), nullable=True),
    sa.Column('TempNOGTRIPwd', sa.TEXT(), nullable=True),
    sa.Column('RegistrationStatusId', sa.Integer(), nullable=True),
    sa.Column('ClassifyAsUgandanId', sa.Integer(), nullable=True),
    sa.Column('Comments', sa.TEXT(), nullable=True),
    sa.Column('PrimaryCompanyKindId', sa.Integer(), nullable=True),
    sa.Column('SecondaryCompanyKindId', sa.Integer(), nullable=True),
    sa.Column('OtherCompanyKindId', sa.Integer(), nullable=True),
    sa.Column('CompanyGroupId', sa.Integer(), nullable=True),
    sa.Column('CompanyMobile', sa.NVARCHAR(length=55), nullable=True),
    sa.Column('CompanyFax', sa.NVARCHAR(length=55), nullable=True),
    sa.Column('ContactEntityFax', sa.NVARCHAR(length=55), nullable=True),
    sa.Column('NSDFromDate', sa.Date(), nullable=True),
    sa.Column('NSDToDate', sa.Date(), nullable=True),
    sa.Column('ImportedFromNSD', sa.SMALLINT(), nullable=True),
    sa.Column('ImportedDate', sa.DateTime(), nullable=True),
    sa.Column('ExportedDate', sa.DateTime(), nullable=True),
    sa.Column('ExportedToNogtr', sa.SMALLINT(), nullable=True),
    sa.Column('CreatedBy', sa.Integer(), nullable=False),
    sa.Column('DateCreated', sa.DateTime(), nullable=True),
    sa.Column('ModifiedOn', sa.DateTime(), nullable=True),
    sa.Column('ModifiedBy', sa.Integer(), nullable=True),
    sa.Column('RecordChangeStamp', sa.NVARCHAR(length=100), nullable=True),
    sa.Column('PreviousLegalName', sa.NVARCHAR(length=100), nullable=True),
    sa.ForeignKeyConstraint(['CreatedBy'], ['geosims_t_CraneUser.CraneUserId'], ),
    sa.ForeignKeyConstraint(['ModifiedBy'], ['geosims_t_CraneUser.CraneUserId'], ),
    sa.PrimaryKeyConstraint('CompanyId'),
    sa.UniqueConstraint('CompanyEmail'),
    sa.UniqueConstraint('CompanyLongName'),
    sa.UniqueConstraint('CompanyShortName'),
    sa.UniqueConstraint('PAUID'),
    sa.UniqueConstraint('RegistrationNumber'),
    sa.UniqueConstraint('TINNumber')
    )
    op.create_table('geosims_t_CraneUserLoginHistory',
    sa.Column('UserLoginHistoryId', sa.Integer(), nullable=False),
    sa.Column('HistLogUserId', sa.Integer(), nullable=False),
    sa.Column('LogStaffId', sa.Integer(), nullable=True),
    sa.Column('CraneCompanyId', sa.Integer(), nullable=True),
    sa.Column('LogCompanyAuthorisedUserId', sa.Integer(), nullable=True),
    sa.Column('LogAuthorisedUserName', sa.VARCHAR(length=100), nullable=True),
    sa.Column('LoginStatusId', sa.Integer(), nullable=True),
    sa.Column('UserOnlineStatus', sa.SMALLINT(), nullable=True),
    sa.Column('LogLoginDate', sa.DateTime(), nullable=True),
    sa.Column('LogLogoutDate', sa.DateTime(), nullable=True),
    sa.Column('UserLoginLogName', sa.VARCHAR(length=100), nullable=True),
    sa.Column('UserAcessLogName', sa.VARCHAR(length=100), nullable=True),
    sa.Column('Comments', sa.NVARCHAR(length=500), nullable=True),
    sa.ForeignKeyConstraint(['HistLogUserId'], ['geosims_t_CraneUser.CraneUserId'], ),
    sa.PrimaryKeyConstraint('UserLoginHistoryId')
    )
    op.create_table('geosims_t_RockSamples',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('StoreId', sa.VARCHAR(length=100), nullable=False),
    sa.Column('DateCollected', sa.DateTime(), nullable=True),
    sa.Column('DateReceived', sa.DateTime(), nullable=True),
    sa.Column('SampleBasin', sa.Enum('Edward-George', 'Semiliki', 'Pakwach', 'The Albertine Graben', 'Hoima Basin', 'Lake Kyoga Basin', 'Lake Wamala Basin', 'Kadam-Moroto Basin', name='basinsenum'), nullable=True),
    sa.Column('SamplePurpose', sa.Enum('Rock Minerals Analysis', 'Clay and Whole-rock Analysis', 'Rock Pyrolysis Analysis', 'Others', name='samplepurposeenum'), nullable=True),
    sa.Column('OtherSpecifiedSamplePurpose', sa.VARCHAR(length=100), nullable=True),
    sa.Column('SampleName', sa.VARCHAR(length=100), nullable=True),
    sa.Column('Latitude', sa.VARCHAR(length=100), nullable=True),
    sa.Column('Longitude', sa.VARCHAR(length=100), nullable=True),
    sa.Column('Operator', sa.VARCHAR(length=100), nullable=True),
    sa.Column('PetrographicDescription', sa.VARCHAR(length=500), nullable=True),
    sa.Column('CreatedById', sa.Integer(), nullable=False),
    sa.Column('DateCreated', sa.DateTime(), nullable=True),
    sa.Column('ModifiedOn', sa.DateTime(), nullable=True),
    sa.Column('ModifiedBy', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['CreatedById'], ['geosims_t_CraneUser.CraneUserId'], ),
    sa.ForeignKeyConstraint(['ModifiedBy'], ['geosims_t_CraneUser.CraneUserId'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('geosims_t_StratLithoUnit',
    sa.Column('StratLithoId', sa.Integer(), nullable=False),
    sa.Column('PAUID', sa.Integer(), nullable=True),
    sa.Column('StratLithoName', sa.NVARCHAR(length=100), nullable=False),
    sa.Column('LithoStratAlias', sa.NVARCHAR(length=100), nullable=True),
    sa.Column('IsReservoirUnitId', sa.Integer(), nullable=True),
    sa.Column('LithoStratAge', sa.Enum('Early Pliocene', 'Early Miocene', 'Early Pleistocene', 'Holocene', 'Late Miocene', 'Late Pleistocene', 'Middle Miocene', 'Precambrian', name='lithoageenum'), nullable=True),
    sa.Column('LithoStratDescriptionSoftcopyPath', sa.TEXT(), nullable=True),
    sa.Column('LithoStratDescriptionHyperlink', sa.TEXT(), nullable=True),
    sa.Column('LithoStratMapSoftCopyPath', sa.TEXT(), nullable=True),
    sa.Column('LithoStratMapHyperlink', sa.TEXT(), nullable=True),
    sa.Column('MapPortalLithoStratMapLink', sa.TEXT(), nullable=True),
    sa.Column('LithoStratFactsiteUrl', sa.TEXT(), nullable=True),
    sa.Column('Comments', sa.NVARCHAR(length=500), nullable=True),
    sa.Column('CreatedById', sa.Integer(), nullable=False),
    sa.Column('DateCreated', sa.DateTime(), nullable=True),
    sa.Column('ModifiedOn', sa.DateTime(), nullable=True),
    sa.Column('ModifiedBy', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['CreatedById'], ['geosims_t_CraneUser.CraneUserId'], ),
    sa.ForeignKeyConstraint(['ModifiedBy'], ['geosims_t_CraneUser.CraneUserId'], ),
    sa.PrimaryKeyConstraint('StratLithoId'),
    sa.UniqueConstraint('StratLithoName')
    )
    op.create_table('geosims_t_Wellbore',
    sa.Column('WellboreId', sa.Integer(), nullable=False),
    sa.Column('PAUID', sa.Integer(), nullable=True),
    sa.Column('InitialWellborePurpose', sa.Enum('Wildcat', 'Appraisal', 'Production', 'Injection', 'Observation', name='purposeenum'), nullable=True),
    sa.Column('WellboreType', sa.Enum('Exploration', 'Development', name='wellboretypeenum'), nullable=True),
    sa.Column('WellboreOfficialName', sa.NVARCHAR(length=255), nullable=True),
    sa.Column('WellboreLocalName', sa.NVARCHAR(length=255), nullable=False),
    sa.Column('WellboreAliasName', sa.NVARCHAR(length=255), nullable=False),
    sa.Column('DevelopmentAreaName', sa.Enum('KFDA', 'TDA', 'Others', name='developmentareaenum'), nullable=False),
    sa.Column('OtherDevelopmentArea', sa.NVARCHAR(length=100), nullable=True),
    sa.Column('Basin', sa.Enum('Edward-George', 'Semiliki', 'Pakwach', name='fluidsamplebasin'), nullable=True),
    sa.Column('WellboreSpudDate', sa.Date(), nullable=True),
    sa.Column('WellboreTypeId', sa.Integer(), nullable=True),
    sa.Column('WellborePurposeId', sa.Integer(), nullable=True),
    sa.Column('PurposeChangeDate', sa.DateTime(), nullable=True),
    sa.Column('ProspectId', sa.Integer(), nullable=True),
    sa.Column('Discovery', sa.NVARCHAR(length=255), nullable=True),
    sa.Column('WellboreContentId', sa.Integer(), nullable=True),
    sa.Column('LicenseOperatorCompanyId', sa.Integer(), nullable=True),
    sa.Column('DrillingContractorCompanyId', sa.Integer(), nullable=True),
    sa.Column('WellBoreRigName', sa.NVARCHAR(length=255), nullable=True),
    sa.Column('FormerExplAreaName', sa.NVARCHAR(length=255), nullable=True),
    sa.Column('SeismicLine', sa.NVARCHAR(length=255), nullable=True),
    sa.Column('RotaryTableElavation', sa.Float(), nullable=True),
    sa.Column('GroundLevelElavation', sa.Float(), nullable=True),
    sa.Column('TDMD', sa.Float(), nullable=True),
    sa.Column('TDTVD', sa.Float(), nullable=True),
    sa.Column('TDDate', sa.Date(), nullable=True),
    sa.Column('CoreContractorId', sa.Integer(), nullable=True),
    sa.Column('MDTDoneId', sa.Integer(), nullable=True),
    sa.Column('FETDoneId', sa.Integer(), nullable=True),
    sa.Column('WFTContractor', sa.Integer(), nullable=True),
    sa.Column('DSTDoneId', sa.Integer(), nullable=True),
    sa.Column('ManifoldFlowTestedId', sa.Integer(), nullable=True),
    sa.Column('DSTContractorId', sa.Integer(), nullable=True),
    sa.Column('HasPetrophysicalLogsId', sa.Integer(), nullable=True),
    sa.Column('PetrophysicalContractorId', sa.Integer(), nullable=True),
    sa.Column('TopBasementMD', sa.Float(), nullable=True),
    sa.Column('TopBasementTVD', sa.Float(), nullable=True),
    sa.Column('WellboreTestStatus', sa.TEXT(), nullable=True),
    sa.Column('PlannedWellboreCost', sa.DECIMAL(), nullable=True),
    sa.Column('ActualWellboreCost', sa.DECIMAL(), nullable=True),
    sa.Column('WellboreTestCost', sa.DECIMAL(), nullable=True),
    sa.Column('CompletionDate', sa.Date(), nullable=True),
    sa.Column('What3WordWellboreLocation', sa.TEXT(), nullable=True),
    sa.Column('Comments', sa.NVARCHAR(length=500), nullable=True),
    sa.Column('LocationPictureName', sa.TEXT(), nullable=True),
    sa.Column('LocationPicture', sa.TEXT(), nullable=True),
    sa.Column('LocationPictureSoftcopyPath', sa.TEXT(), nullable=True),
    sa.Column('LocationPictureHyperlink', sa.TEXT(), nullable=True),
    sa.Column('WellboreMapSoftcopyPath', sa.TEXT(), nullable=True),
    sa.Column('WellboreMapHyperlink', sa.TEXT(), nullable=True),
    sa.Column('MapPortalWellboreMapLink', sa.TEXT(), nullable=True),
    sa.Column('WellboreFactsiteUrl', sa.TEXT(), nullable=True),
    sa.Column('WellboreStatus', sa.Enum('Plugged and abandoned', 'Planned', 'Suspended', 'Withdrawn', 'In operation', 'In progress', name='statusenum'), nullable=True),
    sa.Column('CreatedById', sa.Integer(), nullable=False),
    sa.Column('DateCreated', sa.DateTime(), nullable=True),
    sa.Column('ModifiedOn', sa.DateTime(), nullable=True),
    sa.Column('ModifiedBy', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['CoreContractorId'], ['geosims_t_Company.CompanyId'], ),
    sa.ForeignKeyConstraint(['CreatedById'], ['geosims_t_CraneUser.CraneUserId'], ),
    sa.ForeignKeyConstraint(['DSTContractorId'], ['geosims_t_Company.CompanyId'], ),
    sa.ForeignKeyConstraint(['DrillingContractorCompanyId'], ['geosims_t_Company.CompanyId'], ),
    sa.ForeignKeyConstraint(['LicenseOperatorCompanyId'], ['geosims_t_Company.CompanyId'], ),
    sa.ForeignKeyConstraint(['ModifiedBy'], ['geosims_t_CraneUser.CraneUserId'], ),
    sa.ForeignKeyConstraint(['PetrophysicalContractorId'], ['geosims_t_Company.CompanyId'], ),
    sa.ForeignKeyConstraint(['ProspectId'], ['geosims_t_Company.CompanyId'], ),
    sa.PrimaryKeyConstraint('WellboreId'),
    sa.UniqueConstraint('PAUID'),
    sa.UniqueConstraint('WellboreOfficialName')
    )
    op.create_table('geosims_t_Cores',
    sa.Column('WellboreCoreId', sa.Integer(), nullable=False),
    sa.Column('WellborePAUID', sa.Integer(), nullable=False),
    sa.Column('WelboreCoreName', sa.NVARCHAR(length=255), nullable=False),
    sa.Column('CoreNumber', sa.NVARCHAR(length=255), nullable=True),
    sa.Column('CoreTypeName', sa.Enum('Slab', '1/2 Slab', '1/3 Slab', '2/3 Slab', 'Biscuit Slab', 'Full Diameter', 'SideWall Core', name='coretypeenum'), nullable=False),
    sa.Column('CoringDate', sa.Date(), nullable=True),
    sa.Column('WBCoringContractorId', sa.Integer(), nullable=True),
    sa.Column('CoreTopMD', sa.DECIMAL(), nullable=True),
    sa.Column('CoreBtmMD', sa.DECIMAL(), nullable=True),
    sa.Column('CoreTopTVD', sa.DECIMAL(), nullable=True),
    sa.Column('CoreBtmTVD', sa.DECIMAL(), nullable=True),
    sa.Column('CutLength', sa.String(length=100), nullable=True),
    sa.Column('CutLengthTVD', sa.String(length=100), nullable=True),
    sa.Column('RecoveredLength', sa.DECIMAL(), nullable=True),
    sa.Column('PercentageCoreRecovery', sa.Float(), nullable=True),
    sa.Column('CoreTopStratLithoId', sa.Integer(), nullable=True),
    sa.Column('CoreBottomStratLithoId', sa.Integer(), nullable=True),
    sa.Column('CorePictureSoftcopyPath', sa.TEXT(), nullable=True),
    sa.Column('CorePictureHyperlink', sa.TEXT(), nullable=True),
    sa.Column('PictureUploadDate', sa.DateTime(), nullable=True),
    sa.Column('CoreReportSoftcopyPath', sa.TEXT(), nullable=True),
    sa.Column('CoreReportHyperlink', sa.TEXT(), nullable=True),
    sa.Column('ReportUploadDate', sa.DateTime(), nullable=True),
    sa.Column('ReportFileFormat', sa.Enum('PDF', 'EXCEL', name='reportformatenum'), nullable=True),
    sa.Column('ReportFileSize', sa.DECIMAL(), nullable=True),
    sa.Column('ReportSecurityGrade', sa.Enum('Restricted', 'Confidential', 'Open', name='securitygradeenum'), nullable=True),
    sa.Column('ReportOpenDueDate', sa.DateTime(), nullable=True),
    sa.Column('ReportDocumentTitle', sa.NVARCHAR(length=100), nullable=True),
    sa.Column('ReportReceivedDate', sa.DateTime(), nullable=True),
    sa.Column('ReportDocumentDate', sa.DateTime(), nullable=True),
    sa.Column('ReportDocumentName', sa.NVARCHAR(length=100), nullable=True),
    sa.Column('StoreIdentifier', sa.NVARCHAR(length=100), nullable=True),
    sa.Column('AnalysisReportDetails', sa.NVARCHAR(length=500), nullable=True),
    sa.Column('Comments', sa.NVARCHAR(length=500), nullable=True),
    sa.Column('CreatedById', sa.Integer(), nullable=False),
    sa.Column('DateCreated', sa.DateTime(), nullable=True),
    sa.Column('ModifiedOn', sa.DateTime(), nullable=True),
    sa.Column('ModifiedBy', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['CoreBottomStratLithoId'], ['geosims_t_StratLithoUnit.StratLithoId'], ),
    sa.ForeignKeyConstraint(['CoreTopStratLithoId'], ['geosims_t_StratLithoUnit.StratLithoId'], ),
    sa.ForeignKeyConstraint(['CreatedById'], ['geosims_t_CraneUser.CraneUserId'], ),
    sa.ForeignKeyConstraint(['ModifiedBy'], ['geosims_t_CraneUser.CraneUserId'], ),
    sa.ForeignKeyConstraint(['WBCoringContractorId'], ['geosims_t_Company.CompanyId'], ),
    sa.ForeignKeyConstraint(['WelboreCoreName'], ['geosims_t_Wellbore.WellboreOfficialName'], ),
    sa.ForeignKeyConstraint(['WellborePAUID'], ['geosims_t_Wellbore.PAUID'], ),
    sa.PrimaryKeyConstraint('WellboreCoreId'),
    sa.UniqueConstraint('CoreNumber')
    )
    op.create_table('geosims_t_Cuttings',
    sa.Column('SampleId', sa.Integer(), nullable=False),
    sa.Column('WellboreId', sa.Integer(), nullable=True),
    sa.Column('SampleBoxNumber', sa.VARCHAR(length=100), nullable=True),
    sa.Column('CuttingCategory', sa.Enum('Washed_Dried', 'Washed_Wet', 'Wet_Unwashed', 'Dry_Unwashed', name='cuttingscategoryenum'), nullable=False),
    sa.Column('SampleType', sa.VARCHAR(length=100), nullable=True),
    sa.Column('TopDepth', sa.Float(), nullable=True),
    sa.Column('BottomDepth', sa.Float(), nullable=True),
    sa.Column('StoreIdentifier', sa.VARCHAR(length=100), nullable=True),
    sa.Column('Operator', sa.VARCHAR(length=100), nullable=True),
    sa.Column('SamplingCompany', sa.NVARCHAR(length=255), nullable=True),
    sa.Column('SamplingDate', sa.DateTime(), nullable=True),
    sa.Column('SampleInterval', sa.VARCHAR(length=100), nullable=True),
    sa.Column('DateReceived', sa.DateTime(), nullable=True),
    sa.Column('OtherDescription', sa.VARCHAR(length=500), nullable=True),
    sa.Column('CreatedById', sa.Integer(), nullable=False),
    sa.Column('DateCreated', sa.DateTime(), nullable=True),
    sa.Column('ModifiedOn', sa.DateTime(), nullable=True),
    sa.Column('ModifiedBy', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['CreatedById'], ['geosims_t_CraneUser.CraneUserId'], ),
    sa.ForeignKeyConstraint(['ModifiedBy'], ['geosims_t_CraneUser.CraneUserId'], ),
    sa.ForeignKeyConstraint(['SamplingCompany'], ['geosims_t_Company.CompanyLongName'], ),
    sa.ForeignKeyConstraint(['WellboreId'], ['geosims_t_Wellbore.WellboreId'], ),
    sa.PrimaryKeyConstraint('SampleId')
    )
    op.create_table('geosims_t_FluidSamples',
    sa.Column('SampleId', sa.Integer(), nullable=False),
    sa.Column('WellboreId', sa.Integer(), nullable=True),
    sa.Column('SamplingActivity', sa.VARCHAR(length=100), nullable=True),
    sa.Column('FluidCategory', sa.Enum('Oil', 'Gas', 'Water', name='fluidcategoryenum'), nullable=False),
    sa.Column('SampleType', sa.VARCHAR(length=100), nullable=True),
    sa.Column('SampleVolume', sa.VARCHAR(length=100), nullable=True),
    sa.Column('SampleBasin', sa.Enum('Edward-George', 'Semiliki', 'Pakwach', 'The Albertine Graben', 'Hoima Basin', 'Lake Kyoga Basin', 'Lake Wamala Basin', 'Kadam-Moroto Basin', name='fluidsamplebasin'), nullable=True),
    sa.Column('DepthObtained', sa.Float(), nullable=True),
    sa.Column('DateCollected', sa.DateTime(), nullable=True),
    sa.Column('DateReceived', sa.DateTime(), nullable=True),
    sa.Column('SamplingCompany', sa.Integer(), nullable=True),
    sa.Column('SamplePurpose', sa.Enum('Crude Oil Analysis', 'PVT Analysis', 'Formation Water Analysis', 'Natural Gas Analysis', 'Others', name='fluidsamplepurposeenum'), nullable=True),
    sa.Column('OtherSpecifiedSamplePurpose', sa.VARCHAR(length=100), nullable=True),
    sa.Column('CreatedById', sa.Integer(), nullable=False),
    sa.Column('DateCreated', sa.DateTime(), nullable=True),
    sa.Column('ModifiedOn', sa.DateTime(), nullable=True),
    sa.Column('ModifiedBy', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['CreatedById'], ['geosims_t_CraneUser.CraneUserId'], ),
    sa.ForeignKeyConstraint(['ModifiedBy'], ['geosims_t_CraneUser.CraneUserId'], ),
    sa.ForeignKeyConstraint(['SamplingCompany'], ['geosims_t_Company.CompanyId'], ),
    sa.ForeignKeyConstraint(['WellboreId'], ['geosims_t_Wellbore.WellboreId'], ),
    sa.PrimaryKeyConstraint('SampleId')
    )
    op.create_table('geosims_rt_Files',
    sa.Column('FileId', sa.Integer(), nullable=False),
    sa.Column('CoresId', sa.Integer(), nullable=True),
    sa.Column('FluidSamplesId', sa.Integer(), nullable=True),
    sa.Column('RockSamplesId', sa.Integer(), nullable=True),
    sa.Column('CuttingsId', sa.Integer(), nullable=True),
    sa.Column('ReportType', sa.Enum('Cores', 'Fluid_Samples', 'Rock_Samples', name='reporttypeenum'), nullable=True),
    sa.Column('ReportPath', sa.VARCHAR(length=500), nullable=True),
    sa.Column('PhotographPath', sa.VARCHAR(length=500), nullable=True),
    sa.Column('CreatedById', sa.Integer(), nullable=False),
    sa.Column('DateCreated', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['CoresId'], ['geosims_t_Cores.WellboreCoreId'], ),
    sa.ForeignKeyConstraint(['CreatedById'], ['geosims_t_CraneUser.CraneUserId'], ),
    sa.ForeignKeyConstraint(['CuttingsId'], ['geosims_t_Cuttings.SampleId'], ),
    sa.ForeignKeyConstraint(['FluidSamplesId'], ['geosims_t_FluidSamples.SampleId'], ),
    sa.ForeignKeyConstraint(['RockSamplesId'], ['geosims_t_RockSamples.id'], ),
    sa.PrimaryKeyConstraint('FileId')
    )
    op.create_table('geosims_t_CoreCatalog',
    sa.Column('CoreCatalogId', sa.Integer(), nullable=False),
    sa.Column('WellboreCoreId', sa.Integer(), nullable=False),
    sa.Column('StoreIdentifier', sa.NVARCHAR(length=100), nullable=True),
    sa.Column('CatalogCoreFromDepth', sa.DECIMAL(), nullable=True),
    sa.Column('CatalogCoreToDepth', sa.DECIMAL(), nullable=True),
    sa.Column('WasAnalysedId', sa.Integer(), nullable=True),
    sa.Column('TopStratLithoId', sa.Integer(), nullable=True),
    sa.Column('BottomStratLithoId', sa.Integer(), nullable=True),
    sa.Column('CatalogueCorePictureName', sa.TEXT(), nullable=True),
    sa.Column('CataloguePictureSoftcopyPath', sa.TEXT(), nullable=True),
    sa.Column('CataloguePictureHyperlink', sa.TEXT(), nullable=True),
    sa.Column('CatPictureUploadDate', sa.DateTime(), nullable=True),
    sa.Column('CatalogueReportSoftcopyPath', sa.TEXT(), nullable=True),
    sa.Column('CatalogueReportHyperlink', sa.TEXT(), nullable=True),
    sa.Column('CatReportUploadDate', sa.DateTime(), nullable=True),
    sa.Column('CatalogReportFileSize', sa.DECIMAL(), nullable=True),
    sa.Column('CoreCatalogName', sa.NVARCHAR(length=100), nullable=False),
    sa.Column('Comments', sa.NVARCHAR(length=500), nullable=True),
    sa.Column('CreatedById', sa.Integer(), nullable=False),
    sa.Column('DateCreated', sa.DateTime(), nullable=True),
    sa.Column('ModifiedOn', sa.DateTime(), nullable=True),
    sa.Column('ModifiedBy', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['BottomStratLithoId'], ['geosims_t_StratLithoUnit.StratLithoId'], ),
    sa.ForeignKeyConstraint(['CreatedById'], ['geosims_t_CraneUser.CraneUserId'], ),
    sa.ForeignKeyConstraint(['ModifiedBy'], ['geosims_t_CraneUser.CraneUserId'], ),
    sa.ForeignKeyConstraint(['TopStratLithoId'], ['geosims_t_StratLithoUnit.StratLithoId'], ),
    sa.ForeignKeyConstraint(['WellboreCoreId'], ['geosims_t_Cores.WellboreCoreId'], ),
    sa.PrimaryKeyConstraint('CoreCatalogId'),
    sa.UniqueConstraint('CoreCatalogName')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('geosims_t_CoreCatalog')
    op.drop_table('geosims_rt_Files')
    op.drop_table('geosims_t_FluidSamples')
    op.drop_table('geosims_t_Cuttings')
    op.drop_table('geosims_t_Cores')
    op.drop_table('geosims_t_Wellbore')
    op.drop_table('geosims_t_StratLithoUnit')
    op.drop_table('geosims_t_RockSamples')
    op.drop_table('geosims_t_CraneUserLoginHistory')
    op.drop_table('geosims_t_Company')
    op.drop_table('geosims_rt_PasswordReset')
    op.drop_table('geosims_t_CraneUser')
    op.drop_table('revoked_tokens')
    op.drop_table('geosims_rt_CraneWebSecurityLevel')
    # ### end Alembic commands ###
