#$ python3 api_demo.py
import requests

## Config Variables ##
API_ENDPOINT = "http://18.191.72.252:6000/get-prediction-scores"
API_KEY = "ABCDEFG"

## Comment and uncomment out "data" to see the different calls supported by the api ##

# Score comments with all subreddit classifiers and all macro norm classifiers
'''
data = {"comments": ["FUCK YOU YOU LITTLE PIECE OF FUCKING SHIT", "THIS IS A BENIGN COMMENT, NO TOXCIITY HERE!", "To be fair, Donald Trumps policy may not be the best decisions in the world, but at least he tweets out really cool things", "Youre just a woman feminist feminazi"],
        "key": API_KEY}
'''

# Score comments with only Futurology, nba, pokemongo, and news subreddit classifiers, use all macros norms classifiers
'''
data = {"comments": ["FUCK YOU YOU LITTLE PIECE OF FUCKING SHIT", "THIS IS A BENIGN COMMENT, NO TOXCIITY HERE!", "To be fair, Donald Trumps policy may not be the best decisions in the world, but at least he tweets out really cool things", "Youre just a woman feminist feminazi"],
        "subreddit_list": ["Futurology", "nba", "pokemongo", "news"],
        "key": API_KEY}
'''

# Score comments with no subreddit classifiers and only personal-attacks macro norm classifier
'''
data = {"comments": ["FUCK YOU YOU LITTLE PIECE OF FUCKING SHIT", "THIS IS A BENIGN COMMENT, NO TOXCIITY HERE!", "To be fair, Donald Trumps policy may not be the best decisions in the world, but at least he tweets out really cool things", "Youre just a woman feminist feminazi"],
        "subreddit_list": [],
        "macro_norm_list": ["personal-attacks"],
        "key": API_KEY}
'''

# Score comments with all subreddit classifiers and no macro norm classifiers
'''
data = {"comments": ["FUCK YOU YOU LITTLE PIECE OF FUCKING SHIT", "THIS IS A BENIGN COMMENT, NO TOXCIITY HERE!", "To be fair, Donald Trumps policy may not be the best decisions in the world, but at least he tweets out really cool things", "Youre just a woman feminist feminazi"],
        "macro_norm_list": [],
        "key": API_KEY}
'''

# Stress testing
num_of_comments = 100 # Adjust for stress testing
comments = [];
for i in range(0, num_of_comments):
    comments.append("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
data = {"comments": comments,
        "key": API_KEY}

## Get request
r = requests.post(url= API_ENDPOINT, json = data)

print(r.json())
