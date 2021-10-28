from .. import db
from .CraneUser import CraneUser
from .Wellbore import Wellbore
from .FileSecurityGrade import FileSecurityGrade
from .FileFormat import FileFormat
from .Company import Company
from .StratLithoUnit import StratLithoUnit

class WellboreCore(db.Model):
    __tablename__ = 'geosims_t_WellboreCore'
    WellboreCore_id = db.Column(db.Integer,primary_key=True)
    Wellbore_id = db.Column(db.Integer, db.ForeignKey(Wellbore.Wellbore_id),nullable=False)
    CoreNumber = db.Column(db.NVARCHAR(255), unique=True)
    CoringDate = db.Column(db.Date)
    WBCoringContractor_id = db.Column(db.Integer, db.ForeignKey(Company.Company_id),nullable=True)
    CoreTopMDRT = db.Column(db.DECIMAL)
    CoreBtmMDRT = db.Column(db.DECIMAL)
    CoreTopTVD = db.Column(db.DECIMAL)
    CoreBtmTVD = db.Column(db.DECIMAL)
    CutLength = db.Column(db.String(100))
    CutLengthTVD = db.Column(db.String(100))
    RecoveredLength = db.Column(db.DECIMAL)
    CoreRecovery = db.Column(db.String(100))
    CoreTopStratLitho_id = db.Column(db.Integer, db.ForeignKey(StratLithoUnit.StratLitho_id),nullable=True)
    CoreBottomStratLitho_id = db.Column(db.Integer, db.ForeignKey(StratLithoUnit.StratLitho_id),nullable=True)
    CorePictureSoftcopyPath = db.Column(db.TEXT)
    CorePictureHyperlink = db.Column(db.TEXT)
    PictureUploadDate = db.Column(db.DateTime)
    CoreReportSoftcopyPath = db.Column(db.TEXT)
    CoreReportHyperlink = db.Column(db.TEXT)
    ReportUploadDate = db.Column(db.DateTime)
    ReportFormat_id = db.Column(db.Integer, db.ForeignKey(FileFormat.FileFormat_id),nullable=True)
    ReportFileSize = db.Column(db.DECIMAL)
    CoreReportSecurityGrade_id = db.Column(db.Integer, db.ForeignKey(FileSecurityGrade.FileSecurityGrade_id),nullable=True)
    ReportOpenDueDate = db.Column(db.DateTime)
    ReportDocumentTitle = db.Column(db.NVARCHAR(100))
    ReportReceivedDate = db.Column(db.DateTime)
    ReportDocumentDate = db.Column(db.DateTime)
    ReportDocumentName = db.Column(db.NVARCHAR(100))
    WellboreCoreName = db.Column(db.NVARCHAR(100), unique=True)
    Comments = db.Column(db.NVARCHAR(500))
    CreatedBy_id = db.Column(db.Integer, db.ForeignKey(CraneUser.CraneUser_id),nullable=False)
    DateCreated = db.Column(db.DateTime)
    ModifiedOn = db.Column(db.DateTime)
    ModifiedBy = db.Column(db.Integer, db.ForeignKey(CraneUser.CraneUser_id),nullable=True)
    

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
