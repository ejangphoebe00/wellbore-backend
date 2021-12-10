from .. import db
from .CraneUser import CraneUser
from .RockSamples import RockSamples
from .Core import Cores
from .FluidSamples import FluidSamples

import enum
from datetime import datetime

class ReportTypeEnum(enum.Enum):
    Cores = 'Cores'
    Fluid_Samples = 'Fluid_Samples'
    Rock_Samples = 'Rock_Samples'

# named files in order to accommodate both images and documents/reports
class Files(db.Model):
    __tablename__ = 'geosims_rt_Files'
    FileId = db.Column(db.Integer,primary_key=True)
    CoresId = db.Column(db.Integer, db.ForeignKey(Cores.WellboreCoreId))
    FluidSamplesId = db.Column(db.Integer, db.ForeignKey(FluidSamples.SampleId))
    RockSamplesId = db.Column(db.Integer, db.ForeignKey(RockSamples.id))
    ReportType = db.Column(db.Enum(ReportTypeEnum))
    ReportPath = db.Column(db.VARCHAR(500))
    PhotographPath = db.Column(db.VARCHAR(500))
    CreatedById = db.Column(db.Integer, db.ForeignKey(CraneUser.CraneUserId),nullable=False)
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
