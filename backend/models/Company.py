from enum import unique
from .. import db
from .CraneUser import CraneUser

class Company(db.Model):
    __tablename__ = 'crane_t_Company'
    Company_id = db.Column(db.Integer,primary_key=True)
    PAUID = db.Column(db.NVARCHAR(255),nullable=False, unique=True)
    CompanyLongName = db.Column(db.NVARCHAR(255),nullable=False, unique=True)
    CompanyShortName = db.Column(db.NVARCHAR(255),nullable=True, unique=True)
    NSD_Number = db.Column(db.NVARCHAR(255),nullable=False)
    CompanyCategory_id = db.Column(db.Integer)
    CountryOfOrigin_id = db.Column(db.Integer)
    CountryOfRegistration_id = db.Column(db.Integer)
    RegistrationNumber = db.Column(db.NVARCHAR(255),nullable=False, unique=True)
    TINNumber = db.Column(db.NVARCHAR(255),nullable=False, unique=True)
    CompanyTelephone = db.Column(db.NVARCHAR(255), nullable=True)
    CompanyEmail = db.Column(db.NVARCHAR(255), unique=True)
    CompanyWebsite = db.Column(db.TEXT)
    CompanyEntityType_id = db.Column(db.Integer)
    CompanyEntitySubType_id = db.Column(db.Integer)
    CompanyMajorActivity_id = db.Column(db.Integer)
    CompanyActivityDivision_id = db.Column(db.Integer)
    CompanyActivityDivisionClass_id = db.Column(db.Integer)
    CompanyActivityDivisionClassCategory_id = db.Column(db.Integer)
    BusinessNatureDescription = db.Column(db.TEXT)
    CompanyPostalAddress = db.Column(db.NVARCHAR(255))
    CompanyPhysicalAddress = db.Column(db.NVARCHAR(255))
    CompanyOtherEmails = db.Column(db.NVARCHAR(255))
    NSDQualificationDate = db.Column(db.DateTime)
    NSDQualificationYear = db.Column(db.String(10))
    # CompanyOtherEmails = db.Column(db.NVARCHAR(100))
    PrimaryContactEntity = db.Column(db.NVARCHAR(50))
    ContactEntityEmail = db.Column(db.NVARCHAR(100))
    ContactEntityTelephone = db.Column(db.NVARCHAR(55))
    ContactEntityMobile = db.Column(db.NVARCHAR(55))
    ContactDesignation = db.Column(db.NVARCHAR(100))
    OperatorSortOrder = db.Column(db.Integer)
    ContractorSortOrder = db.Column(db.Integer)
    PAURegistrationDate = db.Column(db.DateTime)
    CraneNOGTRID = db.Column(db.NVARCHAR(100))
    TempNOGTRIPwd = db.Column(db.TEXT)
    RegistrationStatus_id = db.Column(db.Integer)
    ClassifyAsUgandan_id = db.Column(db.Integer)
    Comments = db.Column(db.TEXT)
    PrimaryCompanyKind_id = db.Column(db.Integer)
    SecondaryCompanyKind_id = db.Column(db.Integer)
    OtherCompanyKind_id = db.Column(db.Integer)
    CompanyGroup_id = db.Column(db.Integer)
    CompanyMobile = db.Column(db.NVARCHAR(55))
    CompanyFax = db.Column(db.NVARCHAR(55))
    ContactEntityFax = db.Column(db.NVARCHAR(55))
    NSD_FromDate = db.Column(db.Date)
    NSD_ToDate = db.Column(db.Date)
    ImportedFromNSD = db.Column(db.SMALLINT, db.CheckConstraint('0 <= ImportedFromNSD <= 1')) #should be between 0 and 1
    ImportedDate = db.Column(db.DateTime)
    ExportedDate = db.Column(db.DateTime)
    ExportedToNogtr = db.Column(db.SMALLINT, db.CheckConstraint('0 <= ExportedToNogtr <= 1')) #should be between 0 and 1
    CreatedBy = db.Column(db.Integer, db.ForeignKey('crane_t_CraneUser.CraneUser_id'),nullable=False)
    DateCreated = db.Column(db.DateTime)
    ModifiedOn = db.Column(db.DateTime)
    ModifiedBy = db.Column(db.Integer, db.ForeignKey('crane_t_CraneUser.CraneUser_id'),nullable=True)
    RecordChangeStamp = db.Column(db.NVARCHAR(100))
    PreviousLegalName = db.Column(db.NVARCHAR(100))
    
    def __repr__(self):
        return '<Company {}>'.format(self.CompanyShortName)
    
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
