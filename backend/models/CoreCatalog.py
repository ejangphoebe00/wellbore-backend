from .. import db
from .CraneUser import CraneUser, DeleteStatusEnum
from .Core import Cores
from .StratLithoUnit import StratLithoUnit

class CoreCatalog(db.Model):
    __tablename__ = 'geosims_t_CoreCatalog'
    CoreCatalogId = db.Column(db.Integer,primary_key=True)
    WellboreCoreId = db.Column(db.Integer, db.ForeignKey(Cores.WellboreCoreId),nullable=False)
    StoreIdentifier = db.Column(db.NVARCHAR(100))
    CatalogCoreFromDepth = db.Column(db.DECIMAL)
    CatalogCoreToDepth = db.Column(db.DECIMAL)
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
    CatalogReportFileSize = db.Column(db.DECIMAL)
    CoreCatalogName = db.Column(db.NVARCHAR(100), unique=True, nullable=False)
    Comments = db.Column(db.NVARCHAR(500))
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
