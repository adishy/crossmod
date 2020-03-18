from crossmod.db.interface import CrossmodDB
from crossmod.db.tables.data import DataTable
from crossmod.helpers.consts import *
import fasttext



class retraining():
    def __init__(self):
        # Crossmod database interface
        self.db = CrossmodDB()

        self.session = self.db.database_session

        UNREMOVED_COMMENT = "__label__unremoved"
        REMOVED_COMMENT = "__label__removed"

    def train(self, subreddit):
        '''
        sqlite> select count(*) from crossmoddbdata where banned_by is not null;
        7942
        sqlite> select count(*) from crossmoddbdata where banned_by is not null and crossmod_action == "report";
        481
        sqlite> select count(*) from crossmoddbdata where banned_by is null and crossmod_action == "report";
        4335
        '''
        rows = self.session.query(DataTable).filter(DataTable.subreddit == subreddit, 
                                                    DataTable.crossmod_action == "report").limit(500)

        model = fasttext.load_model(CrossmodConsts.get_subreddit_classifier(subreddit))

        f = open("tmp_data.train", "a")
        for row in rows:
            print(model.predict(row.comment))
            if row.banned_by == null: 
                f.write(UNREMOVED_COMMENT)
            elif row.banned_by == null: 
                f.write(REMOVED_COMMENT)
            f.write(" " + row.comment)
        f.close()

        # retraining comes here.

        


if __name__ == "__main__":
    test = retraining()
    test.train("Futurology")