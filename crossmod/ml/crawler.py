import praw
import sys
import datetime
import pandas as pd
import time
from tenacity import retry, wait_exponential
from getPredictions import *
from config import *
from consts import CrossmodConsts
from db import CrossmodDB
from classifiers import CrossmodClassifiers
from filters import CrossmodFilters
import requests
###get toxicity score from Perspective API
from googleapiclient import discovery


## Config Variables ##
API_ENDPOINT = "http://crossmod.ml/api/v1/get-prediction-scores"
API_KEY = "ABCDEFG"

#list of subreddits to use for voting (i.e., aggregating the predictions from back-end ensemble of classifiers)
subreddits_limit = 100
total_subreddit_list = list(pd.read_csv("../data/study_subreddits.csv", names = ["subreddit"])["subreddit"][:subreddits_limit])
total_macro_norm_list = list(pd.read_csv('../data/macro-norms.txt', names = ['macronorms'])['macronorms'])

#setup the subreddits list and action
subreddits_names = ['modbot_staging', 'Futurology', 'nba']
subreddits_action = [0, 0, 0]
subreddits_model = [total_subreddit_list, total_subreddit_list, total_subreddit_list]
subreddits_norm = [total_macro_norm_list, total_macro_norm_list, total_macro_norm_list]

# Use API or local crossmod instance
use_api = 1

def get_api_score(comment, subreddit_list, macro_norm_list):
    comments = []
    comments.append(comment)
    data = {"comments": comments,
            "subreddit_list": subreddit_list,
            "macro_norm_list": macro_norm_list,
            "key": API_KEY}
    r = requests.post(url= API_ENDPOINT, json = data)
    return r.json()

def get_toxicity_score(comment):
    analyze_request = {
      'comment': { 'text': comment},
      'requestedAttributes': {'TOXICITY': {}}
    }
    response = service.comments().analyze(body=analyze_request).execute()
    toxicity_score = response['attributeScores']['TOXICITY']['summaryScore']['value']
    return toxicity_score

def main():
    #generate Perspective API client object dynamically based on service name and version. 
    Perspective_API_KEY = CrossmodConsts.PERSPECTIVE_API_SECRET
    service = discovery.build('commentanalyzer', 'v1alpha1', developerKey=Perspective_API_KEY)

    #setup the Reddit bot
    reddit = praw.Reddit(user_agent = CrossmodConsts.REDDIT_USER_AGENT,
                        client_id = CrossmodConsts.REDDIT_CLIENT_ID, 
                        client_secret = CrossmodConsts.REDDIT_CLIENT_SECRET,
                        username = CrossmodConsts.REDDIT_USERNAME, 
                        password = CrossmodConsts.REDDIT_PASSWORD)
    multi_reddits_names = ''

    action_dict = dict(zip(subreddits_names, subreddits_action))
    model_dict = dict(zip(subreddits_names, subreddits_model))
    norm_dict = dict(zip(subreddits_names, subreddits_norm))
    print("Crawling to these subreddits (with action, subreddits, macro norm): ")
    for name in subreddits_names:
        multi_reddits_names += name
        multi_reddits_names += '+'
        print("\t", name, action_dict[name], model_dict[name], norm_dict[name])

    multi_reddits = reddit.subreddit(multi_reddits_names)

    db = CrossmodDB()

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

    if use_api == 1:
        classifiers = None
    else:
        classifiers = CrossmodClassifiers(subreddits = subreddit_list, norms = macro_norm_list)

    process_comments(multi_reddits, action_dict, model_dict, norm_dict, classifiers, db, whitelisted_authors)

    db.database_session.exit()


def process_comments(multi_reddits, action_dict, model_dict, norm_dict, classifiers, db, whitelisted_authors):
    
    start_time = time.time()

    print("Crossmod = ACTIVE, starting at t = ", start_time)
    print("Whitelisted authors:", whitelisted_authors)

    me = whitelisted_authors[0]

    for comment in multi_reddits.stream.comments():
        start = time.time()

        if comment == None:
            continue

        if comment.created_utc < start_time:
            continue

        subreddit_name = comment.subreddit.display_name

        print("r/", subreddit_name, "Comment: ", comment.body)

        if comment.author != me and (comment.author in whitelisted_authors or CrossmodFilters.apply_filters(comment.body)):
            print("Filtering comment:", comment.id, comment.body)
			### Write to CrossmodDB
            db.write(created_utc = datetime.datetime.fromtimestamp(comment.created_utc),
					ingested_utc = datetime.datetime.now(),
					id = comment.id,
					body = comment.body,
					toxicity_score = -1.0,
					crossmod_action = "filtered",
					author = comment.author.name,
					subreddit = comment.subreddit.display_name, 
					banned_by = None,
					banned_at_utc = None,
					agreement_score = -1.0,
					norm_violation_score = -1.0)
            continue	

        backend_predictions = {}

        ### Type 1: Use toxicity scores from Perspective API to make decisions
        # DISABLED NOW
        # try:
        #     toxicity_score = get_toxicity_score(comment.body)       
        # except:
        #     toxicity_score = -1.0
        # print("Toxicity score from Perspective API = ", toxicity_score)
        # backend_predictions['toxicity_score'] = toxicity_score
        
        if use_api == 1:
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
        else:
            ### Type 3: Use prediction from crossmod classifiers
            try:
                comment_value = comment.body
                backend_predictions.update(classifiers.get_result(comment_value))
                print("Number of subreddit classifiers agreeing to remove comment = ", backend_predictions['agreement_score'])
                print("Number of norms violated = ", backend_predictions['norm_violation_score'])
            except Exception as ex:
                print(ex)
                continue
            agreement_score = backend_predictions['agreement_score']
            norm_violation_score = backend_predictions['norm_violation_score']


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