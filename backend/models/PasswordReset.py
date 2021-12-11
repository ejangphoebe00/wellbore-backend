from .. import db
from .CraneUser import CraneUser
from datetime import datetime

class PasswordReset(db.Model):
    __tablename__ = "geosims_rt_PasswordReset"
    id = db.Column(db.Integer, primary_key=True)
    ResetKey = db.Column(db.String(128), unique=True)
    CraneUserId = db.Column(db.Integer, db.ForeignKey(CraneUser.CraneUserId),nullable=True)
    CreationDate = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    HasActivated = db.Column(db.Boolean, default=False)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
