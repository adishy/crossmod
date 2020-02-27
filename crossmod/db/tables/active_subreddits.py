from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from crossmod.db.tables import SubredditSettingsTable 
from crossmod.db.base import Base

class ActiveSubredditsTable(Base):
      __tablename__ = 'active_subreddits'
      id = Column(Integer, primary_key = True)
      subreddit = Column(String, ForeignKey('subreddit_settings.subreddit'))
      perform_action = Column(Boolean)