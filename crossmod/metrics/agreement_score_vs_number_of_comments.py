import pandas
import seaborn
import os
import datetime
import numpy as np
import matplotlib.pyplot as plt
from crossmod.environments import CrossmodConsts
from crossmod.db.interface import CrossmodDB 
from crossmod.db import DataTable

class AgreementScoreVsComments:
    def __init__(self, subreddit):
        self.db = CrossmodDB()
        self.axises = {'x': 'number_of_comments',
                       'y': 'agreement_score'}
        self.subreddit = subreddit
        self.agreement_score_vs_numbers = self.read_agreement_score_vs_numbers()
        self.output_directory = os.path.join(CrossmodConsts.METRICS_OUTPUT_DIRECTORY, "agreement_score_vs_comments")
        os.makedirs(self.output_directory, exist_ok=True)
        self.output_format = "png"

    def get_number_of_comments(self, current_agreement_score):
        comments = self.db.database_session.query(DataTable).filter(DataTable.subreddit == self.subreddit, DataTable.agreement_score >= current_agreement_score).count()
        return comments

    def read_agreement_score_vs_numbers(self, agreement_score_start = 50, agreement_score_end = 100, delta = 5):
        agreement_scores = [i * 0.01 for i in range(agreement_score_start, agreement_score_end, delta)]
        number_of_comments = [self.get_number_of_comments(i) for i in agreement_scores]

        return {self.axises['x']: number_of_comments, 
                self.axises['y']: agreement_scores}

    def create_plot(self):
        agreement_score_vs_numbers = pandas.DataFrame(self.agreement_score_vs_numbers,
                                                      columns = list(self.axises.values()))
        seaborn.set_style("darkgrid")
        line_plot = seaborn.lineplot(x = self.axises['x'], 
                                     y = self.axises['y'], 
                                     data = agreement_score_vs_numbers)
        line_plot.set_title(f'Number of Comments vs. Crossmod Agreement Score for r/{self.subreddit}')
        line_plot.set_xlabel('Crossmod Agreement Score')
        line_plot.set_ylabel('Number of Comments')

        return line_plot

    def show_plot(self):
        line_plot = self.create_plot()
        plt.show()

    def save_plot(self):
        line_plot = self.create_plot()
        plt.savefig(os.path.join(self.output_directory, f"{self.subreddit}_{datetime.datetime.now()}.{self.output_format}"),  dpi=600)
