from backend.models.Company import Company
from .. import db
from .CraneUser import CraneUser
from .Wellbore import Wellbore

import enum
from datetime import datetime

class CuttingsCategoryEnum(enum.Enum):
    Washed_Dried = 'Washed Dried'
    Washed_Wet = 'Washed Wet'
    Wet_Unwashed = 'Wet Unwashed'
    Dry_Unwashed = 'Dry Unwashed'

class Cuttings(db.Model):
    __tablename__ = 'geosims_t_Cuttings'
    SampleId = db.Column(db.Integer,primary_key=True)
    WellboreId = db.Column(db.Integer, db.ForeignKey(Wellbore.WellboreId))
    SampleBoxNumber = db.Column(db.VARCHAR(100))
    CuttingCategory = db.Column(db.Enum(CuttingsCategoryEnum), nullable=False)
    SampleType = db.Column(db.VARCHAR(100))
    TopDepth = db.Column(db.Float)
    BottomDepth = db.Column(db.Float)
    StoreIdentifier = db.Column(db.VARCHAR(100))
    Operator = db.Column(db.VARCHAR(100))
    SamplingCompany = db.Column(db.NVARCHAR(255), db.ForeignKey(Company.CompanyLongName),nullable=True)
    SamplingDate = db.Column(db.DateTime)
    SampleInterval = db.Column(db.VARCHAR(100))#
    DateReceived = db.Column(db.DateTime)
    OtherDescription = db.Column(db.VARCHAR(500))
    CreatedById = db.Column(db.Integer, db.ForeignKey(CraneUser.CraneUserId),nullable=False)
    DateCreated = db.Column(db.DateTime, default=datetime.utcnow)
    ModifiedOn = db.Column(db.DateTime, default=datetime.utcnow, onupdate=db.func.current_timestamp())
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
