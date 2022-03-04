from .. import db
from .CraneUser import CraneUser, DeleteStatusEnum
from .Company import Company
import enum

class DevelopmentAreaEnum(enum.Enum):
    KFDA = "King Fisher Development Area"
    TDA = "Telinga Development Area"
    Others = "Others"

class PurposeEnum(enum.Enum):
    Wildcat = "Wildcat"
    Appraisal = 'Appraisal'
    Production = 'Production'
    Injection = 'Injection'
    Observation = 'Observation'

class WellboreTypeEnum(enum.Enum):
    Exploration = 'Exploration'
    Development = 'Development'

class StatusEnum(enum.Enum):
    Plugged_and_abandoned = 'Plugged and abandoned'
    Planned = 'Planned'
    Suspended = 'Suspended'
    Withdrawn = 'Withdrawn'
    In_operation = 'In operation'
    In_progress = 'In progress'

class FluidSampleBasin(enum.Enum):
    Edward = "Edward-George"
    Semiliki = "Semiliki"
    Pakwach = "Pakwach"
    Albertine = "The Albertine Graben"
    Hoima = "Hoima Basin"
    Kyoga = "Lake Kyoga Basin"
    Wamala = "Lake Wamala Basin"
    Kadam = "Kadam-Moroto Basin"


class Wellbore(db.Model):
    __tablename__ = 'geosims_t_Wellbore'
    WellboreId = db.Column(db.Integer,primary_key=True)
    PAUID = db.Column(db.Integer, unique=True)
    InitialWellborePurpose = db.Column(db.Enum(PurposeEnum))
    WellboreType = db.Column(db.Enum(WellboreTypeEnum))
    WellboreOfficialName = db.Column(db.NVARCHAR(255),nullable=True, unique=True)
    WellboreLocalName = db.Column(db.NVARCHAR(255),nullable=False)
    WellboreAliasName = db.Column(db.NVARCHAR(255),nullable=False)
    DevelopmentAreaName = db.Column(db.Enum(DevelopmentAreaEnum), default="King Fisher Development Area",nullable=False)
    OtherDevelopmentArea = db.Column(db.NVARCHAR(100))
    Basin = db.Column(db.Enum(FluidSampleBasin,
             values_callable=lambda enum: [str(e.value) for e in enum]))
    WellboreSpudDate = db.Column(db.Date)
    # SpudYear = db.Column(db.String(50))
    WellboreTypeId = db.Column(db.Integer)
    WellborePurposeId = db.Column(db.Integer)
    PurposeChangeDate = db.Column(db.DateTime)
    # WellId = db.Column(db.Integer)
    ProspectId = db.Column(db.Integer, db.ForeignKey(Company.CompanyId),nullable=True)
    Discovery = db.Column(db.NVARCHAR(255))
    WellboreContentId = db.Column(db.Integer)
    # WellboreResponsibleLicenceId = db.Column(db.Integer)
    LicenseOperatorCompanyId = db.Column(db.Integer, db.ForeignKey(Company.CompanyId),nullable=True)
    DrillingContractorCompanyId = db.Column(db.Integer, db.ForeignKey(Company.CompanyId),nullable=True)
    WellBoreRigName = db.Column(db.NVARCHAR(255))
    FormerExplAreaName = db.Column(db.NVARCHAR(255))
    SeismicLine = db.Column(db.NVARCHAR(255))
    RotaryTableElavation = db.Column(db.Float)
    GroundLevelElavation = db.Column(db.Float)
    TDMD = db.Column(db.Float)
    TDTVD = db.Column(db.Float)
    TDDate = db.Column(db.Date)
    # WellboreCoreId = db.Column(db.Integer)
    CoreContractorId = db.Column(db.Integer, db.ForeignKey(Company.CompanyId),nullable=True)
    # RCI_TakenId = db.Column(db.Integer)
    MDTDoneId = db.Column(db.Integer)
    FETDoneId = db.Column(db.Integer)
    WFTContractor = db.Column(db.Integer)
    DSTDoneId = db.Column(db.Integer)
    ManifoldFlowTestedId = db.Column(db.Integer)
    DSTContractorId = db.Column(db.Integer, db.ForeignKey(Company.CompanyId),nullable=True)
    HasPetrophysicalLogsId = db.Column(db.Integer)
    PetrophysicalContractorId = db.Column(db.Integer, db.ForeignKey(Company.CompanyId),nullable=True)
    TopBasementMD = db.Column(db.Float)
    TopBasementTVD = db.Column(db.Float)
    WellboreTestStatus = db.Column(db.TEXT)
    PlannedWellboreCost = db.Column(db.DECIMAL)
    ActualWellboreCost = db.Column(db.DECIMAL)
    WellboreTestCost = db.Column(db.DECIMAL)
    CompletionDate = db.Column(db.Date)
    What3WordWellboreLocation = db.Column(db.TEXT)
    Comments = db.Column(db.NVARCHAR(500))
    LocationPictureName = db.Column(db.TEXT)
    LocationPicture = db.Column(db.TEXT)
    LocationPictureSoftcopyPath = db.Column(db.TEXT)
    LocationPictureHyperlink = db.Column(db.TEXT)
    WellboreMapSoftcopyPath = db.Column(db.TEXT)
    WellboreMapHyperlink = db.Column(db.TEXT)
    MapPortalWellboreMapLink = db.Column(db.TEXT)
    WellboreFactsiteUrl = db.Column(db.TEXT)
    WellboreStatus = db.Column(db.Enum(StatusEnum,
             values_callable=lambda enum: [str(e.value) for e in enum]))
    CreatedById = db.Column(db.Integer, db.ForeignKey(CraneUser.CraneUserId),nullable=False)
    DateCreated = db.Column(db.DateTime)
    ModifiedOn = db.Column(db.DateTime)
    ModifiedBy = db.Column(db.Integer, db.ForeignKey(CraneUser.CraneUserId),nullable=True)
    DeleteStatus = db.Column(db.Enum(DeleteStatusEnum,
                                     values_callable=lambda x: [str(e.value) for e in DeleteStatusEnum]), nullable=True)
    
    def serialise(self):
        '''serialize model object into json object'''
        json_obj = {}
        for column in self.__table__.columns:
            json_obj[column.name] = str(getattr(self, column.name))
        return json_obj
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
