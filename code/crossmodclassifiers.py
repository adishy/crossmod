import fasttext
import pandas as pd
from multiprocessing import Pool
import subprocess
import re
from crossmodconsts import *

class CrossmodClassifiers:    
    SUBREDDIT_CLASSIFIERS = "subreddit"
    NORMS_CLASSIFIERS = "norms"

    UNREMOVED_COMMENT = "__label__unremoved"
    REMOVED_COMMENT = "__label__removed"
    
    ## input_comment, clfs_type, clfs_ids
    def __init__(self, **kwargs):
        input_comment = kwargs['input_comment']
        clfs_type = kwargs['clfs_type']
        clfs_ids = kwargs['clfs_ids']

        self.clfs_pool = Pool(len(clfs_ids))
        self.clfs_arguments = [{'clfs_type': clfs_type, 
                                'clfs_id': clf, 
                                'input_comment': input_comment} for clf in clfs_ids]
        self.clfs_predictions = self.clfs_pool.map(CrossmodClassifiers.run_classifier, self.clfs_arguments)
        
        self.total_clfs = len(clfs_ids)
        self.agreement_score = 0
        for clfs_prediction in self.clfs_predictions:
            if clfs_prediction[0][0] == CrossmodClassifiers.REMOVED_COMMENT:
                self.agreement_score += 1

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
        input_comment = arguments['input_comment']
        clfs_type = arguments['clfs_type']
        clfs_id = arguments['clfs_id']

        if clfs_type == CrossmodClassifiers.SUBREDDIT_CLASSIFIERS:
            clf_path = CrossmodConsts.get_subreddit_classifier(clfs_id)

        elif clfs_type == CrossmodClassifiers.NORMS_CLASSIFIERS:
            clf_path = CrossmodConsts.get_norms_classifier(clfs_id)

        clf = fasttext.load_model(clf_path)
        input_comment = CrossmodClassifiers.process_input_comment(input_comment)
        clf_prediction = clf.predict(input_comment)

        return clf_prediction
        
    def get_agreement_score(self):
        return self.agreement_score / self.total_clfs

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
    #preprocess comments
    comments = preprocessing(input_comments)
    #write comment to a file
    comment_to_file = open("temp_comments.txt", "w")
    for comment in comments:
        comment_to_file.write(comment)
        comment_to_file.write("\n")

    comment_to_file.close()

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

def main():
    print(CrossmodClassifiers(input_comment = "just a comment", 
                        clfs_type = CrossmodClassifiers.SUBREDDIT_CLASSIFIERS, 
                        clfs_ids = ["technology", "Futurology", "space"]).get_agreement_score())

    print(get_classifier_predictions(["space is really awesome!"], ["technology", "Futurology", "space"]))

if __name__ == '__main__':
    main()