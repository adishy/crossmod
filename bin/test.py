import praw
from crossmod.environments import CrossmodConsts

reddit = praw.Reddit(user_agent = CrossmodConsts.REDDIT_USER_AGENT,
                                  client_id = CrossmodConsts.UPDATER_REDDIT_CLIENT_ID, 
                                  client_secret = CrossmodConsts.UPDATER_REDDIT_CLIENT_SECRET,
                                  username = CrossmodConsts.REDDIT_USERNAME, 
                                  password = CrossmodConsts.REDDIT_PASSWORD)

for log in reddit.subreddit("Futurology").mod.log(limit=200):
      print("Mod: {}, Subreddit: {}".format(log.mod, log.subreddit))

#for reported_item in reddit.subreddit("Futurology").mod.reports():
#    print("User Reports: {}".format(reported_item.user_reports))
#    print("Mod Reports: {}".format(reported_item.mod_reports))
