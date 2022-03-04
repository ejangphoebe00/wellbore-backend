from enum import unique
from .. import db
from .CraneUser import CraneUser, DeleteStatusEnum

class Company(db.Model):
    __tablename__ = 'geosims_t_Company'
    CompanyId = db.Column(db.Integer,primary_key=True)
    PAUID = db.Column(db.NVARCHAR(255),nullable=False, unique=True)
    CompanyLongName = db.Column(db.NVARCHAR(255),nullable=False, unique=True)
    CompanyShortName = db.Column(db.NVARCHAR(255),nullable=True, unique=True)
    NSDNumber = db.Column(db.NVARCHAR(255),nullable=False)
    CompanyCategoryId = db.Column(db.Integer)
    Country = db.Column(db.String)
    # CountryOfOrigin_id = db.Column(db.Integer)
    # CountryOfRegistration_id = db.Column(db.Integer)
    RegistrationNumber = db.Column(db.NVARCHAR(255),nullable=False, unique=True)
    TINNumber = db.Column(db.NVARCHAR(255),nullable=False, unique=True)
    CompanyTelephone = db.Column(db.NVARCHAR(255), nullable=True)
    CompanyEmail = db.Column(db.NVARCHAR(255), unique=True)
    CompanyWebsite = db.Column(db.TEXT)
    CompanyEntityTypeId = db.Column(db.Integer)
    CompanyEntitySubTypeId = db.Column(db.Integer)
    CompanyMajorActivityId = db.Column(db.Integer)
    CompanyActivityDivisionId = db.Column(db.Integer)
    CompanyActivityDivisionClassId = db.Column(db.Integer)
    CompanyActivityDivisionClassCategoryId = db.Column(db.Integer)
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
    RegistrationStatusId = db.Column(db.Integer)
    ClassifyAsUgandanId = db.Column(db.Integer)
    Comments = db.Column(db.TEXT)
    PrimaryCompanyKindId = db.Column(db.Integer)
    SecondaryCompanyKindId = db.Column(db.Integer)
    OtherCompanyKindId = db.Column(db.Integer)
    CompanyGroupId = db.Column(db.Integer)
    CompanyMobile = db.Column(db.NVARCHAR(55))
    CompanyFax = db.Column(db.NVARCHAR(55))
    ContactEntityFax = db.Column(db.NVARCHAR(55))
    NSDFromDate = db.Column(db.Date)
    NSDToDate = db.Column(db.Date)
    ImportedFromNSD = db.Column(db.SMALLINT) #should be between 0 and 1
    ImportedDate = db.Column(db.DateTime)
    ExportedDate = db.Column(db.DateTime)
    ExportedToNogtr = db.Column(db.SMALLINT) #should be between 0 and 1
    CreatedBy = db.Column(db.Integer, db.ForeignKey(CraneUser.CraneUserId),nullable=False)
    DateCreated = db.Column(db.DateTime)
    ModifiedOn = db.Column(db.DateTime)
    ModifiedBy = db.Column(db.Integer, db.ForeignKey(CraneUser.CraneUserId),nullable=True)
    RecordChangeStamp = db.Column(db.NVARCHAR(100))
    PreviousLegalName = db.Column(db.NVARCHAR(100))
    DeleteStatus = db.Column(db.Enum(DeleteStatusEnum,
                                     values_callable=lambda x: [str(e.value) for e in DeleteStatusEnum]), nullable=True)
    
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
