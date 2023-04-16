from sqlalchemy import func
from .base import db


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    is_expired = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

