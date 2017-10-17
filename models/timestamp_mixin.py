from models.base_model import db as DB
from datetime import datetime

class TimestampMixin:
    created  = DB.Column(DB.DateTime, nullable=False, default=datetime.utcnow)
    modified = DB.Column(DB.DateTime, onupdate=datetime.utcnow)
