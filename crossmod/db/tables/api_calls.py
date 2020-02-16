from sqlalchemy import Column, Integer, String, DateTime
import crossmod
from crossmod.db.base import Base
from crossmod.db.api_acces_levels import ApiAccessLevelTable

'''
    Schema:
        api_call_db:
            * API Call ID:              (column_name: id)
            * API Call Key:             (column_name: api_key)
            * API Call Access Level:    (column_name: access_level)               (Access Level 0-5 which determines rate limit, tied to api_key)
            * # of Queries in call:     (column_name: num_of_queries)             (Number of comments queried through request)
            * Call Received Timestamp   (column name: call_received_utc)          (Timestamp in UTC at which the call was received)
            * Call Returned Timestamp   (column_name: call_returned_utc)          (Timestamp in UTC at which the call was returned)
'''

class ApiCallTable(Base):
      __tablename__ = 'api_call_db'
      id = Column(Integer, primary_key = True)
      api_key = Column(String(40))
      access_level = Column(Integer, foreign_key('api_access_level_db.access_level_limit'))
      num_of_queries = Column(Integer)
      call_received_utc = Column(DateTime)
      call_returned_utc = Column(DateTime)
