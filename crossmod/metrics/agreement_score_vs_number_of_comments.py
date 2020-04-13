import pandas
import seaborn
import numpy as np
import matplotlib.pyplot as plt
from crossmod.db.interface import CrossmodDB 
from crossmod.db import DataTable

class AgreementScoreVsComments:
    def __init__(self, subreddit):
        self.db = CrossmodDB()
        self.axises = {'x': 'agreement_score',
                       'y': 'number_of_comments'}
        self.subreddit = subreddit
        self.agreement_score_vs_numbers = self.read_agreement_score_vs_numbers()


    def get_number_of_comments(self, current_agreement_score):
        comments = self.db.database_session.query(DataTable).filter(DataTable.subreddit == self.subreddit, DataTable.agreement_score >= current_agreement_score).count()

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

AgreementScoreVsComments("Futurology").show_plot()