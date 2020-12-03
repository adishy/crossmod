import pandas as pd
import numpy as np
import json 
import requests 
import time
import os
import random

api_key = os.environ["VICTOR_PERSPECTIVE_API_KEY"]
url = ('https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze' +    
        '?key=' + api_key)

def get_api_score(row):
    time.sleep(random.uniform(1, 1.5))
    text = row["body"]
    data_dict = {
        'comment': {'text': text},
        'languages': ['en'],
        'requestedAttributes': {
            'TOXICITY': {},
            'SEVERE_TOXICITY': {},
            'TOXICITY_FAST': {},
            'IDENTITY_ATTACK': {},
            'INSULT': {},
            'PROFANITY': {},
            'THREAT': {},
            'SEXUALLY_EXPLICIT': {},
            'FLIRTATION': {},
        }
    }
    response = requests.post(url=url, data=json.dumps(data_dict)) 
    response_dict = json.loads(response.content)
    return response_dict

def main():
    pilot_study_file = "/data/databases/pilot_data.csv"
    df = pd.read_csv(pilot_study_file)
    # reporting_experiment_file = "/data/databases/reporting_experiment.csv"
    # data = pd.read_csv(reporting_experiment_file)
    # erroneous_file = "/data/databases/erroneous_reporting_experiment_data.csv"
    # data = pd.read_csv(erroneous_file)
    # big_query_file = "/data/databases/big_query_control_data_sept_2019_to_dec_2019.csv"
    # data = pd.read_csv(big_query_file)

    p_toxicity_scores = []
    p_severe_toxicity_scores = []
    p_fast_toxicity_scores = []
    p_identity_attack_scores = []
    p_insult_scores = []
    p_profanity_scores = []
    p_threat_scores = []
    p_sexually_scores = []
    p_filtration_scores = []
    error_row = []

    size = 100
    list_of_dfs = [df.loc[i:i+size-1,:] for i in range(0, len(df), size)]
    for data in list_of_dfs:
        print(data.shape)

    for data in list_of_dfs:
        for index, row in data.iterrows():
            response_dict = get_api_score(row)
            try:
                p_toxicity_scores.append(response_dict["attributeScores"]["TOXICITY"]["summaryScore"]["value"])
                p_severe_toxicity_scores.append(response_dict["attributeScores"]["SEVERE_TOXICITY"]["summaryScore"]["value"])
                p_fast_toxicity_scores.append(response_dict["attributeScores"]["TOXICITY_FAST"]["summaryScore"]["value"])
                p_identity_attack_scores.append(response_dict["attributeScores"]["IDENTITY_ATTACK"]["summaryScore"]["value"])
                p_insult_scores.append(response_dict["attributeScores"]["INSULT"]["summaryScore"]["value"])
                p_profanity_scores.append(response_dict["attributeScores"]["PROFANITY"]["summaryScore"]["value"])
                p_threat_scores.append(response_dict["attributeScores"]["THREAT"]["summaryScore"]["value"])
                p_sexually_scores.append(response_dict["attributeScores"]["SEXUALLY_EXPLICIT"]["summaryScore"]["value"])
                p_filtration_scores.append(response_dict["attributeScores"]["FLIRTATION"]["summaryScore"]["value"])
            except:
                print(index)
                print(response_dict)
                error_row.append(row)
                p_toxicity_scores.append(-1)
                p_severe_toxicity_scores.append(-1)
                p_fast_toxicity_scores.append(-1)
                p_identity_attack_scores.append(-1)
                p_insult_scores.append(-1)
                p_profanity_scores.append(-1)
                p_threat_scores.append(-1)
                p_sexually_scores.append(-1)
                p_filtration_scores.append(-1)

            if index % 100 == 0:
                print(index)

        df.to_csv('my_csv.csv', mode='w+', header=False)

if __name__ == "__main__":
    main()
