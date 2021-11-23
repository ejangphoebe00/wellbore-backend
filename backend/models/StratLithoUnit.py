from enum import Enum
from .. import db
from .CraneUser import CraneUser

class LithoAgeEnum(Enum):
    Early_Pliocene = "Early Pliocene"
    Early_Miocene = "Early Miocene" 
    Early_Pleistocene = "Early Pleistocene"
    Holocene = "Holocene" 
    Late_Miocene = "Late Miocene"
    Late_Pleistocene = "Late Pleistocene"
    Middle_Miocene = "Middle Miocene"
    Precambrian = "Precambrian"


class StratLithoUnit(db.Model):
    __tablename__ = 'geosims_t_StratLithoUnit'
    StratLitho_id = db.Column(db.Integer,primary_key=True)
    PAUID = db.Column(db.Integer)
    StratLithoName = db.Column(db.NVARCHAR(100), unique=True, nullable=False)
    # ReserviorUnit = db.Column(db.SMALLINT) # should be 0 or 1
    LithoStratAlias = db.Column(db.NVARCHAR(100))
    IsReservoirUnit_id = db.Column(db.Integer)
    LithoStratAge = db.Column(db.Enum(LithoAgeEnum,
             values_callable=lambda enum: [str(e.value) for e in enum]))
    LithoStratDescriptionSoftcopyPath = db.Column(db.TEXT)
    LithoStratDescriptionHyperlink = db.Column(db.TEXT)
    LithoStratMapSoftCopyPath = db.Column(db.TEXT)
    LithoStratMapHyperlink = db.Column(db.TEXT)
    MapPortalLithoStratMapLink = db.Column(db.TEXT)
    LithoStratFactsiteUrl = db.Column(db.TEXT)
    Comments = db.Column(db.NVARCHAR(500))
    CreatedBy_id = db.Column(db.Integer, db.ForeignKey(CraneUser.CraneUser_id),nullable=False)
    DateCreated = db.Column(db.DateTime)
    ModifiedOn = db.Column(db.DateTime)
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
