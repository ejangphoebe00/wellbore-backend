from .. import db
from .CraneUser import CraneUser, DeleteStatusEnum

class CraneUserLoginHistory(db.Model):
    __tablename__ = 'geosims_t_CraneUserLoginHistory'
    UserLoginHistoryId = db.Column(db.Integer,primary_key=True)
    HistLogUserId = db.Column(db.Integer, db.ForeignKey(CraneUser.CraneUserId),nullable=False) 
    LogStaffId = db.Column(db.Integer)
    CraneCompanyId = db.Column(db.Integer)   
    LogCompanyAuthorisedUserId = db.Column(db.Integer)
    LogAuthorisedUserName = db.Column(db.VARCHAR(100)) 
    LoginStatusId = db.Column(db.Integer)   
    UserOnlineStatus = db.Column(db.SMALLINT)  
    LogLoginDate = db.Column(db.DateTime)  
    LogLogoutDate = db.Column(db.DateTime) 
    UserLoginLogName = db.Column(db.VARCHAR(100)) 
    UserAcessLogName = db.Column(db.VARCHAR(100))   
    Comments = db.Column(db.NVARCHAR(500))
    DeleteStatus = db.Column(db.Enum(DeleteStatusEnum,
                                     values_callable=lambda x: [str(e.value) for e in DeleteStatusEnum]), nullable=True)
    
    def __repr__(self):
        return '<CraneUserLoginHistory {}>'.format(self.LogAuthorisedUserName)
    
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
