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
    Sample_id = db.Column(db.Integer,primary_key=True)
    Wellbore_id = db.Column(db.Integer, db.ForeignKey(Wellbore.Wellbore_id))
    Sample_box_number = db.Column(db.VARCHAR(100))
    Cutting_category = db.Column(db.Enum(CuttingsCategoryEnum), nullable=False)
    Sample_type = db.Column(db.VARCHAR(100))
    Minimum_depth = db.Column(db.Float)
    Maximum_depth = db.Column(db.Float)
    Sample_interval = db.Column(db.VARCHAR(100))#
    Date_received = db.Column(db.DateTime)
    Other_description = db.Column(db.VARCHAR(500))
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
