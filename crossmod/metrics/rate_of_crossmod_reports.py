from crossmod.environments import CrossmodConsts
from crossmod.db.interface import CrossmodDB 
from crossmod.db import DataTable
from sqlalchemy import func
from dateutil import tz
import pandas
import seaborn
import os
import datetime
import numpy as np
import matplotlib.pyplot as plt

class RateOfCrossmodReports:
    def __init__(self, subreddit):
        self.db = CrossmodDB()
        self.axises = {'x': 'date',
                       'y': 'number_of_reports'}
        self.subreddit = subreddit
        self.start = self.db.database_session.query(func.min(DataTable.created_utc)).scalar()
        self.number_of_reports = self.read_number_of_comments()
        self.output_directory = os.path.join(CrossmodConsts.METRICS_OUTPUT_DIRECTORY, "rate_of_crossmod_reports")
        os.makedirs(self.output_directory, exist_ok=True)
        self.output_format = "png"

    def get_number_of_reports(self, start, end):
        number_of_reports = self.db.database_session.query(DataTable).filter(DataTable.subreddit == self.subreddit, 
                                                                             DataTable.crossmod_action == "report", 
                                                                             DataTable.ingested_utc >= start, 
                                                                             DataTable.ingested_utc < end).count()

        return number_of_reports

    def read_number_of_comments(self):
        dates = [i for i in range(1, (datetime.datetime.now() - self.start).days)]
        number_of_reports = [0] + [self.get_number_of_reports(self.start + datetime.timedelta(days = dates[i-1]), 
                                                              self.start + datetime.timedelta(days = dates[i])) for i in range(1, len(dates))]
        return {self.axises['x']: dates, 
                self.axises['y']: number_of_reports}

    def create_plot(self):
        number_of_reports = pandas.DataFrame(self.number_of_reports,
                                              columns = list(self.axises.values()))
        seaborn.set_style("darkgrid")
        line_plot = seaborn.lineplot(x = self.axises['x'], 
                                     y = self.axises['y'], 
                                     data = number_of_reports)
        line_plot.set_title(f'Number of Reports made by Crossmod each day since {self.start.strftime("%b %d %Y")} for r/{self.subreddit}')
        line_plot.set_xlabel(f'Days since {self.start.strftime("%b %d %Y")}')
        line_plot.set_ylabel('Number of Comments')

        return line_plot

    def show_plot(self):
        line_plot = self.create_plot()
        plt.show()

    def save_plot(self):
        line_plot = self.create_plot()
        plt.savefig(os.path.join(self.output_directory, f"{datetime.datetime.now()}.{self.output_format}"),  dpi=600)

RateOfCrossmodReports("Futurology").save_plot()