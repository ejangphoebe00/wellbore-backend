from .. import db
from .CraneUser import CraneUser
from .Core import Cores
# from .FileSecurityGrade import FileSecurityGrade
# from .FileFormat import FileFormat
from .StratLithoUnit import StratLithoUnit
# from .CoreType import CoreType
# from .CatalogSecurityFlag import CatalogSecurityFlag

class CoreCatalog(db.Model):
    __tablename__ = 'geosims_t_CoreCatalog'
    CoreCatalogId = db.Column(db.Integer,primary_key=True)
    WellboreCoreId = db.Column(db.Integer, db.ForeignKey(Cores.WellboreCoreId),nullable=False)
    # CoreType = db.Column(db.Integer, db.ForeignKey(CoreType.CoreTypeId),nullable=False)
    StoreIdentifier = db.Column(db.NVARCHAR(100))
    CatalogCoreFromDepth = db.Column(db.DECIMAL)
    CatalogCoreToDepth = db.Column(db.DECIMAL)
    # CoreCatalogSecurityFlagId = db.Column(db.Integer, db.ForeignKey(CatalogSecurityFlag.CatalogSecurityFlagId),nullable=True)
    WasAnalysedId = db.Column(db.Integer)
    TopStratLithoId = db.Column(db.Integer, db.ForeignKey(StratLithoUnit.StratLithoId),nullable=True)
    BottomStratLithoId = db.Column(db.Integer, db.ForeignKey(StratLithoUnit.StratLithoId),nullable=True)
    CatalogueCorePictureName = db.Column(db.TEXT)
    CataloguePictureSoftcopyPath = db.Column(db.TEXT)
    CataloguePictureHyperlink = db.Column(db.TEXT)
    CatPictureUploadDate = db.Column(db.DateTime)
    CatalogueReportSoftcopyPath = db.Column(db.TEXT)
    CatalogueReportHyperlink = db.Column(db.TEXT)
    CatReportUploadDate = db.Column(db.DateTime)
    # CatalogReportFormatId = db.Column(db.Integer, db.ForeignKey(FileFormat.FileFormatId),nullable=True)
    CatalogReportFileSize = db.Column(db.DECIMAL)
    # CatalogReportSecurityGradeId = db.Column(db.Integer, db.ForeignKey(FileSecurityGrade.FileSecurityGradeId),nullable=True)
    CoreCatalogName = db.Column(db.NVARCHAR(100), unique=True, nullable=False)
    Comments = db.Column(db.NVARCHAR(500))
    CreatedById = db.Column(db.Integer, db.ForeignKey(CraneUser.CraneUserId),nullable=False)
    DateCreated = db.Column(db.DateTime)
    ModifiedOn = db.Column(db.DateTime)
    ModifiedBy = db.Column(db.Integer, db.ForeignKey(CraneUser.CraneUserId),nullable=True)
    

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
