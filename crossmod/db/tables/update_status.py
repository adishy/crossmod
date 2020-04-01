from sqlalchemy import Column, Integer, String, DateTime
import crossmod
from crossmod.db.base import Base

class UpdateStatusTable(Base):
    __tablename__ = 'crossmod_db_update_status'
    __table_args__ = {'extend_existing': True} 
    id = Column(Integer, primary_key = True)
    update_start_utc = Column(DateTime)
    update_end_utc = Column(DateTime)
    rows_updated = Column(Integer)
    last_row_id = Column(String(50))
