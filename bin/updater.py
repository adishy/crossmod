from crossmod.db.interface import CrossmodDB
from crossmod.environments.consts import CrossmodConsts
from crossmod.db.tables import DataTable
from crossmod.db.tables import UpdateStatusTable
import datetime
import praw
import sys
import click

class CrossmodDataTableUpdater:
    def __init__(self):
        self.REMOVED = "[removed]"
        self.DELETED = "[deleted]"

        self.db = CrossmodDB()

        self.session = self.db.database_session
        
        self.updated_count = 0

        #setup the Reddit bot
        self.reddit = praw.Reddit(user_agent = CrossmodConsts.REDDIT_USER_AGENT,
                                  client_id = CrossmodConsts.UPDATER_REDDIT_CLIENT_ID, 
                                  client_secret = CrossmodConsts.UPDATER_REDDIT_CLIENT_SECRET,
                                  username = CrossmodConsts.REDDIT_USERNAME, 
                                  password = CrossmodConsts.REDDIT_PASSWORD)

    def update_database_values(self):
        print("Starting data table update!")
        rows = self.db.database_session.query(DataTable).all()
        rows_queried = 0
        total = self.db.database_session.query(DataTable).count()
        for row in rows:
            self.change_moderated_value(row)    
            print("{} rows of {}\r\n".format(rows_queried, total))
            print("Updated count", self.updated_count)
            rows_queried += 1
        self.db.database_session.commit()

    def change_moderated_value(self, row):
        comment = self.reddit.comment(id = row.id)

        if comment.banned_at_utc != None and comment.banned_by != None:
            row.banned_by = comment.banned_by
            row.banned_at_utc = datetime.datetime.fromtimestamp(comment.banned_at_utc)

            self.db.database_session.commit()
            self.updated_count += 1

if __name__ == '__main__':
  CrossmodDataTableUpdater().update_database_values() 
