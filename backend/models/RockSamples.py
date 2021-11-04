import enum
from .. import db
from .CraneUser import CraneUser
from datetime import datetime

class BasinsEnum(enum.Enum):
    Albertine = "The Albertine Graben"
    Hoima = "Hoima Basin"
    Kyoga = "Lake Kyoga Basin"
    Wamala = "Lake Wamala Basin"
    Kadam = "Kadam-Moroto Basin"


class RockSamples(db.Model):
    __tablename__ = 'geosims_t_RockSamples'
    id = db.Column(db.Integer,primary_key=True)
    Sample_id = db.Column(db.VARCHAR(100), nullable=False, unique=True)
    Date_collected = db.Column(db.DateTime)
    Date_received = db.Column(db.DateTime)
    Sample_basin = db.Column(db.Enum(BasinsEnum,
             values_callable=lambda enum: [str(e.value) for e in enum]))
    Rock_name = db.Column(db.VARCHAR(100))
    Coordinate_location = db.Column(db.VARCHAR(100))
    Petrographic_description = db.Column(db.VARCHAR(500))
    # Petrographic_analysis_reports = db.Column(db.VARCHAR(100))
    CreatedBy_id = db.Column(db.Integer, db.ForeignKey(CraneUser.CraneUser_id),nullable=False)
    DateCreated = db.Column(db.DateTime, default=datetime.utcnow)
    ModifiedOn = db.Column(db.DateTime, default=datetime.utcnow, onupdate=db.func.current_timestamp())
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
