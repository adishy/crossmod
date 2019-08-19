import praw
import pandas as pd
from getPredictions import *
from config import *

###get toxicity score from Perspective API
from googleapiclient import discovery

# use_classifiers = 0
use_classifiers = 1

def get_toxicity_score(comment):
    analyze_request = {
      'comment': { 'text': comment},
      'requestedAttributes': {'TOXICITY': {}}
    }

    response = service.comments().analyze(body=analyze_request).execute()
    toxicity_score = response['attributeScores']['TOXICITY']['summaryScore']['value']
    return toxicity_score

###main()
#generate Perspective API client object dynamically based on service name and version.
API_KEY = pd.read_csv('../keys/perspective-api-key.txt', names = ['key'])['key'][0]
service = discovery.build('commentanalyzer', 'v1alpha1', developerKey=API_KEY)
###

#load credentials for Reddit bot
creds = pd.read_csv('../keys/crossmod-creds.txt')

#setup the Reddit bot
reddit = praw.Reddit(user_agent='Testing Crossmod (by /u/CrossModerator)',
                     client_id=creds["CLIENT_ID"][0], client_secret=creds["CLIENT_SECRET"][0],
                     username=creds["USERNAME"][0], password=creds["PASSWORD"][0])

staging_subreddit = "modbot_staging"
subreddit = reddit.subreddit(staging_subreddit) #Select the subreddit for Crossmod to work on 

print(subreddit.title) #Prints title of subreddit
print(subreddit.description)  #Prints description of subreddit
print(reddit.user.me()) #Prints your username

###list of white-listed authors whose content the bot would ignore
whitelisted_authors = []
whitelisted_authors.append(reddit.user.me())

mod_list_string = ""
moderators_list = ["thebiglebowskiii"] #add mods to list of whitelisted_authors
for moderator in moderators_list:
	mod_list_string = mod_list_string + "/u/" + moderator + " , "

###list of subreddits to use for voting (i.e., aggregating the predictions from back-end ensemble of classifiers)
subreddits_limit = 100
subreddit_list = pd.read_csv("../data/study_subreddits.csv", names = ["subreddit"])["subreddit"][:subreddits_limit]
macro_norm_list = pd.read_csv('../data/macro-norms.txt', names = ['macronorms'])['macronorms']

total_num_comments = 0
num_processed = 0

###get current time when starting scripts (will ignore comments made before this timestamp)-
import time
start_time = time.time()

print("Crossmod = ACTIVE, starting at t = ", start_time)

for comment in subreddit.stream.comments(): #to iterate through the comments and stream it live
	total_num_comments += 1
	
	if (comment.created_utc < start_time) | (comment.author in whitelisted_authors):
		continue
	
	num_processed += 1
	print(num_processed, comment.body, comment.created_utc)

	### Get back-end predictions and score the comment! 

	### Type 1: Use toxicity scores from Perspective API to make decisions -
	try:
		toxicity_score = get_toxicity_score(comment.body)
	except:
		toxicity_score = -1.0

	print("Toxicity score from Perspective API = ", toxicity_score)

	backend_predictions = {}
	backend_predictions['toxicity_score'] = toxicity_score

	if use_classifiers == 1:
		### Type 2: Score using ensemble of subreddit classifiers in back-end (cross-community learning)
		###score comment using subreddit classifier predictions - currently supports batch queries, i.e., a list of comments
		comment_list = []
		comment_list.append(comment.body)

		###obtain predictions from subreddit classifiers
		try:
			predictions = get_classifier_predictions(comment_list, subreddit_list)
		except Exception as ex:
			print(ex)
			continue
		for col in predictions.drop('comment', axis = 1).columns:
			backend_predictions[col] = predictions[col][0]
		###calculate sum of votes from subreddit classifier predictions (agreement_score)
		predictions['sum_votes'] = predictions.drop('comment', axis = 1).sum(axis = 1)
		agreement_score = predictions['sum_votes'][0]
		backend_predictions['agreement_score'] = agreement_score
		print("Number of subreddit classifiers agreeing to remove comment = ", agreement_score)
		### Type 3: Score using ensemble of macro norm classifiers in back-end
		###score comment using macro norm classifier predictions - currently supports batch queries, i.e., a list of comments
		predictions = get_macronorm_classifier_predictions(comment_list, macro_norm_list)
		for col in predictions.drop('comment', axis = 1).columns:
			backend_predictions[col] = predictions[col][0]
		predictions['sum_votes'] = predictions.drop('comment', axis = 1).sum(axis = 1)
		norm_violation_score = predictions['sum_votes'][0]
		backend_predictions['norm_violation_score'] = norm_violation_score
	### Compute the appropriate action to be performed from the config file based on back-end predictions! 
	ACTION = check_config(backend_predictions)
	print("Action = ", ACTION)
	if ACTION == "remove":
		###REMOVE: if toxicity score returned by the Perspective API > 90%, directly remove from thread and send to mod queue.
		print("Removing comment, and alerting moderator by modmail at t=", time.time())
		subreddit.modmail.create("[Comment removal by Crossmod] Toxicity score = " + str(toxicity_score), "Comment's permalink = " + comment.permalink, "thebiglebowskiii")
		comment.mod.remove()
		message = "[Comment removal by Crossmod] Toxicity score = " + str(toxicity_score)
		comment.mod.send_removal_message(message, title='ignored', type='public')
		continue
	elif ACTION == "report":
		###REPORT: if toxicity score returned by the Perspective API in the range [80%, 90%), report comment and send to mod (& report) queue for review (doesn't remove from thread automatically).
		print("Reporting a comment and sending it to report queue at t=", time.time())
		comment.report("Toxicity = " + str(toxicity_score))
		message = "Looks like we got ourselves a toxic comment! Toxicity score = " + str(toxicity_score)
		comment.reply(message)
		continue
	elif ACTION == "modmail":
		###MODMAIL: if toxicity score returned by the Perspective API in the range [75%, 80%), send a modmail alerting moderators.
		print("Sending a modmail at t=", time.time())
		subreddit.modmail.create("[Alert by Crossmod] toxicity_score >= 75%", "Comment's permalink = " + comment.permalink, "thebiglebowskiii")
		continue
	else:
		continue
		
print("Modbot = INACTIVE, ending at t = ", time.time())
print(total_num_comments, num_processed)