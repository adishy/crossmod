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

        UNREMOVED_COMMENT = "__label__unremoved"
        REMOVED_COMMENT = "__label__removed"

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
        f = open("tmp_data.train", "a")
        for row in rows:
            print(model.predict(row.comment))
            if row.banned_by == null: 
                f.write(UNREMOVED_COMMENT)
            elif row.banned_by == null: 
                f.write(REMOVED_COMMENT)
            f.write(" " + row.comment)
        f.close()



if __name__ == "__main__":
    test = retraining()
    start = 0
    end = datetime.datetime.now()
    test.train("Futurology", start, end)