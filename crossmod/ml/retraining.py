from crossmod.db.interface import CrossmodDB
from crossmod.db.tables.data import DataTable
from crossmod.helpers.consts import *
import fasttext

class retraining():
    def __init__(self):
        # Crossmod database interface
        self.db = CrossmodDB()

        self.session = self.db.database_session

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

        for row in rows:
            print(model.predict(row.comment))

        


if __name__ == "__main__":
    test = retraining()
    test.train("Futurology")