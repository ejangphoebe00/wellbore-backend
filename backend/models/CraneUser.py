from sqlalchemy import true
from .. import db
import enum
from flask_bcrypt import Bcrypt
from datetime import datetime
from .CraneWebSecurityLevel import CraneWebSecurityLevel

class UserCatgoryEnum(enum.Enum):
    App_Admin = 'App Admin'
    Data_Admin = 'Data Admin'
    Staff = 'Staff'

class DeleteStatusEnum(enum.Enum):
    Deleted = "Deleted"
    Available = "Available"
# print(UserCatgoryEnum.App_Admin)

class CraneUser(db.Model):
    __tablename__ = 'geosims_t_CraneUser'
    CraneUserId = db.Column(db.Integer,primary_key=True)
    FirstName = db.Column(db.NVARCHAR(255),nullable=False)
    MiddleName = db.Column(db.NVARCHAR(255),nullable=True)
    Surname = db.Column(db.NVARCHAR(255),nullable=False)
    LUID = db.Column(db.Integer)
    CraneUserName = db.Column(db.NVARCHAR(255),nullable=False, unique=True)
    LoginID = db.Column(db.NVARCHAR(255),nullable=True)
    LoginIDAlias = db.Column(db.NVARCHAR(255), nullable=True)
    UserCategory = db.Column(db.Enum(UserCatgoryEnum,
                                     values_callable=lambda x: [str(e.value) for e in UserCatgoryEnum]),
                                     default='Staff') # persist values instead of keys in the db
    UserCompanyId = db.Column(db.Integer)
    UserPremsUserId = db.Column(db.Integer)
    UserStaffId = db.Column(db.Integer, unique=True)
    OrganisationName = db.Column(db.NVARCHAR(255),nullable=False)
    UserPassword = db.Column(db.NVARCHAR(255),nullable=True)
    UserEmailAddress = db.Column(db.NVARCHAR(255),nullable=False, unique=True)
    UserSecurityLevelId = db.Column(db.Integer)
    UserWebSecurityLevelId = db.Column(db.Integer, db.ForeignKey(CraneWebSecurityLevel.WebSecurityLevelId),nullable=False) 
    UserNogtrWebSecurityLevelId = db.Column(db.Integer)
    UserPremsWebSecurityLevelId = db.Column(db.Integer)
    UserIntranetSecurityLevelId = db.Column(db.Integer)
    UserNsdWebSecurityLevelId = db.Column(db.Integer)
    LoginErrorCount = db.Column(db.Integer)
    LoginStatusId = db.Column(db.Integer)
    LastSeen = db.Column(db.DateTime,nullable=True)
    DeactivateAccount = db.Column(db.SMALLINT,nullable=False)
    ActivationChangeComment = db.Column(db.NVARCHAR(255),nullable=True)
    ActivationChangeDate = db.Column(db.DateTime, nullable=True)
    CredentialsSent = db.Column(db.SMALLINT, nullable=True)
    UserOnlineStatus = db.Column(db.SMALLINT, nullable=True)
    Comments = db.Column(db.NVARCHAR(500),nullable=True)
    OrganisationUserName = db.Column(db.NVARCHAR(255),nullable=True, default='Petroleum Authority of Uganda')
    ProfilePicture = db.Column(db.NVARCHAR(225), nullable=True)
    CreatedById = db.Column(db.Integer)
    DateCreated = db.Column(db.DateTime,default=datetime.utcnow)
    ModifiedOn = db.Column(db.DateTime,default=datetime.utcnow,onupdate=db.func.current_timestamp())
    ModifiedBy = db.Column(db.NVARCHAR(255),nullable=True)
    RecordChangeStamp = db.Column(db.NVARCHAR(100),nullable=True)
    DefaultPassword = db.Column(db.NVARCHAR(255),nullable=True)
    DefaultChangeDate = db.Column(db.DateTime,default=datetime.utcnow, onupdate=db.func.current_timestamp())
    PasswordChangeDate = db.Column(db.DateTime,default=db.func.current_timestamp(),nullable=True)
    DeleteStatus = db.Column(db.Enum(DeleteStatusEnum,
                                     values_callable=lambda x: [str(e.value) for e in DeleteStatusEnum]), nullable=True)

    
    def __repr__(self):
        return '<CraneUser {}>'.format(self.CraneUserName)
    
    def serialise(self):
        '''serialize model object into json object'''
        json_obj = {}
        for column in self.__table__.columns:
            json_obj[column.name] = str(getattr(self, column.name))
        return json_obj
    
    # can be called without an object for this class
    @staticmethod
    def hash_password(password):
        '''use bcrypt to hash passwords'''
        return Bcrypt().generate_password_hash(password).decode()

    def is_password_valid(self, password):
        '''Check the password against it's hash to validates the user's password
            (returns True if passwords match)
        '''
        if self.UserPassword is not None:
            return Bcrypt().check_password_hash(self.UserPassword, password)
        else:
            return Bcrypt().check_password_hash(self.DefaultPassword, password)
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
