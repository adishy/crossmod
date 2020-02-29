from sqlalchemy import Column, Integer, String, UnicodeText, ForeignKey
import crossmod
from crossmod.db.base import Base

class SubredditSettingsTable(Base):
      __tablename__ = 'subreddit_settings'
      id = Column(Integer, primary_key = True)
      subreddit = Column(String(50))
      moderator_list = Column(UnicodeText)
      subreddit_classifiers = Column(UnicodeText)
      norm_classifiers = Column(UnicodeText)