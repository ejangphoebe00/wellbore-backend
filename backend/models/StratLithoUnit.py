from .. import db
from .CraneUser import CraneUser

class StratLithoUnit(db.Model):
    __tablename__ = 'crane_t_StratLithoUnit'
    StratLitho_id = db.Column(db.Integer,primary_key=True)
    PAUID = db.Column(db.Integer)
    StratLithoName = db.Column(db.NVARCHAR(100))
    ReserviorUnit = db.Column(db.SMALLINT) # should be 0 or 1
    LithoStratAlias = db.Column(db.NVARCHAR(100))
    IsReservoirUnit_id = db.Column(db.Integer)
    LithoStratAge_id = db.Column(db.Integer)
    LithoStratDescriptionSoftcopyPath = db.Column(db.TEXT)
    LithoStratDescriptionHyperlink = db.Column(db.TEXT)
    LithoStratMapSoftCopyPath = db.Column(db.TEXT)
    LithoStratMapHyperlink = db.Column(db.TEXT)
    MapPortalLithoStratMapLink = db.Column(db.TEXT)
    LithoStratFactsiteUrl = db.Column(db.TEXT)
    Comments = db.Column(db.NVARCHAR(500))
    CreatedBy_id = db.Column(db.Integer, db.ForeignKey('crane_t_CraneUser.CraneUser_id'),nullable=False)
    DateCreated = db.Column(db.DateTime)
    ModifiedOn = db.Column(db.DateTime)
    ModifiedBy = db.Column(db.Integer, db.ForeignKey('crane_t_CraneUser.CraneUser_id'),nullable=True)
    

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
