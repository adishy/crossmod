from cromssmod.helpers.consts import *
from crossmod.db.interface import *
import datetime
import praw
import sys
import click

class CrossmodDBUpdater:
    def __init__(self):
        self.REMOVED = "[removed]"
        self.DELETED = "[deleted]"

        self.db = CrossmodDB()

        self.session = self.db.database_session

        #setup the Reddit bot
        self.reddit = praw.Reddit(user_agent = CrossmodConsts.REDDIT_USER_AGENT,
                                  client_id = CrossmodConsts.REDDIT_CLIENT_ID, 
                                  client_secret = CrossmodConsts.REDDIT_CLIENT_SECRET,
                                  username = CrossmodConsts.REDDIT_USERNAME, 
                                  password = CrossmodConsts.REDDIT_PASSWORD)

    def update_database_values(self):
        status_count = self.session.query(CrossmodDBUpdateStatus).count()
        if(status_count == 0):
            rows = self.session.query(CrossmodDBData)
        else:
            starting_row_id = self.session.query(CrossmodDBUpdateStatus).order_by(CrossmodDBUpdateStatus.id.desc()).first().last_row_id
            starting_row = self.session.query(CrossmodDBData).filter(CrossmodDBData.id == starting_row_id).first()
            rows = self.session.query(CrossmodDBData).filter(CrossmodDBData.ingested_utc > starting_row.ingested_utc, 
                                                             CrossmodDBData.ingested_utc <= starting_row.ingested_utc + datetime.timedelta(days = 7))
        update_start_utc = datetime.datetime.now()
        rows_updated = 0
        total = rows.count()
        for row in rows:
            if(rows_updated == total - 1):
                last_row_id = row.id
            self.change_moderated_value(row, rows_updated)    
            print("{} rows of {}\r\n".format(rows_updated, total))
            rows_updated += 1
        update_end_utc = datetime.datetime.now()

        if rows_updated > 0:
            status_entry = CrossmodDBUpdateStatus(id = status_count + 1,
                                                  update_end_utc = update_end_utc,
                                                  rows_updated = rows_updated,
                                                  last_row_id = last_row_id)
            self.session.add(status_entry)
            self.session.commit()

    def change_moderated_value(self, row, count):
        comment = self.reddit.comment(id = row.id)

        if comment.banned_at_utc != None and comment.banned_by != None:
            row.banned_by = comment.banned_by
            row.banned_at_utc = datetime.datetime.fromtimestamp(comment.banned_at_utc)

            if count % 20 == 0:
                self.db.database_session.commit()

    def simple_update(self, interval_in_secs):
        while(True):
            current_requery_timestamp = datatime.datetime.now()
            last_requery_timestamp = self.session.query(CrossmodDBUpdateStatus).order_by(CrossmodDBUpdateStatus.id.desc()).first().update_end_utc
            comments = self.session.query(CrossmodDBData.created_utc < current_requery_timestamp, CrossmodDBData.created_utc > last_requery_timestamp)
            count = 0
            total = comments.count()
            for comment in comments:
                if count == total - 1:
                    last_comment_id = comment.id
                change_moderated_value(comment)
                count += 1
            status_entry = CrossmodDBUpdateStatus(id = status_count + 1,
                                                  update_end_utc = update_end_utc,
                                                  rows_updated = rows_updated,
                                                  last_row_id = last_comment_id)
            self.session.add(status_entry)
            sleep(interval_in_secs)

@click.command()
@click.option('-m', '--mode',
              type=click.Choice(['simple', 'repeated'], case_sensitive=False),
              help='Choose which mode to start requerying in: \'simple\' or \'repeated\'')
@click.option('-i', '--interval', help='Update interval in hours', default=2.0, show_default=True)
def main(mode, interval):
    interval_in_secs = interval * 60 * 60 # hours to seconds
    updater = CrossmodDBUpdater()
    if mode == 'simple':
        print("Mode:", "simple")
        print("Interval:", interval, "hours")
        updater.simple_update(interval_in_secs)
    elif mode == 'repeated':    
        print("Mode:", "repeated")
        print("Intervals:", interval, interval * 8, interval * "hours")
        updater.update_database_values()
    else:
        click.echo(click.get_current_context().get_help())

if __name__ == "__main__":
    main()
