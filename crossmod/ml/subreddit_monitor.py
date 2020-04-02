from crossmod.db.interface import CrossmodDB
from crossmod.environments.consts import CrossmodConsts
from crossmod.helpers.filters import CrossmodFilters
from crossmod.helpers.filters import CrossmodFilters
from crossmod.ml.moderation_settings import *
from crossmod.ml.classifiers import CrossmodClassifiers
from crossmod.db.tables import DataTable
from crossmod.db.tables import SubredditSettingsTable
from datetime import datetime
from sqlalchemy import func
from tenacity import retry, wait_exponential
import requests
import praw
import sys
import datetime
import time
import pytz

class CrossmodSubredditMonitor():
    """Provides an interface to monitor multiple subreddits by querying Crossmod's API"""
    
    def __init__(self):
      """Initializes db object and PRAW object and other vairables to track
         which subreddits to monitor"""

      # Crossmod database interface
      self.db = CrossmodDB()

      # PRAW interface to monitor subreddits
      self.reddit = praw.Reddit(user_agent = CrossmodConsts.MONITOR_REDDIT_USER_AGENT,
                                client_id = CrossmodConsts.MONITOR_REDDIT_CLIENT_ID, 
                                client_secret = CrossmodConsts.REDDIT_CLIENT_SECRET,
                                username = CrossmodConsts.REDDIT_USERNAME, 
                                password = CrossmodConsts.REDDIT_PASSWORD)
      
      # Who am I? I am Spider-Man.
      self.me = self.reddit.user.me()

      # Keeps track of how many subreddits are currently being monitored
      # (If this changes during monitor(), monitor() will be called again to
      # refresh the subreddit list from the db
      self.current_subreddits_count = self.number_of_subreddits()

    def number_of_subreddits(self):
      return self.db.database_session.query(func.count(SubredditSettingsTable.subreddit)).scalar()

    def should_perform_action(self, subreddit):
        """Queries database to check whether active moderation is required."""
        row = self.db.database_session.query(SubredditSettingsTable.perform_action).filter(SubredditSettingsTable.subreddit == subreddit).one()
        return row.perform_action


    def find_removal_consensus(self, comment, subreddit_name):
      """Finds removal consensus querying Crossmod's API."""
      subreddit_settings = self.db.database_session \
                               .query(SubredditSettingsTable) \
                               .filter(SubredditSettingsTable.subreddit == subreddit_name) \
                               .one()
      data = {"comments": [comment],
              "subreddit_list": subreddit_settings.subreddit_classifiers.split(','),
              "macro_norm_list": subreddit_settings.norm_classifiers.split(','),
              "key": CrossmodConsts.CLIENT_API_SUPER_KEY}
      result = requests.post(url= CrossmodConsts.CLIENT_API_ENDPOINT, json = data).json()

      if type(result) is not list or len(result) != 1:
        raise ValueError(f"Expected API response to be a list with a single comment, but got: {result}")
      
      return result[0]


    def is_whitelisted(self, author, subreddit):
      """Checks whether the author provided is a moderator of the subreddit in
         which the comment was posted."""
      moderator_list = [moderator.name for moderator in self.reddit.subreddit(subreddit).moderator()]
      moderator_list.append(self.me)
      return author in moderator_list


    def perform_action(self, comment, action, agreement_score, norm_violation_score):
      if action == "EMPTY":
        return

      elif action == "remove":
        print("Removing comment, and alerting moderator by modmail at:", time.time())
        self.reddit.subreddit(comment.subreddit.name) \
                   .modmail.create("[Comment removal by Crossmod] Crossmod performed a comment removal!", 
                                   f"Crossmod removed a comment with permalink [{comment.permalink}]", 
                                   self.me)
        comment.mod.remove()
        message = f"[Comment removal by Crossmod] Comment removal consensus:\nAgreement Score {agreement_score}, Norm Violation Score {norm_violation_score}"
        comment.mod.send_removal_message(message, title='ignored', type='public')
    
      elif action == "report":
        print("Reporting a comment and sending it to report queue at:", time.time())
        comment.report(f"Agreement Score: {agreement_score}/1.0, Norm Violation Score: {norm_violation_score}/1.0")
    
      elif action == "modmail":
        print("Sending a modmail at:", time.time())
        self.reddit.subreddit(comment.subreddit.name) \
        .modmail.create("[Alert by Crossmod] Comment exceeds removal consensus threshold!", 
                        f"A comment with permalink [{comment.permalink}] exceeded Crossmod's removal consensus threshold.", 
                        self.me)
  
    @retry(wait=wait_exponential(multiplier=1, min=4, max=10))
    def monitor(self):
      # PRAW interface used to stream comments from subreddits
      self.current_subreddits_count = self.number_of_subreddits()
      subreddits_listener = self.reddit.subreddit("+".join([row.subreddit for row in self.db.database_session.query(SubredditSettingsTable.subreddit).all()]))

      print("Crossmod started monitoring at:", (datetime.datetime.now(pytz.timezone('EST'))).strftime('%Y-%m-%d %H:%M:%S'), "EST")
      print("Currently moderating in :", ", ".join([f"r/{row.subreddit}" for row in self.db.database_session.query(SubredditSettingsTable.subreddit).filter(SubredditSettingsTable.perform_action == True).all()]))
      print("Currently listening to:", ", ".join([f"r/{row.subreddit}" for row in self.db.database_session.query(SubredditSettingsTable.subreddit).filter(SubredditSettingsTable.perform_action == False).all()]))
      print()

      for comment in subreddits_listener.stream.comments(skip_existing = True):
        print("______________________________________________\n")
        
        start = time.time()

        if comment == None or comment.body == '[removed]':
            continue

        subreddit_name = comment.subreddit.display_name
        print(f"Posted in r/{subreddit_name}:")
        print("Comment ID:", comment.id, "\nComment Body:", comment.body.replace('\n', ' '))

        if self.is_whitelisted(comment.author, subreddit_name) or CrossmodFilters.apply_filters(comment.body):
            print("Filtering comment:", comment.id, comment.body)
            self.db.write(DataTable,
                          created_utc = datetime.datetime.fromtimestamp(comment.created_utc),
                          ingested_utc = datetime.datetime.now(),
                          id = comment.id,
                          body = comment.body,
                          crossmod_action = "filtered",
                          author = comment.author.name,
                          subreddit = comment.subreddit.display_name, 
                          banned_by = None,
                          banned_at_utc = None,
                          agreement_score = -1.0,
                          norm_violation_score = -1.0)
            continue	

        removal_consensus = self.find_removal_consensus(comment.body, subreddit_name)
        agreement_score = removal_consensus['agreement_score']
        norm_violation_score = removal_consensus['norm_violation_score']
        
        print("Agreement score from Crossmod API:", agreement_score)
        print("Norm violation score from Crossmod API:", norm_violation_score)

        action = check_config(removal_consensus)

        ### Write to CrossmodDB
        self.db.write(DataTable, 
                      created_utc = datetime.datetime.fromtimestamp(comment.created_utc),
                      ingested_utc = datetime.datetime.now(),
                      id = comment.id,
                      body = comment.body,
                      crossmod_action = action,
                      author = comment.author.name,
                      subreddit = comment.subreddit.display_name, 
                      banned_by = None,
                      banned_at_utc = None,
                      agreement_score = agreement_score,
                      norm_violation_score = norm_violation_score)

        end = time.time()

        if self.should_perform_action(subreddit_name):
          self.perform_action(comment, 
                              action, 
                              agreement_score, 
                              norm_violation_score)

        print("Processing time for comment:", end - start, "seconds")
        print("______________________________________________\n") 

        number_of_subreddits_now = self.number_of_subreddits()
        if self.current_subreddits_count != number_of_subreddits_now:
          print("\nSubreddit(s) added! Restarting subreddit monitor..\n")
          self.current_subreddits_count = number_of_subreddits_now
          self.monitor()
