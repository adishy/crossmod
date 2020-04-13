import pandas
import seaborn
import numpy as np
import matplotlib.pyplot as plt
from db import *

db = CrossmodDB()

class NumberOfCommentsVsAgreementScore:
    def __init__(self):
        self.db = CrossmodDB()
        self.axises = {'x': 'agreement_score',
                       'y': 'number_of_comments'}
        self.agreement_score_vs_numbers = self.read_agreement_score_vs_numbers()


    def get_number_of_comments(self, current_agreement_score):
        comments = self.db.database_session.query(CrossmodDBData).filter(CrossmodDBData.agreement_score >= current_agreement_score).count()

        return comments

    def read_agreement_score_vs_numbers(self):
        agreement_scores = []
        number_of_comments = []

        current_agreement_score = 0.51
        maximum_agreement_score = 1.0

        while(current_agreement_score <= maximum_agreement_score):
            agreement_scores.append(current_agreement_score)
            current_agreement_score += 0.01

        for agreement_score in agreement_scores:
            number_of_comments.append(self.get_number_of_comments(agreement_score))

        return {self.axises['x']: agreement_scores, 
                self.axises['y']: number_of_comments}

    def show_plot(self):

        agreement_score_vs_numbers = pandas.DataFrame(self.agreement_score_vs_numbers,
                                                      columns = list(self.axises.values()))

        number_of_comments = self.agreement_score_vs_numbers['number_of_comments']

        seaborn.set_style("darkgrid")
        line_plot = seaborn.lineplot(x = self.axises['x'], 
                                     y = self.axises['y'], 
                                     data = agreement_score_vs_numbers)

        line_plot.set_xlabel('Crossmod Agreement Score')
        line_plot.set_ylabel('Number of Comments')

        plt.yticks(np.arange(min(number_of_comments), max(number_of_comments) + 1, 400.0))
        plt.show()

class RemovedCommentsToxicityScoreAndBannedBy:
    def __init__(self):
        self.db = CrossmodDB()
        self.axises = {'x': 'banned_by',
                       'y': 'agreement_score'}
        self.removed_comments_banned_by = self.get_removed_comments_banned_by()

    def get_removed_comments_banned_by(self):
        agreement_scores = []

        banned_by = []

        automod_moderated_comments = self.db.database_session.query(CrossmodDBData).filter(CrossmodDBData.banned_by == 'AutoModerator')
            
        for row in automod_moderated_comments.all():
            agreement_scores.append(row.agreement_score)
            banned_by.append('AutoModerator')

        moderator_moderated_comments = self.db.database_session.query(CrossmodDBData).filter(CrossmodDBData.banned_by != None, CrossmodDBData.banned_by != 'AutoModerator')
    
        for row in moderator_moderated_comments.all():
            agreement_scores.append(row.agreement_score)
            banned_by.append('Moderators')

        crossmod_moderated_comments = self.db.database_session.query(CrossmodDBData).filter(CrossmodDBData.agreement_score >= 0.70)

        for row in crossmod_moderated_comments.all():
            agreement_scores.append(row.agreement_score)
            banned_by.append('Crossmod')

        return {self.axises['x']: banned_by, self.axises['y']: agreement_scores}

    def show_plot(self):
        removed_comments_banned_by = pandas.DataFrame(self.removed_comments_banned_by)

        seaborn.set_style("darkgrid")
        categorical_scatter_plot = seaborn.catplot(x = self.axises['x'], 
                                                   y = self.axises['y'], data = removed_comments_banned_by)

        categorical_scatter_plot.set(xlabel = 'Comments Flagged By', ylabel = 'Crossmod Agreement Score')
        plt.show()
        
if __name__ == "__main__":
    #NumberOfCommentsVsAgreementScore().show_plot()
    RemovedCommentsToxicityScoreAndBannedBy().show_plot()