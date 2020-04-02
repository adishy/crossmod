from crossmod.db.base import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean
import crossmod
import datetime

class UsersTable(Base):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True} 
    email = Column(String(254), primary_key = True)
    password_hash = Column(String(256), nullable = False)
    admin = Column(Boolean, default = False)
    created_at_utc = Column(DateTime, default = datetime.datetime.utcnow)