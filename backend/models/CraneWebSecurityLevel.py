from .. import db

class CraneWebSecurityLevel(db.Model):
    __tablename__ = "crane_rt_CraneWebSecurityLevel"
    WebSecurityLevel_id = db.Column(db.Integer,primary_key=True)
    WebSecurityLevelName = db.Column(db.NVARCHAR(255))
    WebSecurityLevelDescription = db.Column(db.NVARCHAR(255))
    WebSecurityLevelAbbreviation = db.Column(db.NVARCHAR(255))    
    Comments = db.Column(db.NVARCHAR(500))
    ModifiedOn = db.Column(db.DateTime)
    ModifiedBy = db.Column(db.NVARCHAR(255))

    # relationships
    # users = db.relationship('crane_t_CraneUser', backref='crane_rt_CraneWebSecurityLevel', lazy=True)
    
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
