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
    
    ## { 'agreement_score': 0.95, 'norm_violations_score': 5, 'subreddits_that_remove': ["science", "space"], 'norms_violated': ["violence"] }
    ## input_comment, clfs_type, clfs_ids
    def __init__(self, **kwargs):
        input_comment = kwargs['input_comment']
        clfs_type = kwargs['clfs_type']
        clfs_ids = kwargs['clfs_ids']

        self.clfs_pool = Pool(10)
        self.clfs_arguments = [{'clfs_type': clfs_type, 
                                'clfs_id': clf, 
                                'input_comment': input_comment} for clf in clfs_ids]

        # [ {'clfs_id': 'science', 'clfs_prediction': 1, 'clfs_type': SUBREDDIT }, {'clfs_id': 'space', 'clfs_prediction': 1, 'clfs_type': SUBREDDIT } ]
        self.clfs_predictions = self.clfs_pool.map(CrossmodClassifiers.run_classifier, self.clfs_arguments)
        self.clfs_pool.close()
        self.clfs_pool.join()
        
        self.total_clfs = len(clfs_ids)

        result = {
            'agreement_score': 0,
            'norm_violation_score': 0,
            'subreddits_that_remove': [],
            'norms_violated': []
        }


        for clfs_prediction in self.clfs_predictions:
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

        self.result = result

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

        print('PID: ' + str(os.getpid()))
        input_comment = arguments['input_comment']
        clfs_type = arguments['clfs_type']
        clfs_id = arguments['clfs_id']

        start = int(round(time.time() * 1000))

        if clfs_type == CrossmodClassifiers.SUBREDDIT_CLASSIFIERS:
            clf_path = CrossmodConsts.get_subreddit_classifier(clfs_id)

        elif clfs_type == CrossmodClassifiers.NORM_CLASSIFIERS:
            clf_path = CrossmodConsts.get_norms_classifier(clfs_id)

        clf = fasttext.load_model(clf_path)
        input_comment = CrossmodClassifiers.process_input_comment(input_comment)
        end = int(round(time.time() * 1000))

        print("Loading: ", end - start)
        
        start =  int(round(time.time() * 1000))

        clf_prediction = clf.predict(input_comment)

        end = int(round(time.time() * 1000))

        print("Predicting: ", end - start)

        if clf_prediction[0][0] == CrossmodClassifiers.REMOVED_COMMENT:
            clf_prediction = 1
        else:
            clf_prediction = 0

        print('PID is done now: ' + str(os.getpid()))
        # {'clfs_id': 'science', 'clfs_prediction': 1, 'clfs_type': SUBREDDIT }
        
        end_total = int(round(time.time() * 1000))

        print("loading and predicting: ", end_total - start_total)

        return { 'clfs_id': clfs_id, 'clfs_prediction': clf_prediction, 'clfs_type': clfs_type }
        
    def get_result(self):
        return self.result

def preprocessing(input_comments):
    
    train_text = pd.DataFrame()
    train_text['text'] = input_comments
    
    ###preprocessing -
    # print("Preprocessing... 1. split new lines, 2. convert to lowercase, and 3. strip numbers and punct")
    ### 1) remove newlines
    train_text['text'] = train_text['text'].replace('\n', ' ', regex = True)
    
    ## 2) convert to lowercase
    train_text['text'] = train_text['text'].str.lower()
    
    ### 3) remove punct and numbers: https://stackoverflow.com/questions/47947438/preprocessing-string-data-in-pandas-dataframe
    import re
    train_text['text'] = train_text.text.apply(lambda x : " ".join(re.findall('[\w]+',x)))
#     train_text["text"] = train_text['text'].str.apply(lambda x : " ".join(re.findall('[\w]+',x)))

    return train_text['text']

def get_classifier_predictions(input_comments, subreddit_list):
    count = 1

    ###result will be stored as a dataframe
    test_comments = pd.DataFrame()
    test_comments['comment'] = comments

    for study_sub in subreddit_list:
        # print(count, ") Expert: " , study_sub)
        count+=1
        command = [CrossmodConsts.FASTTEXT_BINARY, "predict", CrossmodConsts.get_subreddit_classifier(study_sub), "temp_comments.txt", "1"]
        result = subprocess.run(command, stdout=subprocess.PIPE)
        output = result.stdout.decode('utf-8')
        expert_decision = output.split('\n')[:-1]
        ###store each experts prediction as a new column, containing the subreddit's name
        test_comments['prediction_' + study_sub] = expert_decision
        test_comments['prediction_' + study_sub] = (test_comments['prediction_' + study_sub] == '__label__removed').astype(int)
        print(expert_decision)
    return test_comments

def get_classifier_prediction(study_sub):
    #input_comment = arguments['input_comment']
    #study_sub = arguments['subreddit']
    count = 1

    ###result will be stored as a dataframe
    test_comments = pd.DataFrame()

    # print(count, ") Expert: " , study_sub)
    count+=1
    command = [CrossmodConsts.FASTTEXT_BINARY, "predict", CrossmodConsts.get_subreddit_classifier(study_sub), "temp_comments.txt", "1"]
    result = subprocess.run(command, stdout=subprocess.PIPE)
    output = result.stdout.decode('utf-8')
    expert_decision = output.split('\n')[:-1]
    ###store each experts prediction as a new column, containing the subreddit's name
    test_comments['prediction_' + study_sub] = expert_decision
    test_comments['prediction_' + study_sub] = (test_comments['prediction_' + study_sub] == '__label__removed').astype(int)
    print(expert_decision)
    
    return test_comments


def main():
    classifiers = []

    import fileinput

    for line in fileinput.input():
        classifiers.append(line.replace('\n',''))

    #print(CrossmodClassifiers(input_comment = "you suck", 
    #                          clfs_type = CrossmodClassifiers.SUBREDDIT_CLASSIFIERS, 
    #                          clfs_ids = classifiers))
  
    

    arguments = [study_sub for study_sub in classifiers]

    print(arguments)

    #preprocess comments
    comments = preprocessing(["you suck"])
    
    #write comment to a file
    comment_to_file = open("temp_comments.txt", "w")
    
    for comment in comments:
        comment_to_file.write(comment)
        comment_to_file.write("\n")

    comment_to_file.close()

    print(get_classifier_prediction('AskReddit'))

    pool = Pool()

    results = pool.map(get_classifier_prediction, arguments)
    pool.close()
    pool.join()
    #print(get_classifier_predictions(["space is really awesome!"], ["technology", "Futurology", "space"]))

if __name__ == '__main__':
    main()
