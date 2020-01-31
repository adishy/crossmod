## @TODO Tidy up code
## @TODO Update documentation on githubpages document and push
##  --Make sure every thing's public except for key, port 80 for crossmod.ml

## @TODO Add new option to api_demo to generate comment list of x comments (for stress testing)
## @TODO Add rate limit for each key
##  -Research how other people do rate limits
## @TODO Queueing system
"""
==Documentation==
::Quick Start::
    - install DEPENDENCIES
    - Navigate to crossmod_api/code
    $ export FLASK_APP=api.py
    $ flask run

    - If you run into [Errno 98] Address already in use, try a different port such as 6000:
    $ flask run -h localhost -p 6000


::Requests::
    The JSON request is an object with the following fields:
    {
        "comments": [ comment1, comment2, ... ],
        "subreddit_list": [ classifier1, classifier2, ... ],
        "macro_norm_list": [ norm1, norm2, ... ],
        "key": KEY
    }
    - "comments": array of comment strings to be evaulated by Crossmod
    - "subreddit_list" (OPTIONAL): list of subreddit classifiers used to predict scores.
        + If field is left blank, the default classifiers in ../data/study_subreddits.csv will all be used
        + If field is passed a blank list [], no classifiers will be used, and no agreement score will be found
    - "macro_norm_list" (OPTIONAL): list of macro norms used to predict scores.
        + If field is left blank, the default macro norms in ../data/macro-norms.txt will all be used
        + If field is passed a blank list [], no macro norms will be used, and no norm violation score will be found
    - "key": string used for authentication.
        + currently, for debugging, key is set to "ABCDEFG"

    #Example Requests#
    While flask is running:
        - rating comments with all classifiers and no macro norms
            $ curl -d '{"comments": ["FUCK YOU YOU LITTLE PIECE OF FUCKING SHIT", "And why wouldnt they be? He has done nothing but shart his way up to the top time and time again and even managed to become POTUS. Even if he does face repercussions, hes old as fuck already. He got to live like royalty all his life.", "You are just a woman. Go back to the kitchen where you belong, scum"], "macro_norm_list": [], "key": "ABCDEFG"}' -H "Content-Type: application/json" -X POST http://localhost:5000/get-prediction-scores

        - rating comments with only select classifiers and all macro norms
            $ curl -d '{"comments": ["FUCK YOU YOU LITTLE PIECE OF FUCKING SHIT", "And why wouldnt they be? He has done nothing but shart his way up to the top time and time again and even managed to become POTUS. Even if he does face repercussions, hes old as fuck already. He got to live like royalty all his life.", "You are just a woman. Go back to the kitchen where you belong, scum"], "subreddit_list": ["Futurology", "nba", "AskReddit", "science", "politics", "pokemongo"], "key": "ABCDEFG"}' -H "Content-Type: application/json" -X POST http://localhost:5000/get-prediction-scores

        - rating comments with all classifiers and all macro norms
            $ curl -d '{"comments": ["FUCK YOU YOU LITTLE PIECE OF FUCKING SHIT", "And why wouldnt they be? He has done nothing but shart his way up to the top time and time again and even managed to become POTUS. Even if he does face repercussions, hes old as fuck already. He got to live like royalty all his life.", "You are just a woman. Go back to the kitchen where you belong, scum"], "key": "ABCDEFG"}' -H "Content-Type: application/json" -X POST http://localhost:5000/get-prediction-scores

            *** If you ran Flask on a different port than 5000, you will need to change the routing.
            *** Change http://localhost:5000/get-prediction-scores to http://localhost:YOURPORT/get-prediction-scores

::Responses::
    The JSON response is an array of JSON objects, where the index of each JSON object
    corresponds to the index of the original comment in the request.
    [
        {
            'agreement_score': AGREEMENT_SCORE,
            'norm_violation_score': NORM_VIOLATION_SCORE,
            'subreddits_that_remove': [ subreddit1, subreddit2, ... ],
            'norms_violated': [ norm1, norm2, ... ]
        },
        ....
    ]
    - "agreement_score": prediction score from subreddit classifiers.
        + if no classifiers were used, is a NULL value.
    - "norm_violation_score": prediction score from macro norms.
        + if no macro norms were used, is a NULL value.
    - "subreddits_that_remove": list of classifiers that would have removed the comment.
        + if no classifiers were used, is an empty list
    - "norms_violated": list of norms that were violated by the comment.
        + if no macro norms were used, is an empty listed

    **NOTE: CHECK IF agreement_score OR norm_violation_score IS NULL
            NOT IF subreddits_that_remove OR norms_violated IS EMPTY
             because a NULL value implies that classifiers and/or macro norms were not used
             whereas an EMPTY list does NOT NECESSARILY imply the above


::Dependencies::
    -getPredictions.py
    -flask
    -pandas
    -traceback
    -json


::Common Troubleshooting::
    - Make sure getPredictions.py points to the correct paths for the norm/reddit models and the fastText directory
    - Make sure fastText binaries are compiled on local machine.
        + If not, navigate to /fastText-0.9.1
            $ make clean && make
"""

from crossmodclassifiers import *

from flask import Flask, request, jsonify
import pandas as pd
import traceback
import json


application = Flask(__name__)
application.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

### GLOBAL LOADING OF CLASSIFIERS
auth_key = "ABCDEFG"
call_rate_limit = 0 #@TODO: Time rate limit not yet implemented

subreddits_limit = 100
full_subreddit_list = list(pd.read_csv("../data/study_subreddits.csv", names = ["subreddit"])["subreddit"][:subreddits_limit])
full_macro_norm_list = list(pd.read_csv('../data/macro-norms.txt', names = ['macronorms'])['macronorms'])

classifiers = CrossmodClassifiers(subreddits = full_subreddit_list,
                                  norms = full_macro_norm_list) # Load Classifiers

### REQUEST: JSON Object ###
"""
{
    "comments": [ comment1, comment2, ... ],
    "subreddit_list": [ classifier1, classifier2, ... ],
    "macro_norm_list": [ norm1, norm2, ... ],
    "key": KEY
}
"""
### RESPONSE: JSON Array ###
"""
[
    {
        'agreement_score': AGREEMENT_SCORE,
        'norm_violation_score': NORM_VIOLATION_SCORE,
        'subreddits_that_remove': [ subreddit1, subreddit2, ... ],
        'norms_violated': [ norm1, norm2, ... ]
    },
    ....
]
"""
@application.route('/get-prediction-scores', methods=['POST'])
def getPredictionScores():

    ## JSON REQUEST FIELDS ##
    comments = []
    subreddit_list = full_subreddit_list     #by default, use all classifiers
    macro_norm_list = full_macro_norm_list   #by default, use all macro norms
    key = ""

    try:
        '''
        Obtain JSON request
        '''
        json_ = request.json
        comments = json_["comments"]
        key = json_["key"]

        # If JSON request contains values for optional fields "subreddit_list" and "macro_norm_list",
        # evaluate comment using those values.
        # Otherwise use the all default classifiers and/or macro norms
        # in ../data/study_subreddits.csv and/or ../data/macro-norms.txt
        if 'subreddit_list' in json_:
            subreddit_list = pd.Series(json_["subreddit_list"])
        if 'macro_norm_list' in json_:
            macro_norm_list = pd.Series(json_["macro_norm_list"])

        number_of_classifiers=len(subreddit_list);
        number_of_macro_norms=len(macro_norm_list)


        '''
        Authenticate key
        '''
        if key != auth_key:
            return jsonify({'exception': "invalid key"})


        '''
        Build JSON response
        '''
        json_response = []


        ## GET classifier_predictions ##
        # ex {'agreement_score': 1, 'norm_violation_score': 0, 'subreddits_that_remove': ['Futurology'], 'norms_violated': [], 'prediction_Futurology': True}
        backend_predictions = []
        for i in range(len(comments)):
            backend_predictions.append(classifiers.get_result(comments[i]))



        ## ADD i comments JSON objects to response JSON array ##
        for i in range(len(comments)):
            ## INSTANTIATE ith comment's object ##
            json_comment = {}
            json_comment["agreement_score"] = None
            json_comment["norm_violation_score"] = None
            json_comment["subreddits_that_remove"] = []
            json_comment["norms_violated"] = []

            ## CALCULATE ith comment's agreement_score ##
            agreement_score = 0
            if number_of_classifiers != 0:
                # agreement_score = number of subreddits that would remove/total number of subreddits
                for classifier in subreddit_list:
                    if backend_predictions[i]["prediction_" + classifier] == True:
                        agreement_score += 1

                        ## Find subreddits_that_remove ##
                        json_comment["subreddits_that_remove"].append(classifier)

                json_comment["agreement_score"] = agreement_score / number_of_classifiers


            ## CALCULATE ith comment's norm_violation_score ##
            norm_violation_score = 0
            if number_of_macro_norms != 0:
                # norm_violation_score = number of norms violated / total number of norms
                for norm in macro_norm_list:
                    if backend_predictions[i]["prediction_" + norm] == True:
                        norm_violation_score += 1

                        ## Find norms violated ##
                        json_comment["norms_violated"].append(norm)

                json_comment["norm_violation_score"] = norm_violation_score / number_of_macro_norms

            print("COMMENT:", comments[i][0:100], "...", sep="")
            print("# of classifiers removing comment = ", agreement_score, "/", number_of_classifiers)
            print("agreement_score = ", json_comment["agreement_score"])
            print("--")
            print("# of macro norms violated = ", norm_violation_score, "/", number_of_macro_norms)
            print("norm violation score = ", json_comment["norm_violation_score"])
            print("________________________")


            ## ADD ith comment to JSON response ##
            json_response.append(json_comment)


        '''
        RETURN JSON response
        '''
        json_response = tuple(json_response)
        json_response = json.dumps(json_response)
        return json_response

    except:
        '''
        HANDLE errors
        '''
        return jsonify({'trace': traceback.format_exc()})




if __name__ == "__main__":
    application.run(host='0.0.0.0')
