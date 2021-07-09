from .. import db
from .CraneUser import CraneUser

class CraneUserLoginHistory(db.Model):
    __tablename__ = 'crane.t_CraneUserLoginHistory'
    UserLoginHistory_id = db.Column(db.Integer,primary_key=True)
    HistLogUser_id = db.Column(db.Integer, db.ForeignKey('crane.t_CraneUser.CraneUser_id'),nullable=False) 
    LogStaff_id = db.Column(db.Integer)
    CraneCompany_id = db.Column(db.Integer)   
    LogCompanyAuthorisedUser_id = db.Column(db.Integer)
    LogAuthorisedUserName = db.Column(db.VARCHAR(100)) 
    LoginStatus_id = db.Column(db.Integer)   
    UserOnlineStatus = db.Column(db.SMALLINT)  
    LogLoginDate = db.Column(db.DateTime)  
    LogLogoutDate = db.Column(db.DateTime) 
    UserLoginLogName = db.Column(db.VARCHAR(100)) 
    UserAcessLogName = db.Column(db.VARCHAR(100))   
    Comments = db.Column(db.NVARCHAR(500))
    
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
