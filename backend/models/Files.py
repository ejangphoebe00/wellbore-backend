from .. import db
from .CraneUser import CraneUser
from .RockSamples import RockSamples
from .Cores import Cores
from .FluidSamples import FluidSamples

import enum
from datetime import datetime

class ReportTypeEnum(enum.Enum):
    Cores = 'Cores'
    Fluid_Samples = 'Fluid_Samples'
    Rock_Samples = 'Rock_Samples'

# named files in order to accommodate both images and documents/reports
class Files(db.Model):
    __tablename__ = 'reports'
    Report_id = db.Column(db.Integer,primary_key=True)
    Cores_id = db.Column(db.Integer, db.ForeignKey(Cores.Core_sample_id))
    Fluid_samples_id = db.Column(db.Integer, db.ForeignKey(FluidSamples.Sample_id))
    Rock_samples_id = db.Column(db.Integer, db.ForeignKey(RockSamples.id))
    Report_type = db.Column(db.Enum(ReportTypeEnum))
    file_path = db.Column(db.VARCHAR(500))
    CreatedBy_id = db.Column(db.Integer, db.ForeignKey(CraneUser.CraneUser_id),nullable=False)
    DateCreated = db.Column(db.DateTime, default=datetime.utcnow)


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
