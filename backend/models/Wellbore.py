from .. import db
from .CraneUser import CraneUser
from .Company import Company

class Wellbore(db.Model):
    __tablename__ = 'crane_t_Wellbore'
    Wellbore_id = db.Column(db.Integer,primary_key=True)
    PAUID = db.Column(db.Integer)
    WellboreOfficialName = db.Column(db.NVARCHAR(255),nullable=True)
    WellboreLocalName = db.Column(db.NVARCHAR(255),nullable=False)
    WellboreAliasName = db.Column(db.NVARCHAR(255),nullable=False)
    WellboreSpudDate = db.Column(db.Date)
    SpudYear = db.Column(db.String(50))
    WellboreType_id = db.Column(db.Integer)
    InitialWellborePurpose_id = db.Column(db.Integer)
    WellborePurpose_id = db.Column(db.Integer)
    PurposeChangeDate = db.Column(db.DateTime)
    Well_id = db.Column(db.Integer)
    Prospect_id = db.Column(db.Integer, db.ForeignKey('crane_t_Company.Company_id'),nullable=True)
    Discovery_id = db.Column(db.Integer)
    WellboreContent_id = db.Column(db.Integer)
    WellboreStatus_id = db.Column(db.Integer)
    WellboreResponsibleLicence_id = db.Column(db.Integer)
    LicenseOperatorCompany_id = db.Column(db.Integer, db.ForeignKey('crane_t_Company.Company_id'),nullable=True)
    DrillingContractorCompany_id = db.Column(db.Integer, db.ForeignKey('crane_t_Company.Company_id'),nullable=True)
    WellBoreRigName = db.Column(db.NVARCHAR(255))
    Basin_id = db.Column(db.Integer)
    FormerExplAreaName = db.Column(db.NVARCHAR(255))
    SeismicLine = db.Column(db.NVARCHAR(255))
    RotaryTableElavation = db.Column(db.Float)
    GroundLevelElavation = db.Column(db.Float)
    TD_MD = db.Column(db.Float)
    TD_TVD = db.Column(db.Float)
    TD_Date = db.Column(db.Date)
    # WellboreCore_id = db.Column(db.Integer)
    CoreContractor_id = db.Column(db.Integer, db.ForeignKey('crane_t_Company.Company_id'),nullable=True)
    RCI_Taken_id = db.Column(db.Integer)
    MDT_Done_id = db.Column(db.Integer)
    FET_Done_id = db.Column(db.Integer)
    WFTContractor = db.Column(db.Integer)
    DST_Done_id = db.Column(db.Integer)
    ManifoldFlowTested_id = db.Column(db.Integer)
    DST_Contractor_id = db.Column(db.Integer, db.ForeignKey('crane_t_Company.Company_id'),nullable=True)
    HasPetrophysicalLogs_id = db.Column(db.Integer)
    PetrophysicalContractor_id = db.Column(db.Integer, db.ForeignKey('crane_t_Company.Company_id'),nullable=True)
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
    CreatedBy_id = db.Column(db.Integer, db.ForeignKey('crane_t_CraneUser.CraneUser_id'),nullable=False)
    DateCreated = db.Column(db.DateTime)
    ModifiedOn = db.Column(db.DateTime)
    ModifiedBy = db.Column(db.Integer, db.ForeignKey('crane_t_CraneUser.CraneUser_id'),nullable=True)
    
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
