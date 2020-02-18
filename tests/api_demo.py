#$ python3 api_demo.py
from datetime import datetime
import requests

## Config Variables ##
API_ENDPOINT = "http://crossmod.ml/api/v1/get-prediction-scores"
API_KEY = "ABCDEFG"


## EXAMPLE API REQUESTS
comments = ["FUCK YOU YOU LITTLE PIECE OF FUCKING SHIT", "THIS IS A BENIGN COMMENT, NO TOXCIITY HERE!", "To be fair, Donald Trumps policy may not be the best decisions in the world, but at least he tweets out really cool things", "Youre just a woman feminist feminazi"]

# Score comments with all subreddit classifiers and all macro norm classifiers

data = {"comments": comments,
        "key": API_KEY}


# Score comments with only Futurology, nba, pokemongo, and news subreddit classifiers, use all macros norms classifiers
'''
data = {"comments": comments,
        "subreddit_list": ["Futurology", "nba", "pokemongo", "news"],
        "key": API_KEY}
'''

# Score comments with no subreddit classifiers and only personal-attacks macro norm classifier
'''
data = {"comments": comments,
        "subreddit_list": [],
        "macro_norm_list": ["personal-attacks"],
        "key": API_KEY}
'''

# Score comments with all subreddit classifiers and no macro norm classifiers
'''
data = {"comments": comments,
        "macro_norm_list": [],
        "key": API_KEY}
'''



## Get request
startTime = datetime.now()
r = requests.post(url= API_ENDPOINT, json = data)
endTime = datetime.now()

print(r.json())
print("Time elapsed: ", (endTime - startTime))
