from .. import db
from .CraneUser import CraneUser
from .Wellbore import Wellbore
from .Company import Company

import enum
from datetime import datetime

class FluidCategoryEnum(enum.Enum):
    Oil = 'Oil'
    Gas = 'Gas'
    Water = 'Water'

class FluidSamples(db.Model):
    __tablename__ = 'geosims_t_FluidSamples'
    Sample_id = db.Column(db.Integer,primary_key=True)
    Wellbore_id = db.Column(db.Integer, db.ForeignKey(Wellbore.Wellbore_id))
    Sampling_activity = db.Column(db.VARCHAR(100))
    Fluid_category = db.Column(db.Enum(FluidCategoryEnum), nullable=False)
    Sample_type = db.Column(db.VARCHAR(100))
    Sample_volume = db.Column(db.VARCHAR(100))
    Depth_obtained = db.Column(db.Float) #
    Date_collected = db.Column(db.DateTime)
    Date_received = db.Column(db.DateTime)
    Sampling_company = db.Column(db.Integer, db.ForeignKey(Company.Company_id))
    # Analysis_reports = db.Column(db.VARCHAR(100))
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
