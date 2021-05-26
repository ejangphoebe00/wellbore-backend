from .. import db

class CoreCatalog(db.Model):
    __tablename__ = 'crane.t_CoreCatalog'
    CoreCatalog_id = db.Column(db.Integer,primary_key=True)
    WellboreCore_id = db.Column(db.Integer,nullable=True)
    CoreType = db.Column(db.Integer)
    StoreIdentifier = db.Column(db.NVARCHAR(100))
    CatalogCoreFromDepth = db.Column(db.DECIMAL)
    CatalogCoreToDepth = db.Column(db.DECIMAL)
    CoreCatalogSecurityFlag_id = db.Column(db.Integer)
    WasAnalysed_id = db.Column(db.Integer)
    TopStratLitho_id = db.Column(db.Integer)
    BottomStratLitho_id = db.Column(db.Integer)
    CatalogueCorePictureName = db.Column(db.TEXT)
    CataloguePictureSoftcopyPath = db.Column(db.TEXT)
    CataloguePictureHyperlink = db.Column(db.TEXT)
    CatPictureUploadDate = db.Column(db.DateTime)
    CatalogueReportSoftcopyPath = db.Column(db.TEXT)
    CatalogueReportHyperlink = db.Column(db.TEXT)
    CatReportUploadDate = db.Column(db.DateTime)
    CatalogReportFormat_id = db.Column(db.Integer)
    CatalogReportFileSize = db.Column(db.DECIMAL)
    CatalogReportSecurityGrade_id = db.Column(db.Integer)
    CoreCatalogName = db.Column(db.NVARCHAR(100))
    Comments = db.Column(db.NVARCHAR(500))
    CreatedBy_id = db.Column(db.Integer)
    DateCreated = db.Column(db.DateTime)
    ModifiedOn = db.Column(db.DateTime)
    ModifiedBy = db.Column(db.NVARCHAR(255))
    

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
