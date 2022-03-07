from .. import db
from .CraneUser import CraneUser, DeleteStatusEnum
from .Wellbore import Wellbore
from .Company import Company
from .StratLithoUnit import StratLithoUnit
import enum

class CoreTypeEnum(enum.Enum):
    Slab = "Slab"
    Slab_1_2 = "1/2 Slab"
    Slab_1_3 = "1/3 Slab"
    Slab_2_3 = "2/3 Slab"
    Biscuit_Slab = "Biscuit Slab"
    Full_Diameter = "Full Diameter"
    SideWall_Core = "SideWall Core"

class ReportFormatEnum(enum.Enum):
    PDF = "PDF"
    EXCEL = "EXCEL"

class SecurityGradeEnum(enum.Enum):
    Restricted = "Restricted"
    Confidential = "Confidential"
    Open = "Open"

# rename this to cores
class Cores(db.Model):
    __tablename__ = 'geosims_t_Cores'
    WellboreCoreId = db.Column(db.Integer,primary_key=True)
    WellborePAUID = db.Column(db.Integer, db.ForeignKey(Wellbore.PAUID),nullable=False)
    WelboreCoreName = db.Column(db.NVARCHAR(255), db.ForeignKey(Wellbore.WellboreOfficialName),nullable=False)
    CoreNumber = db.Column(db.NVARCHAR(255), unique=True)
    CoreTypeName = db.Column(db.Enum(CoreTypeEnum,
            values_callable=lambda enum: [str(e.value) for e in enum]), nullable=False)     
    CoringDate = db.Column(db.Date)
    WBCoringContractorId = db.Column(db.Integer, db.ForeignKey(Company.CompanyId),nullable=True)
    CoreTopMD = db.Column(db.DECIMAL)
    CoreBtmMD = db.Column(db.DECIMAL)
    CoreTopTVD = db.Column(db.DECIMAL)
    CoreBtmTVD = db.Column(db.DECIMAL)
    CutLength = db.Column(db.String(100))
    CutLengthTVD = db.Column(db.String(100))
    RecoveredLength = db.Column(db.DECIMAL)
    PercentageCoreRecovery = db.Column(db.Float) #(cutlength/(cutlength+recoveredlength))*100
    CoreTopStratLithoId = db.Column(db.Integer, db.ForeignKey(StratLithoUnit.StratLithoId),nullable=True)
    CoreBottomStratLithoId = db.Column(db.Integer, db.ForeignKey(StratLithoUnit.StratLithoId),nullable=True)
    CorePictureSoftcopyPath = db.Column(db.TEXT)
    CorePictureHyperlink = db.Column(db.TEXT)
    PictureUploadDate = db.Column(db.DateTime)
    CoreReportSoftcopyPath = db.Column(db.TEXT)
    CoreReportHyperlink = db.Column(db.TEXT)
    ReportUploadDate = db.Column(db.DateTime)
    ReportFileFormat = db.Column(db.Enum(ReportFormatEnum))
    ReportFileSize = db.Column(db.DECIMAL)
    ReportSecurityGrade = db.Column(db.Enum(SecurityGradeEnum))
    ReportOpenDueDate = db.Column(db.DateTime)
    ReportDocumentTitle = db.Column(db.NVARCHAR(100))
    ReportReceivedDate = db.Column(db.DateTime)
    ReportDocumentDate = db.Column(db.DateTime)
    ReportDocumentName = db.Column(db.NVARCHAR(100))
    StoreIdentifier = db.Column(db.NVARCHAR(100))
    AnalysisReportDetails = db.Column(db.NVARCHAR(500))
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

    @staticmethod
    def calculate_percentage_core_recovery(cutlength, recoveredlength):
        if cutlength is not None and recoveredlength is not None:
            result = (float(cutlength)/(float(cutlength)+float(recoveredlength)))*100
            return round(result,2)
        else:
            return 0
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
