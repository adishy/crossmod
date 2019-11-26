import fasttext
import pandas as pd
from multiprocessing import Pool
import subprocess
import re
from crossmodconsts import *
import time

class CrossmodClassifiers:    
    SUBREDDIT_CLASSIFIERS = "subreddit"
    NORM_CLASSIFIERS = "norms"

    UNREMOVED_COMMENT = "__label__unremoved"
    REMOVED_COMMENT = "__label__removed"
    
    subreddit_clfs = {}

    ## { 'agreement_score': 0.95, 'norm_violations_score': 5, 'subreddits_that_remove': ["science", "space"], 'norms_violated': ["violence"] }
    ## input_comment, clfs_type, clfs_ids
    def __init__(self, **kwargs):
        count = 0
           
        self.clfs_type = kwargs['clfs_type']
        self.clfs_ids = kwargs['clfs_ids']
       
        if(self.clfs_type == CrossmodClassifiers.SUBREDDIT_CLASSIFIERS):
            start = time.time()
            for clfs_id in self.clfs_ids:
                if clfs_id not in CrossmodClassifiers.subreddit_clfs:
                    CrossmodClassifiers.subreddit_clfs[clfs_id] = fasttext.load_model(CrossmodConsts.get_subreddit_classifier(clfs_id))
                    print("Loaded classifier: ", count)
                    count += 1

            end = time.time()
            print("Loaded classifiers: ", int(round(end - start)), "s") 

    @staticmethod
    def process_input_comment(input_comment):
        ### 1) remove newlines
        ##  2) convert to lowercase
        ### 3) remove punct and numbers
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
        clf = CrossmodClassifiers.subreddit_clfs[clfs_id]

        input_comment = CrossmodClassifiers.process_input_comment(input_comment)
        
        clf_prediction = clf.predict(input_comment)

        if clf_prediction[0][0] == CrossmodClassifiers.REMOVED_COMMENT:
            clf_prediction = 1
        else:
            clf_prediction = 0

        return { 'clfs_id': clfs_id, 'clfs_prediction': clf_prediction, 'clfs_type': clfs_type }
        
    def get_result(self, input_comment):
        clfs_pool = Pool()
        clfs_arguments = [{'clfs_type': self.clfs_type, 
                           'clfs_id': clf,
                           'input_comment': input_comment} for clf in self.clfs_ids]

        # [ {'clfs_id': 'science', 'clfs_prediction': 1, 'clfs_type': SUBREDDIT }, {'clfs_id': 'space', 'clfs_prediction': 1, 'clfs_type': SUBREDDIT } ]
        clfs_predictions = clfs_pool.map(CrossmodClassifiers.run_classifier, clfs_arguments)
        clfs_pool.close()
        clfs_pool.join()
        
        result = {
            'agreement_score': 0,
            'norm_violation_score': 0,
            'subreddits_that_remove': [],
            'norms_violated': []
        }


        for clfs_prediction in clfs_predictions:
            if clfs_prediction['clfs_prediction'] == 1:
                if clfs_prediction['clfs_type'] == CrossmodClassifiers.SUBREDDIT_CLASSIFIERS:
                    result['agreement_score'] += 1
                    result['subreddits_that_remove'].append(clfs_prediction['clfs_id'])

                elif clfs_prediction['clfs_type'] == CrossmodClassifiers.NORM_CLASSIFIERS:
                    result['norm_violation_score'] += 1
                    result['norms_violated'].append(clfs_prediction['clfs_id'])
                
                result['prediction_' + clfs_prediction['clfs_id']] = True

            else:
                result['prediction_' + clfs_prediction['clfs_id']] = False

        return result

def main():
    classifiers = []

    classifiers_file = open("sample.in", "r")
    clfs_ids = classifiers_file.readlines()

    for clfs_id in clfs_ids:
        classifiers.append(clfs_id.replace('\n', ''))

    print("Currently using: ", len(classifiers), " classifiers")

    subreddit_classifiers = CrossmodClassifiers(clfs_type = CrossmodClassifiers.SUBREDDIT_CLASSIFIERS, 
                                                clfs_ids = classifiers)
  
  
    while(True):
        input_comment = input("input a comment for a subreddit: ")
    
        start = time.time()

        print(subreddit_classifiers.get_result(input_comment))

        end = time.time()

        print("Predicted: ", int(round(end - start)), "s")

if __name__ == '__main__':
    main()
