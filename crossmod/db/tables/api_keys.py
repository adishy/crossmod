from sqlalchemy import Column, Integer, String, ForeignKey
import crossmod
from crossmod.db.base import Base
from crossmod.db.tables.api_access_levels import ApiAccessLevelTable

'''
    Schema:
        api_key_db:
            * API Key:                  (column_name: api_key)
            * API Key Email:            (column_name: email)
            * API Key ID:               (column_name: id)
            * API Key Access Level:     (column_name: access_level)      (Access Level 0-5 which determines rate limit, tied to api_key)
'''

class ApiKeyTable(Base):
      __tablename__ = 'api_key_db'
      id = Column(Integer, primary_key = True)
      email = Column(String)
      api_key = Column(String(40))
      access_level = Column(Integer, ForeignKey('api_access_level_db.access_level_limit'))
