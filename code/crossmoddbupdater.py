import praw
import pandas as pd
from crossmoddb import *

class CrossmodDBUpdater:
    def __init__(self):
        self.REMOVED = "[removed]"
        self.DELETED = "[deleted]"

        self.db = CrossmodDB()

        #load credentials for Reddit bot
        creds = pd.read_csv('../keys/crossmod-creds.txt')

        #setup the Reddit bot
        self.reddit = praw.Reddit(user_agent = 'Updating Crossmod database values (by /u/CrossModerator)',
                                  client_id = creds["CLIENT_ID"][0], 
                                  client_secret = creds["CLIENT_SECRET"][0],
                                  username = creds["USERNAME"][0], 
                                  password = creds["PASSWORD"][0])

    def update_database_values(self):
        rows = self.db.database_session.query(CrossmodDBData)

        for row in rows:
            self.update_moderated_value(row)

    def update_moderated_value(self, row):
        comment_id = row['id']
        comment = self.reddit.comment(id = comment_id)

        if str(comment.body) == self.REMOVED and str(comment.author) == self.DELETED:
            print(comment.id, comment.body, comment.author, comment.created_utc, comment.banned_at_utc, comment.banned_by)
            row.banned_by = comment.banned_by
            row.banned_at_utc = comment.banned_at_utc
            self.db.database_session.commit()
