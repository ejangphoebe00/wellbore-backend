from .. import db
from .CraneUser import CraneUser
from .WellboreCore import WellboreCore
from .FileSecurityGrade import FileSecurityGrade
from .FileFormat import FileFormat
from .StratLithoUnit import StratLithoUnit
from .CoreType import CoreType
from .CatalogSecurityFlag import CatalogSecurityFlag

class CoreCatalog(db.Model):
    __tablename__ = 'crane_t_CoreCatalog'
    CoreCatalog_id = db.Column(db.Integer,primary_key=True)
    WellboreCore_id = db.Column(db.Integer, db.ForeignKey('crane_t_WellboreCore.WellboreCore_id'),nullable=False)
    CoreType = db.Column(db.Integer, db.ForeignKey('crane_rt_CoreType.CoreType_id'),nullable=False)
    StoreIdentifier = db.Column(db.NVARCHAR(100))
    CatalogCoreFromDepth = db.Column(db.DECIMAL)
    CatalogCoreToDepth = db.Column(db.DECIMAL)
    CoreCatalogSecurityFlag_id = db.Column(db.Integer, db.ForeignKey('crane_rt_CatalogSecurityFlag.CatalogSecurityFlag_id'),nullable=True)
    WasAnalysed_id = db.Column(db.Integer)
    TopStratLitho_id = db.Column(db.Integer, db.ForeignKey('crane_t_StratLithoUnit.StratLitho_id'),nullable=True)
    BottomStratLitho_id = db.Column(db.Integer, db.ForeignKey('crane_t_StratLithoUnit.StratLitho_id'),nullable=True)
    CatalogueCorePictureName = db.Column(db.TEXT)
    CataloguePictureSoftcopyPath = db.Column(db.TEXT)
    CataloguePictureHyperlink = db.Column(db.TEXT)
    CatPictureUploadDate = db.Column(db.DateTime)
    CatalogueReportSoftcopyPath = db.Column(db.TEXT)
    CatalogueReportHyperlink = db.Column(db.TEXT)
    CatReportUploadDate = db.Column(db.DateTime)
    CatalogReportFormat_id = db.Column(db.Integer, db.ForeignKey('crane_rt_FileFormat.FileFormat_id'),nullable=True)
    CatalogReportFileSize = db.Column(db.DECIMAL)
    CatalogReportSecurityGrade_id = db.Column(db.Integer, db.ForeignKey('crane_rt_FileSecurityGrade.FileSecurityGrade_id'),nullable=True)
    CoreCatalogName = db.Column(db.NVARCHAR(100), unique=True, nullable=False)
    Comments = db.Column(db.NVARCHAR(500))
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
