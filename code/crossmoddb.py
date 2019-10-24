import os
import sys
import csv
import datetime
from sqlalchemy import Column, Integer, String, DateTime, Float, UnicodeText
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

'''
    Schema:
        CrossmodDBData:
            * Created At Timestamp    (column name: created_utc)        (Timestamp in UTC at which the comment was posted)
            * Ingested At Timestamp   (column_name: ingested_at)        (Timestamp in UTC at which Crossmod ingested the comment)
            * Comment ID              (column name: id)                 (Reddit Comment ID)
            * Comment Body            (column name: body)
            * Toxicity Score          (column name: toxicity_score)
            * Crossmod Action         (column name: crossmod_action)
            * Author                  (column name: author)             (Reddit username of comment author)
            * Subreddit               (column name: subreddit)          (Subreddit name where the moderated Reddit comment was posted in)
            * Banned By               (column name: banned_by)          (The name of the human moderator who removed the comment after Crossmod flagged the comment)
            * Banned At Timestamp     (column name: banned_at)          (Timestamp in UTC at which the comment was moderated on by a human moderator)
'''

class CrossmodDBData(Base):
      __tablename__ = 'CrossmodDBData'
      created_utc = Column(DateTime)
      ingested_at = Column(DateTime)
      id = Column(String(50), primary_key=True)
      body = Column(UnicodeText)
      toxicity_score = Column(Float)
      crossmod_action = Column(String(50))
      author = Column(String(100))
      subreddit = Column(String(50))
      banned_by = Column(String(50))
      banned_at = Column(DateTime)


class CrossmodDB:
    def __init__(self, database_uri = 'sqlite:///sqlalchemy_example.db'):
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
        except:
            print("Could not write comment id: {} to the database".format(kwargs['id']))
            return

    def write_to_CSV(self):
        output_file = open('db_crossmod.csv', 'w')
        out = csv.writer(output_file)

        #includes column headers
        out.writerow(['created_utc', 'ingested_at', 'id', 'body', 'toxicity_score', 
        'crossmod_action', 'author', 'subreddit', 'banned_by', 'banned_at'])

        for row in db.database_session.query.all():
            out.writerow([row.created_utc, row.ingested_at, row.id, row.body, 
            row.toxicity_score, row.crossmod_action, row.author, row.subreddit, 
            row.banned_by, row.banned_at])
        
        #close the file after reading
        output_file.close()




def main():
    db = CrossmodDB()
    db.write(created_utc = datetime.datetime.now(),
    		 ingested_at = datetime.datetime.now(),
             id = 'b',
             body = 'b',
             toxicity_score = 23423.234234,
             crossmod_action = 'c',
             author = 'd',
             subreddit = "games", 
             banned_by = 'not_available',
             banned_at = None)

    row = db.database_session.query(CrossmodDBData).filter(CrossmodDBData.author == 'd')

if __name__ == "__main__":
    main()