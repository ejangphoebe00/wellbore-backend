# from .. import db
# from .CraneUser import CraneUser

# class CoreType(db.Model):
#     __tablename__ = 'geosims_rt_CoreType'
#     CoreType_id = db.Column(db.Integer,primary_key=True)
#     CoreTypeName = db.Column(db.NVARCHAR(255), unique=True, nullable=False) 
#     # transfer core type to wellbore core and delete coretype
#     SortOrder = db.Column(db.Integer)    
#     Comments = db.Column(db.NVARCHAR(500))
#     ModifiedOn = db.Column(db.DateTime)
#     ModifiedBy = db.Column(db.Integer, db.ForeignKey(CraneUser.CraneUser_id),nullable=True)


#     def serialise(self):
#         '''serialize model object into json object'''
#         json_obj = {}
#         for column in self.__table__.columns:
#             json_obj[column.name] = str(getattr(self, column.name))
#         return json_obj
    
#     def save(self):
#         db.session.add(self)
#         db.session.commit()

#     def update(self):
#         db.session.commit()

#     def delete(self):
#         db.session.delete(self)
#         db.session.commit()
