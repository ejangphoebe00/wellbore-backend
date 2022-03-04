# from backend.models.CraneUser import DeleteStatusEnum
import enum
from .. import db

class DeleteStatusEnum(enum.Enum):
    Deleted = "Deleted"
    Available = "Available"

class CraneWebSecurityLevel(db.Model):
    __tablename__ = "geosims_rt_CraneWebSecurityLevel"
    WebSecurityLevelId = db.Column(db.Integer,primary_key=True)
    WebSecurityLevelName = db.Column(db.NVARCHAR(255), unique=True, nullable=False)
    WebSecurityLevelDescription = db.Column(db.NVARCHAR(255))
    WebSecurityLevelAbbreviation = db.Column(db.NVARCHAR(255), unique=True)    
    Comments = db.Column(db.NVARCHAR(500))
    ModifiedOn = db.Column(db.DateTime)
    ModifiedBy = db.Column(db.NVARCHAR(255))
    DeleteStatus = db.Column(db.Enum(DeleteStatusEnum,
                                     values_callable=lambda x: [str(e.value) for e in DeleteStatusEnum]), nullable=True)

    # relationships
    # users = db.relationship('geosims_t_CraneUser', backref='geosims_rt_CraneWebSecurityLevel', lazy=True)
    
    def __repr__(self):
        return '<CraneWebSecurityLevel {}>'.format(self.WebSecurityLevelName)
    
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
