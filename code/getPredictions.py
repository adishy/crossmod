import pandas as pd
import subprocess
from crossmodconsts import *

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
        # print(expert_decision)
    return test_comments

def get_macronorm_classifier_predictions(input_comments, norms_list):
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

    for norm in norms_list:
        # print(count, ") Expert: " , study_sub)
        count+=1
        command = [CrossmodConsts.FASTTEXT_BINARY, "predict", CrossmodConsts.get_norms_classifier(norm), "temp_comments.txt", "1"]
        result = subprocess.run(command, stdout=subprocess.PIPE)
        output = result.stdout.decode('utf-8')
        expert_decision = output.split('\n')[:-1]
        ###store each experts prediction as a new column, containing the subreddit's name
        test_comments['prediction_' + norm] = expert_decision
        test_comments['prediction_' + norm] = (test_comments['prediction_' + norm] == '__label__removed').astype(int)
        # print(expert_decision)
    return test_comments

if __name__ == '__main__':
    # main code
    print("Get predictions from pre-trained experts on test comments!")

    classifiers = []

    classifiers_file = open("sample2.in", "r")
    clfs_ids = classifiers_file.readlines()

    for clfs_id in clfs_ids:
        classifiers.append(clfs_id.replace('\n', ''))

    comment_list = []

    comments_file = open("batch_sample_1000.in", "r")
    comments = comments_file.readlines()

    for comment in comments:
        comment_list.append(comment)

    predictions = get_classifier_predictions(comment_list, classifiers)

    print(predictions)
    print("Predictions from pre-trained exports on test comments = COMPLETE!")
