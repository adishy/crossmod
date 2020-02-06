import os
import sys
import csv
import datetime
from sqlalchemy import Column, Integer, String, DateTime, Float, UnicodeText
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from consts import *

Base = declarative_base()

'''
    Schema:
        CrossmodDBData:
            * Created At Timestamp    (column name: created_utc)        (Timestamp in UTC at which the comment was posted)
            * Ingested At Timestamp   (column_name: ingested_utc)        (Timestamp in UTC at which Crossmod ingested the comment)
            * Comment ID              (column name: id)                 (Reddit Comment ID)
            * Comment Body            (column name: body)
            * Toxicity Score          (column name: toxicity_score)
            * Crossmod Action         (column name: crossmod_action)
            * Author                  (column name: author)             (Reddit username of comment author)
            * Subreddit               (column name: subreddit)          (Subreddit name where the moderated Reddit comment was posted in)
            * Moderator Action        (column name: moderator_action)   (Action taken by moderator after Crossmod flagged a comment)
            * Banned By               (column name: banned_by)          (The name of the human moderator who removed the comment after Crossmod flagged the comment)
            * Banned At Timestamp     (column name: banned_at)          (Timestamp in UTC at which the comment was moderated on by a human moderator)
            * Agreement Score         (column name: agreement_score)
            * Norm Violation Score    (column name: norm_violation_score)

'''

class CrossmodDBData(Base):
      __tablename__ = 'crossmoddbdata'
      created_utc = Column(DateTime)
      ingested_utc = Column(DateTime)
      id = Column(String(50), primary_key = True)
      body = Column(UnicodeText)
      toxicity_score = Column(Float)
      crossmod_action = Column(String(50))
      author = Column(String(100))
      subreddit = Column(String(50))
      banned_by = Column(String(50))
      banned_at_utc = Column(DateTime)
      agreement_score = Column(Float)
      norm_violation_score = Column(Float)

class CrossmodDBUpdateStatus(Base):
    __tablename__ = 'crossmod_db_update_status'
    id = Column(Integer, primary_key = True)
    update_start_utc = Column(DateTime)
    update_end_utc = Column(DateTime)
    rows_updated = Column(Integer)
    last_row_id = Column(String(50))

class CrossmodDB:
    def __init__(self, database_uri = 'sqlite:///' + CrossmodConsts.DB_PATH):
        self.database_uri = database_uri
        self.database = create_engine(self.database_uri)
        Base.metadata.bind = self.database
        Base.metadata.create_all(self.database)
        self.DatabaseSession= sessionmaker(bind = self.database)
        self.database_session = self.DatabaseSession()
        
    def write(self, **kwargs):
        try:
            crossmod_data_entry = CrossmodDBData(**kwargs)
            self.database_session.add(crossmod_data_entry)
            self.database_session.commit()
        except Exception as e:
            print(e)
            print("Could not write comment id: {} to the database".format(kwargs['id']))
            return

def main():
    print(CrossmodConsts.DB_PATH)
    db = CrossmodDB()

if __name__ == "__main__":
    main()
