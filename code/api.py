## @TODO Add rate limit for each key
## @TODO Deploy FLASK to a production server
"""
==Documentation==
::Quick Start::
    - install DEPENDENCIES
    - Navigate to crossmod_api/code
    $ export FLASK_APP=api.py
    $ flask run


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

from getPredictions import *

from flask import Flask, request, jsonify
import pandas as pd
import traceback
import json


application = Flask(__name__)


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
    ## CONFIG VARIABLES ##
    subreddits_limit = 100
    auth_key = "ABCDEFG"
    call_rate_limit = 0 #@TODO: Time rate limit not yet implemented

    ## JSON REQUEST FIELDS ##
    comments = []
    subreddit_list = pd.read_csv("../data/study_subreddits.csv", names = ["subreddit"])["subreddit"][:subreddits_limit]     #default classifiers
    macro_norm_list = pd.read_csv('../data/macro-norms.txt', names = ['macronorms'])['macronorms']                          #default macro norms
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
        # which is a pandas series which contains a means to obtain
        # agreement_score AND subreddits_that_remove
        try:
            classifier_predictions = get_classifier_predictions(comments, subreddit_list)
        except Exception as ex:
            print(ex)
            return jsonify({'exception': ex})
        classifier_predictions['sum_votes'] = classifier_predictions.drop('comment', axis = 1).sum(axis = 1)


        ## GET macro_norm_predictions ##
        # a pandas series which contains a means to obtain
        # norm_violation_score AND norms_violated
        try:
            macro_norm_predictions = get_macronorm_classifier_predictions(comments, macro_norm_list)
        except Exception as ex:
            print (ex)
            return jsonify({'exception': ex})
        macro_norm_predictions['sum_votes'] = macro_norm_predictions.drop('comment', axis = 1).sum(axis = 1)


        ## ADD i comments JSON objects to response JSON array ##
        for i in range(len(comments)):
            ## INSTANTIATE ith comment's object ##
            json_comment = {}
            json_comment["agreement_score"] = None
            json_comment["norm_violation_score"] = None
            json_comment["subreddits_that_remove"] = []
            json_comment["norms_violated"] = []


            ## CALCULATE ith comment's agreement_score ##
            if number_of_classifiers != 0:
                # agreement_score = number of subreddits that would remove/total number of subreddits
                json_comment["agreement_score"] = classifier_predictions['sum_votes'][i] / number_of_classifiers

            ## FIND ith comment's subreddits_that_remove ##
            temp_classifier_predictions = classifier_predictions.drop('comment', axis = 1).drop('sum_votes', axis = 1)
            for subreddit in temp_classifier_predictions.columns:
                if temp_classifier_predictions.get(subreddit).values[i] == 1:
                    json_comment["subreddits_that_remove"].append(subreddit.split("prediction_")[1])


            ## CALCULATE ith comment's norm_violation_score ##
            if number_of_macro_norms != 0:
                # norm_violation_score = number of norms violated / total number of norms
                json_comment["norm_violation_score"] = macro_norm_predictions['sum_votes'][i] / number_of_macro_norms

            ## FIND ith comment's norms_violated ##
            temp_macro_norm_predictions = macro_norm_predictions.drop('comment', axis = 1).drop('sum_votes', axis = 1)
            for norm in temp_macro_norm_predictions.columns:
                if temp_macro_norm_predictions.get(norm).values[i] == 1:
                    json_comment["norms_violated"].append(norm)

            print("Number of subreddit classifiers agreeing to remove comment = ", classifier_predictions['sum_votes'][i], "/", number_of_classifiers)
            print("Agreement Score = ", json_comment["agreement_score"])
            print("Number of macro norms violated = ", macro_norm_predictions['sum_votes'][i], "/", number_of_macro_norms)
            print("norm violation score = ", json_comment["norm_violation_score"])


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
