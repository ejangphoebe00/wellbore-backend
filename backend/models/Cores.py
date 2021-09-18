from .. import db
from .CraneUser import CraneUser
from .Wellbore import Wellbore
from .Company import Company
from datetime import datetime


class Cores(db.Model):
    __tablename__ = 'cores'
    Core_sample_id = db.Column(db.Integer,primary_key=True)
    Coring_contractor = db.Column(db.Integer, db.ForeignKey(Company.Company_id))
    Wellbore_id = db.Column(db.Integer, db.ForeignKey(Wellbore.Wellbore_id))
    Core_number = db.Column(db.VARCHAR(100))
    Coring_date = db.Column(db.DateTime)
    Top_MD = db.Column(db.VARCHAR(100)) #depth
    Bottom_MD = db.Column(db.VARCHAR(100)) #depth
    Cut_length = db.Column(db.Integer)
    Percentage_recovery = db.Column(db.Float)
    Top_formation = db.Column(db.VARCHAR(100)) #
    Bottom_formation = db.Column(db.VARCHAR(100)) #
    Core_photograph = db.Column(db.VARCHAR(100)) 
    Core_analysis_reports = db.Column(db.VARCHAR(100)) # can be multiple
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
    
    def last_inserted(self):
        db.session.flush()
