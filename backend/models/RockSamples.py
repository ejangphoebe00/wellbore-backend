import enum
from .. import db
from .CraneUser import CraneUser, DeleteStatusEnum
from datetime import datetime

class BasinsEnum(enum.Enum):
    Edward = "Edward-George"
    Semiliki = "Semiliki"
    Pakwach = "Pakwach"
    Albertine = "The Albertine Graben"
    Hoima = "Hoima Basin"
    Kyoga = "Lake Kyoga Basin"
    Wamala = "Lake Wamala Basin"
    Kadam = "Kadam-Moroto Basin"

class SamplePurposeEnum(enum.Enum):
    Rock_Minerals_Analysis = "Rock Minerals Analysis"
    Clay_and_Whole_rock_Analysis = "Clay and Whole-rock Analysis"
    Rock_Pyrolysis_Analysis = "Rock Pyrolysis Analysis"
    Others = "Others"


class RockSamples(db.Model):
    __tablename__ = 'geosims_t_RockSamples'
    id = db.Column(db.Integer,primary_key=True)
    StoreId = db.Column(db.VARCHAR(100), nullable=False)
    DateCollected = db.Column(db.DateTime)
    DateReceived = db.Column(db.DateTime)
    SampleBasin = db.Column(db.Enum(BasinsEnum,
             values_callable=lambda enum: [str(e.value) for e in enum]))
    SamplePurpose = db.Column(db.Enum(SamplePurposeEnum,
             values_callable=lambda enum: [str(e.value) for e in enum]))
    OtherSpecifiedSamplePurpose = db.Column(db.VARCHAR(100))
    SampleName = db.Column(db.VARCHAR(100))
    Latitude = db.Column(db.VARCHAR(100))
    Longitude = db.Column(db.VARCHAR(100))
    Operator = db.Column(db.VARCHAR(100))
    PetrographicDescription = db.Column(db.VARCHAR(500))
    # Petrographic_analysis_reports = db.Column(db.VARCHAR(100))
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
