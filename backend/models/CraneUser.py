from .. import db

class CraneUser(db.Model):
    __tablename__ = 'crane.t_CraneUser'
    CraneUser_id = db.Column(db.Integer,primary_key=True)
    FirstName = db.Column(db.NVARCHAR(255),nullable=False)
    MiddleName = db.Column(db.NVARCHAR(255),nullable=True)
    Surname = db.Column(db.NVARCHAR(255),nullable=False)
    LUID = db.Column(db.Integer)
    CraneUserName = db.Column(db.NVARCHAR(255),nullable=False)
    LoginID = db.Column(db.NVARCHAR(255),nullable=False)
    LoginIDAlias = db.Column(db.NVARCHAR(255), nullable=True)
    UserCategory_id = db.Column(db.Integer)
    UserCompany_id = db.Column(db.Integer)
    UserCategory_id = db.Column(db.Integer)
    UserPremsUser_id = db.Column(db.Integer)
    UserStaff_id = db.Column(db.Integer)
    OrganisationName = db.Column(db.NVARCHAR(255),nullable=False)
    CraneUserID = db.Column(db.NVARCHAR(255))
    UserPassword = db.Column(db.TEXT,nullable=False)
    UserEmailAddress = db.Column(db.NVARCHAR(255),nullable=False)
    UserSecurityLevel_id = db.Column(db.Integer,nullable=False)
    UserWebSecurityLevel_id = db.Column(db.Integer,nullable=False)
    UserNogtrWebSecurityLevel_id = db.Column(db.Integer,nullable=False)
    UserPremsWebSecurityLevel_id = db.Column(db.Integer,nullable=False)
    UserIntranetSecurityLevel_id = db.Column(db.Integer,nullable=False)
    UserNsdWebSecurityLevel_id = db.Column(db.Integer,nullable=False)
    LoginErrorCount = db.Column(db.Integer)
    LoginStatus_id = db.Column(db.Integer)
    LastSeen = db.Column(db.DateTime)
    DeactivateAccount = db.Column(db.SMALLINT)
    ActivationChangeComment = db.Column(db.NVARCHAR(255))
    ActivationChangeDate = db.Column(db.DateTime)
    CredentialsSent = db.Column(db.SMALLINT)
    UserOnlineStatus = db.Column(db.SMALLINT)
    Comments = db.Column(db.NVARCHAR(500))
    OrganisationUserName = db.Column(db.NVARCHAR(255))
    CreatedBy_id = db.Column(db.Integer)
    DateCreated = db.Column(db.DateTime)
    ModifiedOn = db.Column(db.DateTime)
    ModifiedBy = db.Column(db.NVARCHAR(255))
    RecordChangeStamp = db.Column(db.VARBINARY('MAX'))
    DefaultPassword = db.Column(db.NVARCHAR(255))
    DefaultChangeDate = db.Column(db.DateTime)
    StoredUserPassword = db.Column(db.NVARCHAR(255))
    PasswordChangeDate = db.Column(db.TIMESTAMP)
    
    def __repr__(self):
        return '<CraneUser {}>'.format(self.CraneUserName)
    
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
