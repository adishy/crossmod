from crossmod.helpers.consts import *
from crossmod.helpers.filters import *
import fasttext
import pandas as pd
from multiprocessing import Pool
import subprocess
import re
import time
from progress.bar import ChargingBar
import sys
from io import StringIO

class CrossmodClassifiers:    
    UNREMOVED_COMMENT = "__label__unremoved"
    REMOVED_COMMENT = "__label__removed"
    
    subreddit_clfs = {}
    norm_clfs = {}

    ## { 'agreement_score': 0.95, 'norm_violations_score': 5, 'subreddits_that_remove': ["science", "space"], 'norms_violated': ["violence"] }
    ## input_comment, clfs_type, clfs_ids
    def __init__(self, **kwargs):
        subreddit_count = 0
        norm_count = 0

        # List of subreddit classifiers
        self.subreddit_clfs_ids = kwargs['subreddits']
        
        # List of norm classifiers
        self.norm_clfs_ids = kwargs['norms']

        start = time.time()
      
        sys.stderr = StringIO()

        # Load subreddit classifiers
        for clfs_id in ChargingBar('Loading Subreddit Classifiers:', max = 100).iter(self.subreddit_clfs_ids):
            if clfs_id not in CrossmodClassifiers.subreddit_clfs:
                CrossmodClassifiers.subreddit_clfs[clfs_id] = fasttext.load_model(CrossmodConsts.get_subreddit_classifier(clfs_id))
                subreddit_count += 1

        # Load norm classifiers
        for clfs_id in ChargingBar('Loading Norm Violation Classifiers:', max = 8).iter(self.norm_clfs_ids):
            if clfs_id not in CrossmodClassifiers.norm_clfs:
                CrossmodClassifiers.norm_clfs[clfs_id] = fasttext.load_model(CrossmodConsts.get_norms_classifier(clfs_id))
                norm_count += 1

        sys.stderr = sys.__stderr__

        end = time.time()
        print("Loaded classifiers: ", int(round(end - start)), "s") 
        print("Loaded ", subreddit_count, " subreddit classifiers, ", norm_count, " norm classifiers")
        
    @staticmethod
    def process_input_comment(input_comment):
        ### 1) remove URLs
        ### 2) remove subreddit names
        ### 3) remove newlines
        ##  4) convert to lowercase
        ### 5) remove punct and numbers
        for url in CrossmodFilters.get_urls(input_comment):
            input_comment = input_comment.replace(url, '')
        for subreddit_name in CrossmodFilters.get_subreddit_names(input_comment):
            input_comment = input_comment.replace()
        input_comment = input_comment.replace('\n', ' ')
        input_comment = input_comment.lower()
        input_comment = re.sub('[^A-Za-z]+', ' ', input_comment)

        return input_comment
        
    @staticmethod
    def run_classifier(arguments):
        start_total = int(round(time.time() * 1000))

        input_comment = arguments['input_comment']
        clfs_id = arguments['clfs_id']
        clfs_type = arguments['clfs_type']

        if clfs_type == CrossmodConsts.SUBREDDIT_CLASSIFIERS:
            clf = CrossmodClassifiers.subreddit_clfs[clfs_id]

        elif clfs_type == CrossmodConsts.NORM_CLASSIFIERS:
            clf = CrossmodClassifiers.norm_clfs[clfs_id]

        input_comment = CrossmodClassifiers.process_input_comment(input_comment)
        
        clf_prediction = clf.predict(input_comment)

        if clf_prediction[0][0] == CrossmodClassifiers.REMOVED_COMMENT:
            clf_prediction = 1
        else:
            clf_prediction = 0

        return { 'clfs_id': clfs_id, 'clfs_prediction': clf_prediction, 'clfs_type': clfs_type }
        
    def get_result(self, input_comment):
        clfs_predictions = list()

        for clf_id in self.subreddit_clfs_ids:
            clfs_predictions.append(CrossmodClassifiers.run_classifier({'clfs_type': CrossmodConsts.SUBREDDIT_CLASSIFIERS,
                                                                        'clfs_id': clf_id,
                                                                         'input_comment': input_comment}))

        for clf_id in self.norm_clfs_ids:
            clfs_predictions.append(CrossmodClassifiers.run_classifier({'clfs_type': CrossmodConsts.NORM_CLASSIFIERS,
                                                                        'clfs_id': clf_id,
                                                                        'input_comment': input_comment}))

        result = {
            'agreement_score': 0,
            'norm_violation_score': 0,
            'subreddits_that_remove': [],
            'norms_violated': []
        }


        for clfs_prediction in clfs_predictions:
            if clfs_prediction['clfs_prediction'] == 1:
                if clfs_prediction['clfs_type'] == CrossmodConsts.SUBREDDIT_CLASSIFIERS:
                    result['agreement_score'] += 1
                    result['subreddits_that_remove'].append(clfs_prediction['clfs_id'])

                elif clfs_prediction['clfs_type'] == CrossmodConsts.NORM_CLASSIFIERS:
                    result['norm_violation_score'] += 1
                    result['norms_violated'].append(clfs_prediction['clfs_id'])
                
                result['prediction_' + clfs_prediction['clfs_id']] = True

            else:
                result['prediction_' + clfs_prediction['clfs_id']] = False

        result['agreement_score'] /=  len(self.subreddit_clfs_ids)
        result['norm_violation_score'] /= len(self.norm_clfs_ids)
        
        return result
