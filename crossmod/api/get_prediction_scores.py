## @TODO Tidy up code
## @TODO Update crossmod.ml documentation

## @TODO determine API rate limit based on concurrent and single endpoint tests
##       experiment with different numbers of worker processes
## @TODO Make sure key is private
## @TODO Integrate API with database
##       Tie rate limit to key, different access levels
##       Queueing system-- if too many concurrent calls, api currently just returns timeout
'''
ID      Key     Access_Level    Rate_Status(counter)    #_of_requests   Timestamp_of_Last_Request

Another database for queue?
'''

## @NOTE crossmod.ml is port 80

import crossmod

from crossmod.ml.classifiers import *
from crossmod.helpers.consts import *

from flask import Flask, request, jsonify, make_response
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

import pandas as pd
import traceback
import json
from flask_cors import CORS

application = Flask(__name__)
cors = CORS(application)

### CONFIG ###
auth_key = "ABCDEFG"
call_rate_limit = ["10 per minute", "600 per hour"] # set api rate limiting by remote address

subreddits_limit = 100
full_subreddit_list = CrossmodConsts.SUBREDDIT_LIST
full_macro_norm_list = CrossmodConsts.NORM_LIST

classifiers = CrossmodClassifiers(subreddits = full_subreddit_list,
                                  norms = full_macro_norm_list) # globally load classifiers

limiter = Limiter(
    application,
    key_func=get_remote_address,
    default_limits=call_rate_limit
)
## Exceeded call rate message ##
@application.errorhandler(429)
def ratelimit_handler(e):
    return make_response(
        jsonify(error="API call rate limit exceeded %s" % e.description)
        , 429
    )

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
@application.route('/get-prediction-scores', methods=['POST', 'GET'])
def getPredictionScores():
    print("Request:", request, "Method:", request.method)
    if request.method == 'GET':
        return '<html>GET</html>'
    print("Request data:", request.get_json(force=True))
    ## JSON REQUEST FIELDS ##
    comments = []
    subreddit_list = full_subreddit_list     #by default, use all classifiers
    macro_norm_list = full_macro_norm_list   #by default, use all macro norms
    key = ""

    try:
        '''
        Obtain JSON request
        '''
        json_ = request.get_json(force=True)
        comments = json_["comments"]
        print("Comments:", comments)
        key = json_["key"]


        # if JSON request contains values for optional fields "subreddit_list" and/or "macro_norm_list"
        #   then evaluate comments with specified classifiers
        # else use default classifiers and/or macro norms listed in
        #   ../data/study_subreddits.csv and/or ../data/macro-norms.txt
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
            return jsonify({'exception': "invalid api key " + key})


        '''
        Build JSON response
        '''
        json_response = []


        ## GET backend_predictions ##
        backend_predictions = []
        for i in range(len(comments)):
            backend_predictions.append(classifiers.get_result(comments[i]))



        ## ADD i comments' JSON objects to response JSON array ##
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

            ## Console debug statements ##
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
        #json_response = tuple(json_response)
        #json_response = json.dumps(json_response)
        return jsonify(json_response)

    except:
        '''
        HANDLE errors
        '''
        return jsonify({'trace': traceback.format_exc()})




if __name__ == "__main__":
    application.run(debug=True, host='0.0.0.0', port=8000)
