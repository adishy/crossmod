from sqlalchemy import Column, Integer, String, DateTime, Float, UnicodeText

'''
    Schema:
        CrossmodDBData:
            * Created At Timestamp    (column name: created_utc)        (Timestamp in UTC at which the comment was posted)
            * Ingested At Timestamp   (column_name: ingested_utc)        (Timestamp in UTC at which Crossmod ingested the comment)
            * Comment ID              (column name: id)                 (Reddit Comment ID)
            * Comment Body            (column name: body)
            * Toxicity Score          (column name: toxicity_score)
            * Crossmod Action         (column name: crossmod_action)
            * Author                  (column name: author)             (Reddit username of comment author)
            * Subreddit               (column name: subreddit)          (Subreddit name where the moderated Reddit comment was posted in)
            * Moderator Action        (column name: moderator_action)   (Action taken by moderator after Crossmod flagged a comment)
            * Banned By               (column name: banned_by)          (The name of the human moderator who removed the comment after Crossmod flagged the comment)
            * Banned At Timestamp     (column name: banned_at)          (Timestamp in UTC at which the comment was moderated on by a human moderator)
            * Agreement Score         (column name: agreement_score)
            * Norm Violation Score    (column name: norm_violation_score)

'''

class DataTable(Base):
      __tablename__ = 'crossmoddbdata'
      created_utc = Column(DateTime)
      ingested_utc = Column(DateTime)
      id = Column(String(50), primary_key = True)
      body = Column(UnicodeText)
      toxicity_score = Column(Float)
      crossmod_action = Column(String(50))
      author = Column(String(100))
      subreddit = Column(String(50))
      banned_by = Column(String(50))
      banned_at_utc = Column(DateTime)
      agreement_score = Column(Float)
      norm_violation_score = Column(Float)