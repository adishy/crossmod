from crossmod.ml.classifiers import CrossmodClassifiers

from flask import Flask, request, jsonify
import pandas as pd
import traceback
import json


### CONFIG ###
call_rate_limit = 0 #@TODO: Rate limit for each key

subreddits_limit = 100
full_subreddit_list = list(pd.read_csv("../data/study_subreddits.csv", names = ["subreddit"])["subreddit"][:subreddits_limit])
full_macro_norm_list = list(pd.read_csv('../data/macro-norms.txt', names = ['macronorms'])['macronorms'])

classifiers = CrossmodClassifiers(subreddits = full_subreddit_list,
                                  norms = full_macro_norm_list) # globally load classifiers


@crossmod.app.route('/get-prediction-scores', methods=['POST'])
def get_prediction_scores():

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
        json_response = tuple(json_response)
        json_response = json.dumps(json_response)
        return json_response

    except:
        '''
        HANDLE errors
        '''
        return jsonify({'trace': traceback.format_exc()})

