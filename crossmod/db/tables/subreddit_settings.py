from sqlalchemy import Column, Integer, String, UnicodeText, Boolean
import crossmod
from crossmod.db.base import Base

class SubredditSettingsTable(Base):
      __tablename__ = 'subreddit_settings'
      __table_args__ = {'extend_existing': True} 
      id = Column(Integer, primary_key = True)
      subreddit = Column(String(50), unique = True)
      subreddit_classifiers = Column(UnicodeText)
      norm_classifiers = Column(UnicodeText)
      perform_action = Column(Boolean, default = False)
      removal_config = Column(UnicodeText, default = '{ "agreement_score_threshold": 0.85, "norm_violation_score_threshold": 0.85  }')
