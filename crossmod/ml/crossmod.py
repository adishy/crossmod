from tenacity import retry, wait_exponential
from datetime import datetime
from crossmod.ml.moderation_settings import *
from crossmod.helpers.consts import CrossmodConsts
from crossmod.db.interface import CrossmodDB
from crossmod.ml.classifiers import CrossmodClassifiers
from crossmod.helpers.filters import CrossmodFilters
from crossmod.db.tables import DataTable
from crossmod.db.tables import SubredditSettingsTable
from crossmod.db.tables import ActiveSubredditsTable
import requests
import praw
import sys
import datetime
import pandas as pd
import time

class CrossmodSubredditMonitor():
    """Provides an interface to monitor multiple subreddits by querying Crossmod's API"""
    
    def __init__(self):
      """Initializes CrossmodMonitor members"""

      # Crossmod database interface
      self.db = CrossmodDB()

      # PRAW interface to monitor subreddits
      self.reddit = praw.Reddit(user_agent = CrossmodConsts.REDDIT_USER_AGENT,
                                client_id = CrossmodConsts.REDDIT_CLIENT_ID, 
                                client_secret = CrossmodConsts.REDDIT_CLIENT_SECRET,
                                username = CrossmodConsts.REDDIT_USERNAME, 
                                password = CrossmodConsts.REDDIT_PASSWORD)

      # Query database to find which subreddits to listen to and whether to 
      # only simulate moderation actions for each subreddit
      self.subreddits_to_listen_and_remove = [{row['subreddit']: row['perform_action']} \ 
                                              for row in self.db.database_session.query(ActiveSubredditsTable).all()]
      
      # PRAW interface used to stream comments from subreddits
      self.subreddits_listener = self.reddit.subreddit(self.subreddits_to_listen.keys())


    def find_removal_consensus(self, comment, subreddit_name):
      """Finds removal consensus querying Crossmod's API"""
      subreddit_settings = db.database_session \
                             .query(SubredditSettingsTable) \
                             .filter(SubredditSettingsTable.subreddit == subreddit_name) \
                             .one()
      data = {"comments": [comment],
              "subreddit_list": subreddit_settings['subreddit_classifiers'].split(','),
              "macro_norm_list": subreddit_settings['norm_classifiers'].split(','),
              "key": CrossmodConsts.CLIENT_API_SUPER_KEY}
      result = requests.post(url= CrossmodConsts.CLIENT_API_ENDPOINT, json = data)
      return result.json()[0]

    def is_whitelisted(self, author, subreddit):
      moderator_list = self.db.database_session.query(SubredditSettingsTable.moderator_list).filter(subreddit = subreddit).one().split(",")
      return author in moderator_list

    def monitor(self):
      print("Crossmod starting at:", start_time.stftime('%Y-%m-%d %H:%M:%S')
      print()
      print()
      print("________________________\n\n\")

      for comment in self.subreddits_listener.stream.comments():
        start = time.time()

        if comment == None:
            continue

        # if comment.created_utc < start_time:
        #     continue

        subreddit_name = comment.subreddit.display_name
        print("Posted in r/", subreddit_name, ":\n", "Comment ID: ", comment.id, " Body:\n" comment.body, "\n\n")

        if self.is_whitelisted(comment.author) or CrossmodFilters.apply_filters(comment.body)):
            print("Filtering comment:", comment.id, comment.body)
			      self.db.write(DataTable,
                          created_utc = datetime.fromtimestamp(comment.created_utc),
                          ingested_utc = datetime.now(),
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

        action = check_config(backend_predictions)

        ### Write to CrossmodDB
        self.db.write(DataTable, 
                      created_utc = datetime.fromtimestamp(comment.created_utc),
                      ingested_utc = datetime.now(),
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

        if self.subreddits_to_listen_or_remove[subreddit_name]:
          self.perform_action(comment)

        print("Processing time for comment:", end - start, "seconds")
        print("________________________")


