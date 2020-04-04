# add source <path-to-crossmod-credentials.sh> in your ~/.profile file, 
# i.e. run 
# cat crossmod_credentials.sh >> file
# after filling in all the required credentials in this file, and renaming it to
# crossmod_credentials.sh (i.e. run mv crossmod_credentials_example.sh crossmod_credentials.sh)
# This makes all the credentials required by crossmod available as environment 
# variables

# DEPRECATED
export PERSPECTIVE_API_SECRET=a

# User Agent string for PRAW, (tell Reddit that we're a bot) For example: Testing Crossmod (by /u/CrossModerator)
export REDDIT_USER_AGENT=b

# Reddit Client ID obtained by creating a Reddit app at:
export REDDIT_CLIENT_ID=c

# Reddit Client Secret obtained by creating a Reddit app at:
export REDDIT_CLIENT_SECRET=d

# Password of the Reddit account to be used with PRAW
export REDDIT_PASSWORD=e

# Username of the Reddit account to be used with PRAW
export REDDIT_USERNAME=f

# Root directory where FastText classifiers are stored: 
# Crossmod expects the following subdirectories:
# <root-folder-specified>
# |_ norm-clfs
#     |_ <norm-1>.bin
#     |_ <norm-1>.vec
#     ..
# |_ subreddit-clfs
#     |_ <subreddit-1>.bin
#     |_ <subreddit-1>.vec
#      ..
export MODELS_DIRECTORY=g

# Path to store sqlite3 database file
export DB_PATH=h
