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

        self.UNREMOVED_COMMENT = "__label__unremoved"
        self.REMOVED_COMMENT = "__label__removed"

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
                                                    DataTable.ingested_utc <= end_time).limit(1000)


        f = open("./tmp_data.train", "a")

        for row in rows:
            # print(model.predict(row.body))
            if row.banned_by != None: 
                f.write(self.UNREMOVED_COMMENT)
            else:
                f.write(self.REMOVED_COMMENT)
            f.write(" " + row.body + "\n")

        f.close()

        model = fasttext.train_supervised(input="./tmp_data.train", epoch = 25)

        print(model.test("old.valid"))

        old_model = fasttext.load_model(CrossmodConsts.get_subreddit_classifier("Futurology"))

        print(old_model.test("old.valid"))

        filename = "retrain_" + subreddit + '.bin'
        model.save_model(filename)
        

if __name__ == "__main__":
    test = retraining()
    print("testing Futurology")
    end = datetime.datetime.now()
    test.train("Futurology", 0, end)
