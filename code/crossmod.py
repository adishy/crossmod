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

###get toxicity score from Perspective API
from googleapiclient import discovery

# Usage: python3 crossmod.py modbot_staging 1 1
if len(sys.argv) != 4:
	print("Usage: python3 crossmod.py <subreddit-name> <perform-action [1, 0]> <use-classifiers [1, 0]>")
	print("Example:")
	print("  python3 crossmod.py modbot_staging 1 1")
	print("  starts Crossmod to run on the subreddit modbot_staging, will actively flag comments and use Crossmod's ML backend")
	exit(1);	
else:
	staging_subreddit = sys.argv[1]
	perform_action = bool(int(sys.argv[2]))
	use_classifiers = int(sys.argv[3])

print("Staging subredddit: ", staging_subreddit)
print("Perform action: ", perform_action)
print("Use classifiers: ", use_classifiers)

def get_toxicity_score(comment):
    analyze_request = {
      'comment': { 'text': comment},
      'requestedAttributes': {'TOXICITY': {}}
    }

    response = service.comments().analyze(body=analyze_request).execute()
    toxicity_score = response['attributeScores']['TOXICITY']['summaryScore']['value']
    return toxicity_score


def main():
	###main()
	#generate Perspective API client object dynamically based on service name and version.
	API_KEY = CrossmodConsts.PERSPECTIVE_API_SECRET
	service = discovery.build('commentanalyzer', 'v1alpha1', developerKey=API_KEY)
	###


	#setup the Reddit bot
	reddit = praw.Reddit(user_agent = CrossmodConsts.REDDIT_USER_AGENT,
						client_id = CrossmodConsts.REDDIT_CLIENT_ID, 
						client_secret = CrossmodConsts.REDDIT_CLIENT_SECRET,
						username = CrossmodConsts.REDDIT_USERNAME, 
						password = CrossmodConsts.REDDIT_PASSWORD)

	subreddit = reddit.subreddit(staging_subreddit) #Select the subreddit for Crossmod to work on 

	db = CrossmodDB()

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
	subreddit_list = list(pd.read_csv("../data/single_study_subreddits.csv", names = ["subreddit"])["subreddit"][:subreddits_limit])
	macro_norm_list = list(pd.read_csv('../data/macro-norms.txt', names = ['macronorms'])['macronorms'])

	classifiers = CrossmodClassifiers(subreddits = subreddit_list, 
									  norms = macro_norm_list)


	process_comments(subreddit, classifiers, db, whitelisted_authors, subreddit_list, macro_norm_list)
			
	db.database_session.exit()

@retry(wait=wait_exponential(multiplier=1, min=4, max=10))
def process_comments(subreddit, classifiers, db, whitelisted_authors, subreddit_list, macro_norm_list):
	total_num_comments = 0
	num_processed = 0

	###get current time when starting scripts (will ignore comments made before this timestamp)-
	start_time = time.time()

	print("Crossmod = ACTIVE, starting at t = ", start_time)

	for comment in subreddit.stream.comments(): #to iterate through the comments and stream it live
		# do not process the comment if the comment is None
		if comment == None:
			continue

		start = time.time()
		
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
			try:
				comment_value = comment.body
				backend_predictions.update(classifiers.get_result(comment_value))
				print("Number of subreddit classifiers agreeing to remove comment = ", backend_predictions['agreement_score'])
				print("Number of norms violated = ", backend_predictions['norm_violation_score'])
			except Exception as ex:
				print(ex)
				continue
			
			### Compute the appropriate action to be performed from the config file based on back-end predictions! 
		ACTION = check_config(backend_predictions)
		print("Action = ", ACTION)

		end = time.time()
		print("processing time =", end-start, "seconds")

		if use_classifiers == 1:
			agreement_score = backend_predictions['agreement_score'] / len(subreddit_list)
		else:
			agreement_score = None

		### Write to CrossmodDB
		db.write(created_utc = datetime.datetime.fromtimestamp(comment.created_utc),
				ingested_utc = datetime.datetime.now(),
				id = comment.id,
				body = comment.body,
				toxicity_score = toxicity_score,
				crossmod_action = ACTION,
				author = comment.author.name,
				subreddit = comment.subreddit.display_name, 
				banned_by = None,
				banned_at_utc = None,
				agreement_score = agreement_score)

		
		if not perform_action:
			continue

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

if __name__ == '__main__':
	main()