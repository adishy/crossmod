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
        
    def write(self, table_type, commit = True, **kwargs):
        try:
            table_data_entry = table_type(**kwargs)
            self.database_session.add(table_data_entry)
            
            if commit:
                self.database_session.commit()
        except Exception as e:
            print("Could not write data:")
            print(e)
            return