from crossmod.db.interface import CrossmodDB
from crossmod.db.tables.data import DataTable
from crossmod.helpers.consts import *
import fasttext
import datetime



class retraining():
    def __init__(self):
        # Crossmod database interface
        self.db = CrossmodDB()

        self.session = self.db.database_session

    def train(self, subreddit, start_time, end_time):
        '''
        sqlite> select count(*) from crossmoddbdata where banned_by is not null;
        7942
        sqlite> select count(*) from crossmoddbdata where banned_by is not null and crossmod_action == "report";
        481
        sqlite> select count(*) from crossmoddbdata where banned_by is null and crossmod_action == "report";
        4335
        '''
        rows = self.session.query(DataTable).filter(DataTable.subreddit == subreddit, 
                                                    DataTable.crossmod_action == "report",
                                                    DataTable.ingested_utc > start_time, 
                                                    DataTable.ingested_utc <= end_time).limit(500)

        f = open("tmp_data.txt", "a")
        
        for row in rows:
            print(row)

        f.close()


if __name__ == "__main__":
    test = retraining()
    start = 0
    end = datetime.datetime.now()
    test.train("Futurology", start, end)