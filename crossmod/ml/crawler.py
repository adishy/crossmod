from tenacity import retry, wait_exponential
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

#setup the subreddits list and action
subreddits_names = ['modbot_staging', 'Futurology', 'nba']
subreddits_action = [0, 0, 0]
subreddits_model = [total_subreddit_list, total_subreddit_list, total_subreddit_list]
subreddits_norm = [total_macro_norm_list, total_macro_norm_list, total_macro_norm_list]

# Use API or local crossmod instance
use_api = 1

def get_api_score(comment, subreddit_name):
    data = {"comments": [comment],
            "subreddit_list": subreddit_list,
            "macro_norm_list": macro_norm_list,
            "key": CrossmodConsts.CLIENT_API_KEY}
    r = requests.post(url= CrossmodConsts.CLIENT_API_ENDPOINT, json = data)
    return r.json()

def main():
    #setup the Reddit bot
    reddit = praw.Reddit(user_agent = CrossmodConsts.REDDIT_USER_AGENT,
                        client_id = CrossmodConsts.REDDIT_CLIENT_ID, 
                        client_secret = CrossmodConsts.REDDIT_CLIENT_SECRET,
                        username = CrossmodConsts.REDDIT_USERNAME, 
                        password = CrossmodConsts.REDDIT_PASSWORD)
    db = CrossmodDB()
    subreddits_to_listen = db.database_session.query(ActiveSubredditsTable).all()
    subreddits_listener = reddit.subreddit(subreddits_to_listen)


    ###list of white-listed authors whose content the bot would ignore
    whitelisted_authors = []
    whitelisted_authors.append(reddit.user.me().name)
        
    mod_list_string = ""
    moderators_list = ["thebiglebowskiii", 
					   "AutoModerator", 
					   "TransPlanetInjection", 
					   "Xenophon1", 
					   "ion-tom", 
					   "mind_bomber",
					   "Gobi_The_Mansoe",
					   "multi-mod",
					   "Buck-Nasty",
					   "Yosarian2",
					   "ImLivingAmongYou",
					   "lughnasadh"] #add mods to list of whitelisted_authors


    for moderator in moderators_list:
        mod_list_string = mod_list_string + "/u/" + moderator + " , "

    whitelisted_authors += moderators_list

    process_comments(db)

    db.database_session.exit()

def is_whitelisted(author):

def process_comments(db, subreddits_listener):
    start_time = datetime.fromtimestamp(datetime.now()))

    print("Crossmod starting at:", start_time.stftime('%Y-%m-%d %H:%M:%S')

    for comment in subreddits_listener.stream.comments():
        start = time.time()

        if comment == None:
            continue

        if comment.created_utc < start_time:
            continue

        subreddit_name = comment.subreddit.display_name

        print("r/", subreddit_name, "Comment: ", comment.body)

        if is_whitelisted(comment.author) or CrossmodFilters.apply_filters(comment.body)):
            print("Filtering comment:", comment.id, comment.body)
			### Write to CrossmodDB
            db.write(DataTable,
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

            ### Type 2: Use API
            try:
                body = get_api_score(comment.body, model_dict[subreddit_name], norm_dict[subreddit_name])
                api_agreement_score = body[0]['agreement_score']
                api_norm_violation_score = body[0]['norm_violation_score']
            except:
                api_agreement_score = -1
                api_norm_violation_score = -1
            print("Agreement score from crossmod API = ", api_agreement_score)
            backend_predictions['api_agreement_score'] = api_agreement_score
            backend_predictions['api_norm_violation_score'] = api_norm_violation_score


        ### Write to CrossmodDB
        # TODO: which table and which data should I store
        # db.write(created_utc = datetime.datetime.fromtimestamp(comment.created_utc),
		# 		ingested_utc = datetime.datetime.now(),
		# 		id = comment.id,
		# 		body = comment.body,
		# 		toxicity_score = toxicity_score,
		# 		crossmod_action = ACTION,
		# 		author = comment.author.name,
		# 		subreddit = comment.subreddit.display_name, 
		# 		banned_by = None,
		# 		banned_at_utc = None,
		# 		agreement_score = agreement_score,
		# 		norm_violation_score = norm_violation_score)
        
        if action_dict[comment.subreddit.display_name] == 0:
            end = time.time()
            print("processing time =", end - start, "seconds")
            continue

        ACTION = check_config(backend_predictions)
        print("Action = ", ACTION)

        end = time.time()
        print("processing time =", end - start, "seconds")

if __name__ == '__main__':
	main()