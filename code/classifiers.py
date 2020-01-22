import fasttext
import pandas as pd
from multiprocessing import Pool
import subprocess
import re
from consts import *
import time
from filters import *

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

        # Load subreddit classifiers
        for clfs_id in self.subreddit_clfs_ids:
            if clfs_id not in CrossmodClassifiers.subreddit_clfs:
                CrossmodClassifiers.subreddit_clfs[clfs_id] = fasttext.load_model(CrossmodConsts.get_subreddit_classifier(clfs_id))
                subreddit_count += 1

        # Load norm classifiers
        for clfs_id in self.norm_clfs_ids:
            if clfs_id not in CrossmodClassifiers.norm_clfs:
                CrossmodClassifiers.norm_clfs[clfs_id] = fasttext.load_model(CrossmodConsts.get_norms_classifier(clfs_id))
                norm_count += 1

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
        clfs_pool = Pool()

        subreddit_clfs_arguments = [{'clfs_type': CrossmodConsts.SUBREDDIT_CLASSIFIERS, 
                                    'clfs_id': clf,
                                    'input_comment': input_comment} for clf in self.subreddit_clfs_ids]

        norm_clfs_arguments = [{'clfs_type': CrossmodConsts.NORM_CLASSIFIERS, 
                                'clfs_id': clf,
                                'input_comment': input_comment} for clf in self.norm_clfs_ids]

        # [ {'clfs_id': 'science', 'clfs_prediction': 1, 'clfs_type': SUBREDDIT }, {'clfs_id': 'space', 'clfs_prediction': 1, 'clfs_type': SUBREDDIT } ]
        clfs_predictions = clfs_pool.map(CrossmodClassifiers.run_classifier, subreddit_clfs_arguments + norm_clfs_arguments)
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

def input_comments_tests():
    input_with_urls = [ "add1 http://mit.edu.com you really kind of suck0",
                        "add2 https://facebook.jp.com.2. blah blah bleep bloop nooooo go away",
                        "add3 www.google.be. uvw",
                        "add4 https://www.google.be. 123",
                        "add5 www.website.gov.us test2",
                        "Hey bob on www.test.com." ,
                        "another test with ipv4 http://192.168.1.1/test.jpg. toto2",
                        "website with different port number www.test.com:8080/test.jpg not port 80",
                        "www.website.gov.us/login.html",
                        "test with ipv4 192.168.1.1/test.jpg.",
                        "search at google.co.jp/maps.",
                        "test with ipv6 2001:0db8:0000:85a3:0000:0000:ac1f:8001/test.jpg." ]

    for input_comment in input_with_urls:
        print(CrossmodClassifiers.process_input_comment(input_comment))

def main():
    input_comments_tests()


    return
    
    classifiers = []

    classifiers_file = open("sample.in", "r")
    clfs_ids = classifiers_file.readlines()

    for clfs_id in clfs_ids:
        classifiers.append(clfs_id.replace('\n', ''))

    print("Currently using: ", len(classifiers), " classifiers")

    subreddit_classifiers = ["AskReddit", "Futurology", "space", "technology"]

    norm_classifiers = ["abusing-and-criticisizing-mods", 
                        "hatespeech-racist-homophobic", 
                        "misogynistic-slurs", 
                        "namecalling-claiming-other-too-sensitive", 
                        "opposing-political-views-trump", 
                        "personal-attacks",
                        "porno-links",
                        "verbal-attacks-on-Reddit"]

    classifiers = CrossmodClassifiers(subreddits = subreddit_classifiers,
                                      norms = norm_classifiers)
  
    while(True):
        input_comment = input("input a comment for a subreddit: ")
    
        start = time.time()

        print(classifiers.get_result(input_comment))

        end = time.time()

        print("Predicted: ", int(round(end - start)), "s")

if __name__ == '__main__':
    main()
