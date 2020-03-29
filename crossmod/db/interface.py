from crossmod.helpers.consts import CrossmodConsts
from crossmod.db.base import Base
from crossmod.db.tables import DataTable
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime

class CrossmodDB:
    def __init__(self, database_uri = 'sqlite:///' + CrossmodConsts.DB_PATH):
        self.database_uri = database_uri
        self.database = create_engine(self.database_uri)
        Base.metadata.bind = self.database
        Base.metadata.create_all(self.database)
        self.DatabaseSession= sessionmaker(bind = self.database)
        self.database_session = self.DatabaseSession()
        
    def write(self, **kwargs):
        try:
            crossmod_data_entry = DataTable(**kwargs)
            self.database_session.add(crossmod_data_entry)
            self.database_session.commit()
        except Exception as e:
            print(e)
            print("Could not write comment id: {} to the database".format(kwargs['id']))
            return