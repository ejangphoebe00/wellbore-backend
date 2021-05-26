"""empty message

Revision ID: b574a763d0d1
Revises: 384df507834c
Create Date: 2021-05-27 02:10:47.266221

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b574a763d0d1'
down_revision = '384df507834c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('crane.rt_CatalogSecurityFlag',
    sa.Column('CatalogSecurityFlag_id', sa.Integer(), nullable=False),
    sa.Column('CatalogSecurityFlagName', sa.NVARCHAR(length=255), nullable=True),
    sa.Column('SortOrder', sa.Integer(), nullable=True),
    sa.Column('Comments', sa.NVARCHAR(length=500), nullable=True),
    sa.Column('ModifiedOn', sa.TIMESTAMP(), nullable=True),
    sa.Column('ModifiedBy', sa.NVARCHAR(length=255), nullable=True),
    sa.PrimaryKeyConstraint('CatalogSecurityFlag_id')
    )
    op.create_table('crane.rt_CoreType',
    sa.Column('CoreType_id', sa.Integer(), nullable=False),
    sa.Column('CoreTypeName', sa.NVARCHAR(length=255), nullable=True),
    sa.Column('SortOrder', sa.Integer(), nullable=True),
    sa.Column('Comments', sa.NVARCHAR(length=500), nullable=True),
    sa.Column('ModifiedOn', sa.TIMESTAMP(), nullable=True),
    sa.Column('ModifiedBy', sa.NVARCHAR(length=255), nullable=True),
    sa.PrimaryKeyConstraint('CoreType_id')
    )
    op.create_table('crane.rt_CraneWebSecurityLevel',
    sa.Column('WebSecurityLevel_id', sa.Integer(), nullable=False),
    sa.Column('WebSecurityLevelName', sa.NVARCHAR(length=255), nullable=True),
    sa.Column('WebSecurityLevelDescription', sa.NVARCHAR(length=255), nullable=True),
    sa.Column('WebSecurityLevelAbbreviation', sa.NVARCHAR(length=255), nullable=True),
    sa.Column('Comments', sa.NVARCHAR(length=500), nullable=True),
    sa.Column('ModifiedOn', sa.TIMESTAMP(), nullable=True),
    sa.Column('ModifiedBy', sa.NVARCHAR(length=255), nullable=True),
    sa.PrimaryKeyConstraint('WebSecurityLevel_id')
    )
    op.create_table('crane.rt_FileFormat',
    sa.Column('FileFormat_id', sa.Integer(), nullable=False),
    sa.Column('FileFormatName', sa.NVARCHAR(length=255), nullable=True),
    sa.Column('SortOrder', sa.Integer(), nullable=True),
    sa.Column('Comments', sa.NVARCHAR(length=500), nullable=True),
    sa.Column('ModifiedOn', sa.TIMESTAMP(), nullable=True),
    sa.Column('ModifiedBy', sa.NVARCHAR(length=255), nullable=True),
    sa.PrimaryKeyConstraint('FileFormat_id')
    )
    op.create_table('crane.rt_FileSecurityGrade',
    sa.Column('FileSecurityGrade_id', sa.Integer(), nullable=False),
    sa.Column('FileSecurityGradeName', sa.NVARCHAR(length=255), nullable=True),
    sa.Column('SortOrder', sa.Integer(), nullable=True),
    sa.Column('Comments', sa.NVARCHAR(length=500), nullable=True),
    sa.Column('ModifiedOn', sa.TIMESTAMP(), nullable=True),
    sa.Column('ModifiedBy', sa.NVARCHAR(length=255), nullable=True),
    sa.PrimaryKeyConstraint('FileSecurityGrade_id')
    )
    op.create_table('crane.t_Company',
    sa.Column('Company_id', sa.Integer(), nullable=False),
    sa.Column('PAUID', sa.NVARCHAR(length=255), nullable=False),
    sa.Column('CompanyLongName', sa.NVARCHAR(length=255), nullable=True),
    sa.Column('CompanyShortName', sa.NVARCHAR(length=255), nullable=False),
    sa.Column('NSD_Number', sa.NVARCHAR(length=255), nullable=False),
    sa.Column('CompanyCategory_id', sa.Integer(), nullable=True),
    sa.Column('CountryOfOrigin_id', sa.Integer(), nullable=True),
    sa.Column('CountryOfRegistration_id', sa.Integer(), nullable=True),
    sa.Column('RegistrationNumber', sa.NVARCHAR(length=255), nullable=False),
    sa.Column('TINNumber', sa.NVARCHAR(length=255), nullable=False),
    sa.Column('CompanyTelephone', sa.NVARCHAR(length=255), nullable=True),
    sa.Column('CompanyEmail', sa.NVARCHAR(length=255), nullable=True),
    sa.Column('CompanyWebsite', sa.TEXT(), nullable=True),
    sa.Column('CompanyEntityType_id', sa.Integer(), nullable=True),
    sa.Column('CompanyEntitySubType_id', sa.Integer(), nullable=True),
    sa.Column('CompanyMajorActivity_id', sa.Integer(), nullable=True),
    sa.Column('CompanyActivityDivision_id', sa.Integer(), nullable=True),
    sa.Column('CompanyActivityDivisionClass_id', sa.Integer(), nullable=True),
    sa.Column('CompanyActivityDivisionClassCategory_id', sa.Integer(), nullable=True),
    sa.Column('BusinessNatureDescription', sa.TEXT(), nullable=True),
    sa.Column('CompanyPostalAddress', sa.NVARCHAR(length=255), nullable=True),
    sa.Column('CompanyPhysicalAddress', sa.NVARCHAR(length=255), nullable=True),
    sa.Column('NSDQualificationDate', sa.DateTime(), nullable=True),
    sa.Column('NSDQualificationYear', sa.String(length=10), nullable=True),
    sa.Column('CompanyOtherEmails', sa.NVARCHAR(length=100), nullable=True),
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
    sa.Column('RegistrationStatus_id', sa.Integer(), nullable=True),
    sa.Column('ClassifyAsUgandan_id', sa.Integer(), nullable=True),
    sa.Column('Comments', sa.TEXT(), nullable=True),
    sa.Column('PrimaryCompanyKind_id', sa.Integer(), nullable=True),
    sa.Column('SecondaryCompanyKind_id', sa.Integer(), nullable=True),
    sa.Column('OtherCompanyKind_id', sa.Integer(), nullable=True),
    sa.Column('CompanyGroup_id', sa.Integer(), nullable=True),
    sa.Column('CompanyMobile', sa.NVARCHAR(length=55), nullable=True),
    sa.Column('CompanyFax', sa.NVARCHAR(length=55), nullable=True),
    sa.Column('ContactEntityFax', sa.NVARCHAR(length=55), nullable=True),
    sa.Column('NSD_FromDate', sa.Date(), nullable=True),
    sa.Column('NSD_ToDate', sa.Date(), nullable=True),
    sa.Column('ImportedFromNSD', sa.SMALLINT(), nullable=True),
    sa.Column('ImportedDate', sa.DateTime(), nullable=True),
    sa.Column('ExportedDate', sa.DateTime(), nullable=True),
    sa.Column('ExportedToNogtr', sa.SMALLINT(), nullable=True),
    sa.Column('CreatedBy', sa.Integer(), nullable=True),
    sa.Column('DateCreated', sa.DateTime(), nullable=True),
    sa.Column('ModifiedOn', sa.DateTime(), nullable=True),
    sa.Column('ModifiedBy', sa.NVARCHAR(length=100), nullable=True),
    sa.Column('RecordChangeStamp', sa.VARBINARY(length='MAX'), nullable=True),
    sa.Column('PreviousLegalName', sa.NVARCHAR(length=100), nullable=True),
    sa.PrimaryKeyConstraint('Company_id')
    )
    op.create_table('crane.t_CraneUserLoginHistory',
    sa.Column('UserLoginHistory_id', sa.Integer(), nullable=False),
    sa.Column('HistLogUser_id', sa.Integer(), nullable=True),
    sa.Column('LogStaff_id', sa.Integer(), nullable=True),
    sa.Column('CraneCompany_id', sa.Integer(), nullable=True),
    sa.Column('LogCompanyAuthorisedUser_id', sa.Integer(), nullable=True),
    sa.Column('LogAuthorisedUserName', sa.TEXT(), nullable=True),
    sa.Column('LoginStatus_id', sa.Integer(), nullable=True),
    sa.Column('UserOnlineStatus', sa.SMALLINT(), nullable=True),
    sa.Column('LogLoginDate', sa.DateTime(), nullable=True),
    sa.Column('LogLogoutDate', sa.DateTime(), nullable=True),
    sa.Column('UserLoginLogName', sa.TEXT(), nullable=True),
    sa.Column('UserAcessLogName', sa.TEXT(), nullable=True),
    sa.Column('Comments', sa.NVARCHAR(length=500), nullable=True),
    sa.PrimaryKeyConstraint('UserLoginHistory_id')
    )
    op.create_table('crane.t_StratLithoUnit',
    sa.Column('StratLitho_id', sa.Integer(), nullable=False),
    sa.Column('PAUID', sa.Integer(), nullable=True),
    sa.Column('StratLithoName', sa.NVARCHAR(length=100), nullable=True),
    sa.Column('ReserviorUnit', sa.SMALLINT(), nullable=True),
    sa.Column('LithoStratAlias', sa.NVARCHAR(length=100), nullable=True),
    sa.Column('IsReservoirUnit_id', sa.Integer(), nullable=True),
    sa.Column('LithoStratAge_id', sa.Integer(), nullable=True),
    sa.Column('LithoStratDescriptionSoftcopyPath', sa.TEXT(), nullable=True),
    sa.Column('LithoStratDescriptionHyperlink', sa.TEXT(), nullable=True),
    sa.Column('LithoStratMapSoftCopyPath', sa.TEXT(), nullable=True),
    sa.Column('LithoStratMapHyperlink', sa.TEXT(), nullable=True),
    sa.Column('MapPortalLithoStratMapLink', sa.TEXT(), nullable=True),
    sa.Column('LithoStratFactsiteUrl', sa.TEXT(), nullable=True),
    sa.Column('Comments', sa.NVARCHAR(length=500), nullable=True),
    sa.Column('CreatedBy_id', sa.Integer(), nullable=True),
    sa.Column('DateCreated', sa.DateTime(), nullable=True),
    sa.Column('ModifiedOn', sa.DateTime(), nullable=True),
    sa.Column('ModifiedBy', sa.NVARCHAR(length=255), nullable=True),
    sa.PrimaryKeyConstraint('StratLitho_id')
    )
    op.create_table('crane.t_Wellbore',
    sa.Column('Wellbore_id', sa.Integer(), nullable=False),
    sa.Column('PAUID', sa.Integer(), nullable=True),
    sa.Column('WellboreOfficialName', sa.NVARCHAR(length=255), nullable=True),
    sa.Column('WellboreLocalName', sa.NVARCHAR(length=255), nullable=False),
    sa.Column('WellboreAliasName', sa.NVARCHAR(length=255), nullable=False),
    sa.Column('WellboreSpudDate', sa.Date(), nullable=True),
    sa.Column('SpudYear', sa.String(length=50), nullable=True),
    sa.Column('WellboreType_id', sa.Integer(), nullable=True),
    sa.Column('InitialWellborePurpose_id', sa.Integer(), nullable=True),
    sa.Column('WellborePurpose_id', sa.Integer(), nullable=True),
    sa.Column('PurposeChangeDate', sa.DateTime(), nullable=True),
    sa.Column('Well_id', sa.Integer(), nullable=True),
    sa.Column('Prospect_id', sa.Integer(), nullable=True),
    sa.Column('Discovery_id', sa.Integer(), nullable=True),
    sa.Column('WellboreContent_id', sa.Integer(), nullable=True),
    sa.Column('WellboreStatus_id', sa.Integer(), nullable=True),
    sa.Column('WellboreResponsibleLicence_id', sa.Integer(), nullable=True),
    sa.Column('LicenseOperatorCompany_id', sa.Integer(), nullable=True),
    sa.Column('DrillingContractorCompany_id', sa.Integer(), nullable=True),
    sa.Column('WellBoreRigName', sa.NVARCHAR(length=255), nullable=True),
    sa.Column('Basin_id', sa.Integer(), nullable=True),
    sa.Column('FormerExplAreaName', sa.NVARCHAR(length=255), nullable=True),
    sa.Column('SeismicLine', sa.NVARCHAR(length=255), nullable=True),
    sa.Column('RotaryTableElavation', sa.Float(), nullable=True),
    sa.Column('GroundLevelElavation', sa.Float(), nullable=True),
    sa.Column('TD_MD', sa.Float(), nullable=True),
    sa.Column('TD_TVD', sa.Float(), nullable=True),
    sa.Column('TD_Date', sa.Date(), nullable=True),
    sa.Column('WellboreCore_id', sa.Integer(), nullable=True),
    sa.Column('CoreContractor_id', sa.Integer(), nullable=True),
    sa.Column('RCI_Taken_id', sa.Integer(), nullable=True),
    sa.Column('MDT_Done_id', sa.Integer(), nullable=True),
    sa.Column('FET_Done_id', sa.Integer(), nullable=True),
    sa.Column('WFTContractor', sa.Integer(), nullable=True),
    sa.Column('DST_Done_id', sa.Integer(), nullable=True),
    sa.Column('ManifoldFlowTested_id', sa.Integer(), nullable=True),
    sa.Column('DST_Contractor_id', sa.Integer(), nullable=True),
    sa.Column('HasPetrophysicalLogs_id', sa.Integer(), nullable=True),
    sa.Column('PetrophysicalContractor_id', sa.Integer(), nullable=True),
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
    sa.Column('CreatedBy_id', sa.Integer(), nullable=True),
    sa.Column('DateCreated', sa.DateTime(), nullable=True),
    sa.Column('ModifiedOn', sa.DateTime(), nullable=True),
    sa.Column('ModifiedBy', sa.NVARCHAR(length=255), nullable=True),
    sa.PrimaryKeyConstraint('Wellbore_id')
    )
    op.create_table('crane.t_WellboreCore',
    sa.Column('WellboreCore_id', sa.Integer(), nullable=False),
    sa.Column('Wellbore_id', sa.Integer(), nullable=True),
    sa.Column('CoreNumber', sa.NVARCHAR(length=255), nullable=True),
    sa.Column('CoringDate', sa.Date(), nullable=True),
    sa.Column('WBCoringContractor_id', sa.Integer(), nullable=True),
    sa.Column('CoreTopMDRT', sa.DECIMAL(), nullable=True),
    sa.Column('CoreBtmMDRT', sa.DECIMAL(), nullable=True),
    sa.Column('CoreTopTVD', sa.DECIMAL(), nullable=True),
    sa.Column('CoreBtmTVD', sa.DECIMAL(), nullable=True),
    sa.Column('CutLength', sa.String(length=100), nullable=True),
    sa.Column('CutLengthTVD', sa.String(length=100), nullable=True),
    sa.Column('RecoveredLength', sa.DECIMAL(), nullable=True),
    sa.Column('CoreRecovery', sa.String(length=100), nullable=True),
    sa.Column('CoreTopStratLitho_id', sa.Integer(), nullable=True),
    sa.Column('CoreBottomStratLitho_id', sa.Integer(), nullable=True),
    sa.Column('CorePictureSoftcopyPath', sa.TEXT(), nullable=True),
    sa.Column('CorePictureHyperlink', sa.TEXT(), nullable=True),
    sa.Column('PictureUploadDate', sa.DateTime(), nullable=True),
    sa.Column('CoreReportSoftcopyPath', sa.TEXT(), nullable=True),
    sa.Column('CoreReportHyperlink', sa.TEXT(), nullable=True),
    sa.Column('ReportUploadDate', sa.DateTime(), nullable=True),
    sa.Column('ReportFormat_id', sa.Integer(), nullable=True),
    sa.Column('ReportFileSize', sa.DECIMAL(), nullable=True),
    sa.Column('CoreReportSecurityGrade_id', sa.Integer(), nullable=True),
    sa.Column('ReportOpenDueDate', sa.DateTime(), nullable=True),
    sa.Column('ReportDocumentTitle', sa.NVARCHAR(length=100), nullable=True),
    sa.Column('ReportReceivedDate', sa.DateTime(), nullable=True),
    sa.Column('ReportDocumentDate', sa.DateTime(), nullable=True),
    sa.Column('ReportDocumentName', sa.NVARCHAR(length=100), nullable=True),
    sa.Column('WellboreCoreName', sa.NVARCHAR(length=100), nullable=True),
    sa.Column('Comments', sa.NVARCHAR(length=500), nullable=True),
    sa.Column('CreatedBy_id', sa.Integer(), nullable=True),
    sa.Column('DateCreated', sa.DateTime(), nullable=True),
    sa.Column('ModifiedOn', sa.DateTime(), nullable=True),
    sa.Column('ModifiedBy', sa.NVARCHAR(length=255), nullable=True),
    sa.ForeignKeyConstraint(['Wellbore_id'], ['crane.t_Wellbore.Wellbore_id'], ),
    sa.PrimaryKeyConstraint('WellboreCore_id')
    )
    op.create_table('crane.t_CoreCatalog',
    sa.Column('CoreCatalog_id', sa.Integer(), nullable=False),
    sa.Column('WellboreCore_id', sa.Integer(), nullable=True),
    sa.Column('CoreType', sa.Integer(), nullable=True),
    sa.Column('StoreIdentifier', sa.NVARCHAR(length=100), nullable=True),
    sa.Column('CatalogCoreFromDepth', sa.DECIMAL(), nullable=True),
    sa.Column('CatalogCoreToDepth', sa.DECIMAL(), nullable=True),
    sa.Column('CoreCatalogSecurityFlag_id', sa.Integer(), nullable=True),
    sa.Column('WasAnalysed_id', sa.Integer(), nullable=True),
    sa.Column('TopStratLitho_id', sa.Integer(), nullable=True),
    sa.Column('BottomStratLitho_id', sa.Integer(), nullable=True),
    sa.Column('CatalogueCorePictureName', sa.TEXT(), nullable=True),
    sa.Column('CataloguePictureSoftcopyPath', sa.TEXT(), nullable=True),
    sa.Column('CataloguePictureHyperlink', sa.TEXT(), nullable=True),
    sa.Column('CatPictureUploadDate', sa.DateTime(), nullable=True),
    sa.Column('CatalogueReportSoftcopyPath', sa.TEXT(), nullable=True),
    sa.Column('CatalogueReportHyperlink', sa.TEXT(), nullable=True),
    sa.Column('CatReportUploadDate', sa.DateTime(), nullable=True),
    sa.Column('CatalogReportFormat_id', sa.Integer(), nullable=True),
    sa.Column('CatalogReportFileSize', sa.DECIMAL(), nullable=True),
    sa.Column('CatalogReportSecurityGrade_id', sa.Integer(), nullable=True),
    sa.Column('CoreCatalogName', sa.NVARCHAR(length=100), nullable=True),
    sa.Column('Comments', sa.NVARCHAR(length=500), nullable=True),
    sa.Column('CreatedBy_id', sa.Integer(), nullable=True),
    sa.Column('DateCreated', sa.DateTime(), nullable=True),
    sa.Column('ModifiedOn', sa.DateTime(), nullable=True),
    sa.Column('ModifiedBy', sa.NVARCHAR(length=255), nullable=True),
    sa.ForeignKeyConstraint(['WellboreCore_id'], ['crane.t_WellboreCore.WellboreCore_id'], ),
    sa.PrimaryKeyConstraint('CoreCatalog_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('crane.t_CoreCatalog')
    op.drop_table('crane.t_WellboreCore')
    op.drop_table('crane.t_Wellbore')
    op.drop_table('crane.t_StratLithoUnit')
    op.drop_table('crane.t_CraneUserLoginHistory')
    op.drop_table('crane.t_Company')
    op.drop_table('crane.rt_FileSecurityGrade')
    op.drop_table('crane.rt_FileFormat')
    op.drop_table('crane.rt_CraneWebSecurityLevel')
    op.drop_table('crane.rt_CoreType')
    op.drop_table('crane.rt_CatalogSecurityFlag')
    # ### end Alembic commands ###
