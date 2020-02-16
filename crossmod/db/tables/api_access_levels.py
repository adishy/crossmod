from sqlalchemy import Column, Integer, String
import crossmod
from crossmod.db.base import Base

'''
    Schema:
        api_access_level_db:
            * Access Level ID:               (column_name: access_level_id)         (Access Level 0-5)
            * Access Level Rate Limit:       (column_name: access_level_limit)      (Rate limit associated with each access level)
'''

class ApiAccessLevelTable(Base):
      __tablename__ = 'api_access_level_db'
      access_level_id = Column(Integer, primary_key = True)
      access_level_limit = Column(String(100))
