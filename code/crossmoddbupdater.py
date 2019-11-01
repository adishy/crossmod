import datetime
import praw
from crossmodconsts import *
from crossmoddb import *

class CrossmodDBUpdater:
    def __init__(self):
        self.REMOVED = "[removed]"
        self.DELETED = "[deleted]"

        self.db = CrossmodDB()

        #setup the Reddit bot
        self.reddit = praw.Reddit(user_agent = CrossmodConsts.REDDIT_USER_AGENT,
                                  client_id = CrossmodConsts.REDDIT_CLIENT_ID, 
                                  client_secret = CrossmodConsts.REDDIT_CLIENT_SECRETS,
                                  username = CrossmodConsts.REDDIT_USERNAME, 
                                  password = CrossmodConsts.REDDIT_PASSWORD)

    def update_database_values(self):
        rows = self.db.database_session.query(CrossmodDBData)

        count = 0
        total = rows.count()

        for row in rows:
            self.change_moderated_value(row)
            print("{} rows of {}\r\n".format(count, total))
            count += 1

    def change_moderated_value(self, row):
        comment = self.reddit.comment(id = row.id)

        if comment.banned_at_utc != None and comment.banned_by != None:
            row.banned_by = comment.banned_by
            row.banned_at_utc = datetime.datetime.fromtimestamp(comment.banned_at_utc)
            self.db.database_session.commit()

def main():
    updater = CrossmodDBUpdater()
    updater.update_database_values()

if __name__ == "__main__":
    main()
