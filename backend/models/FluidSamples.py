from .. import db
from .CraneUser import CraneUser, DeleteStatusEnum
from .Wellbore import Wellbore
from .Company import Company

import enum
from datetime import datetime

class FluidCategoryEnum(enum.Enum):
    Oil = 'Oil'
    Gas = 'Gas'
    Water = 'Water'

class FluidSampleBasin(enum.Enum):
    Edward = "Edward-George"
    Semiliki = "Semiliki"
    Pakwach = "Pakwach"
    Albertine = "The Albertine Graben"
    Hoima = "Hoima Basin"
    Kyoga = "Lake Kyoga Basin"
    Wamala = "Lake Wamala Basin"
    Kadam = "Kadam-Moroto Basin"

class FluidSamplePurposeEnum(enum.Enum):
    Crude_Oil_Analysis = "Crude Oil Analysis"
    PVT_Analysis = "PVT Analysis"
    Formation_Water_Analysis = "Formation Water Analysis"
    Natural_Gas_Analysis = "Natural Gas Analysis"
    Others = "Others"

class FluidSamples(db.Model):
    __tablename__ = 'geosims_t_FluidSamples'
    SampleId = db.Column(db.Integer,primary_key=True)
    WellboreId = db.Column(db.Integer, db.ForeignKey(Wellbore.WellboreId))
    SamplingActivity = db.Column(db.VARCHAR(100))
    FluidCategory = db.Column(db.Enum(FluidCategoryEnum), nullable=False)
    SampleType = db.Column(db.VARCHAR(100))
    SampleVolume = db.Column(db.VARCHAR(100))
    SampleBasin = db.Column(db.Enum(FluidSampleBasin,
             values_callable=lambda enum: [str(e.value) for e in enum]))
    DepthObtained = db.Column(db.Float) #
    DateCollected = db.Column(db.DateTime)
    DateReceived = db.Column(db.DateTime)
    SamplingCompany = db.Column(db.Integer, db.ForeignKey(Company.CompanyId))
    SamplePurpose = db.Column(db.Enum(FluidSamplePurposeEnum,
             values_callable=lambda enum: [str(e.value) for e in enum]))
    OtherSpecifiedSamplePurpose = db.Column(db.VARCHAR(100))
    # Analysis_reports = db.Column(db.VARCHAR(100))
    CreatedById = db.Column(db.Integer, db.ForeignKey(CraneUser.CraneUserId),nullable=False)
    DateCreated = db.Column(db.DateTime, default=datetime.utcnow)
    ModifiedOn = db.Column(db.DateTime, default=datetime.utcnow, onupdate=db.func.current_timestamp())
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
